# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import RPi.GPIO as GPIO
#GPIO.setwarnings(False)
## set GPIO mode to BCM. This is needed to support analog devices through gpiozero
logger.debug('Setting terrariumPI GPIO Mode to %s' % (GPIO.BCM,))
GPIO.setmode(GPIO.BCM)
logger.debug('Done setting terrariumPI GPIO Mode to %s' % (GPIO.BCM,))

try:
  import thread as _thread
except ImportError as ex:
  import _thread
import time
import datetime
import uptime
import os
import psutil
import subprocess
import re
import json
import pyfiglet

from hashlib import md5
from gevent import sleep

from terrariumConfig import terrariumConfig
from terrariumWeather import terrariumWeather, terrariumWeatherSourceException
from terrariumSensor import terrariumSensor
from terrariumSwitch import terrariumPowerSwitch
from terrariumDoor import terrariumDoor
from terrariumWebcam import terrariumWebcam, terrariumWebcamSourceException
from terrariumAudio import terrariumAudioPlayer
from terrariumCollector import terrariumCollector
from terrariumEnvironment import terrariumEnvironment
from terrariumNotification import terrariumNotification
from terrariumCalendar import terrariumCalendar

from terrariumUtils import terrariumUtils

class terrariumEngine(object):

  LOOP_TIMEOUT = 30

  def __init__(self):
    # Default system units
    self.__units = {'temperature' : 'C',
                    'distance'    : 'cm',
                    'humidity'    : '%',
                    'moisture'    : '%',
                    'conductivity': 'mS',
                    'ph'          : 'pH',
                    'light'       : 'lux',
                    'uva'         : 'uW/cm^2',
                    'uvb'         : 'uW/cm^2',
                    'uvi'         : '',
                    'fertility'   : 'uS/cm',
                    'co2'         : 'ppm',
                    'volume'      : 'L',
                    'windspeed'   : 'kmh'}

    # List of queues for websocket communication
    self.subscribed_queues = []

    self.device = ''
    regex = r"product: (?P<device>.*)"
    hw=os.popen("lshw -c system 2>/dev/null")
    for line in hw.readlines():
      matches = re.search(regex, line)
      if matches:
        self.device = matches.group('device')
        break
    hw.close()

    # Default power usage for a PI
    self.pi_power_wattage = 5

    self.environment = None

    # Load config
    logger.info('Loading terrariumPI config')
    self.config = terrariumConfig()
    logger.info('Done Loading terrariumPI config')

    # Check for update
    self.current_version = self.config.get_system()['version']
    self.update_available = False
    self.update_last_check = datetime.datetime.fromtimestamp(0)
    self.update_version = None
    self.__update_check()

    # Notification engine
    self.notification = terrariumNotification()
    self.notification.set_profile_image(self.get_profile_image())

    # Calendar engine
    self.calendar = terrariumCalendar()

    logger.info('Setting terrariumPI authentication')
    self.set_authentication(self.config.get_admin(),self.config.get_password())
    logger.info('Done setting terrariumPI authentication')

    # Load data collector for historical data
    logger.info('Loading terrariumPI collector')
    self.collector = terrariumCollector(self.current_version)
    logger.info('Done loading terrariumPI collector')

    # Set the Pi power usage (including usb devices directly on the PI)
    logger.info('Loading terrariumPI PI power setting')
    self.pi_power_wattage = float(self.config.get_pi_power_wattage())
    logger.info('Done loading terrariumPI PI power setting')

    # Set the system temperature indicator
    logger.info('Loading terrariumPI PI temperature indicator')
    self.set_temperature_indicator(self.config.get_temperature_indicator())
    logger.info('Done loading terrariumPI PI temperature indicator')

    # Set the system distance indicator
    logger.info('Loading terrariumPI PI distance indicator')
    self.set_distance_indicator(self.config.get_distance_indicator())
    logger.info('Done loading terrariumPI PI distance indicator')

    # Set the system windspeed indicator
    logger.info('Loading terrariumPI PI windspeed indicator')
    self.set_windspeed_indicator(self.config.get_windspeed_indicator())
    logger.info('Done loading terrariumPI PI windspeed indicator')

    # Set the system volume indicator
    logger.info('Loading terrariumPI PI volume indicator')
    self.set_volume_indicator(self.config.get_volume_indicator())
    logger.info('Done loading terrariumPI PI volume indicator')

    # Load Weather part
    self.weather = None
    if self.config.get_weather_location():
      logger.info('Loading terrariumPI weather data')
      self.weather = terrariumWeather(self.config.get_weather_location(),
                                      self.get_temperature_indicator,
                                      self.get_windspeed_indicator,
                                      self.get_weather)

    logger.info('Done loading terrariumPI weather data')

    # Load humidity and temperature sensors
    self.__load_sensors()

    # Load Powerswitches part
    self.__load_power_switches()

    # Load doors from config
    self.__load_doors()

    # Load the environment system. This will controll the lights, sprayer and heaters
    logger.debug('Loading terrariumPI environment system')
    self.environment = terrariumEnvironment(self.sensors, self.power_switches, self.weather, self.is_door_open, self.config.get_environment,self.notification)
    logger.debug('Done loading terrariumPI environment system')

    # Load webcams from config
    self.__load_webcams()

    # Load audio system
    self.__audio_player = terrariumAudioPlayer(self.config.get_audio_playlists(),
                                               self.config.get_active_soundcard(),
                                               any(self.power_switches[switchid].is_pwm_dimmer() for switchid in self.power_switches),
                                               self.get_audio_playing)

    # Start system update loop
    self.__running = True
    _thread.start_new_thread(self.__engine_loop, ())
    _thread.start_new_thread(self.__webcam_loop, ())
    _thread.start_new_thread(self.__log_tail, ())
    logger.info('TerrariumPI engine is running')

  def __update_check(self):
    if datetime.datetime.now() - self.update_last_check > datetime.timedelta(days=1):
      version_data = terrariumUtils.get_remote_data('https://api.github.com/repos/theyosh/TerrariumPI/releases/latest',json=True)
      if version_data is None:
        logger.warning('Unable to get the latest version information from Github. Will check next round.')
        return None

      self.update_version = version_data['tag_name']
      self.update_available = int(self.update_version.replace('.','')) > int(self.current_version.replace('.',''))
      self.update_last_check = datetime.datetime.now()

  # Private/internal functions
  def __load_sensors(self,data = None):
    # Load Sensors, with ID as index
    starttime = time.time()
    reloading = data is not None

    logger.info('%s terrariumPI sensors' % ('Reloading' if reloading else 'Loading',))

    sensor_config = (self.config.get_sensors() if not reloading else data)
    if not reloading:
      self.sensors = {}

    exclude_ids = []
    for sensor_data in sensor_config:
      if 'exclude' in sensor_data and terrariumUtils.is_true(sensor_data['exclude']):
        logger.info('Excluding sensor with ID {}'.format(sensor_data['id']))
        exclude_ids.append(sensor_data['id'])

    seen_sensors = []
    for sensor in terrariumSensor.scan_sensors(self.__unit_type):
      if sensor.get_id() not in self.sensors and sensor.get_id() not in exclude_ids:
        self.sensors[sensor.get_id()] = sensor

    for sensordata in sensor_config:
      if sensordata['id'] in exclude_ids:
        continue

      if sensordata['id'] not in self.sensors:
        # New sensor (add)
        try:
          sensor = terrariumSensor(sensordata['id'],
                                   sensordata['hardwaretype'],
                                   sensordata['type'],
                                   sensordata['address'],
                                   sensordata['name'],
                                   self.__unit_type)

          self.sensors[sensor.get_id()] = sensor
        except Exception as ex:
          logger.exception('Error adding sensor type {} with name {}'.format(sensordata['type'],sensordata['name']))
          continue

      else:
        # Existing sensor
        sensor = self.sensors[sensordata['id']]
        # Should not be able to change setings
        #sensor.set_hardware_type(sensordata['hardwaretype'])
        #sensor.set_type(sensordata['type'],self.__unit_type)
        sensor.set_address(sensordata['address'])

      sensor.set_name(sensordata['name'])
      sensor.set_alarm_min(sensordata['alarm_min'])
      sensor.set_alarm_max(sensordata['alarm_max'])
      sensor.set_limit_min(sensordata['limit_min'])
      sensor.set_limit_max(sensordata['limit_max'])

      # TEMP
      if 'max_diff' not in sensordata:
        sensordata['max_diff'] = abs(sensor.get_limit_max() - sensor.get_limit_min()) * 0.25

      sensor.set_max_diff(sensordata['max_diff'])

      if 'chirp' == sensor.get_type():
        if 'min_moist' in sensordata and sensordata['min_moist'] is not None:
          sensor.set_min_moist_calibration(sensordata['min_moist'])
        if 'max_moist' in sensordata and sensordata['max_moist'] is not None:
          sensor.set_max_moist_calibration(sensordata['max_moist'])
        if 'temp_offset' in sensordata and sensordata['temp_offset'] is not None:
          sensor.set_temperature_offset_calibration(sensordata['temp_offset'])

      if 'exclude_avg' in sensordata and sensordata['exclude_avg'] is not None:
        sensor.set_exclude_avg(sensordata['exclude_avg'])

      seen_sensors.append(sensor.get_id())


    if reloading:
      for sensor_id in set(self.sensors) - set(seen_sensors):
        # clean up old deleted sensors
        del(self.sensors[sensor_id])

      self.environment.set_sensors(self.sensors)

    logger.info('Done %s terrariumPI sensors. Found %d sensors in %.3f seconds' % ('reloading' if reloading else 'loading',
                                                                                      len(self.sensors),
                                                                                      time.time()-starttime))

  def __load_power_switches(self,data = None):
    # Load Switches, with ID as index
    starttime = time.time()
    starting_up = data is None

    logger.info('{} terrariumPI switches'.format('Starting up' if starting_up else 'Updating'))

    power_switches_config = (self.config.get_power_switches() if starting_up else data)
    seen_power_switches = []

    logger.debug('Loading excluding IDs')
    exclude_ids = []
    for switch_data in power_switches_config:
      if 'exclude' in switch_data and terrariumUtils.is_true(switch_data['exclude']):
        logger.info('Excluding power switch with ID {}'.format(switch_data['id']))
        exclude_ids.append(switch_data['id'])

    logger.info('Loaded {} excluding IDs: {}'.format(len(exclude_ids),exclude_ids))

    prev_state = {}
    if starting_up:
      logger.info('Loading previous power switch states from the last 12 hours')
      start = int(time.time())
      prev_data = self.collector.get_history(['switches'],start,start-43200)

      if 'switches' in prev_data:
        for switch in prev_data['switches']:
          if switch in exclude_ids:
            continue

          prev_state[switch] = prev_data['switches'][switch]['power_wattage'][-1:][0][1]

      self.power_switches = {}
      for power_switch in terrariumPowerSwitch.scan_power_switches(self.toggle_power_switch,**self.config.get_meross_cloud()):
        if power_switch.get_id() not in exclude_ids and power_switch.get_id() not in self.power_switches:
          self.power_switches[power_switch.get_id()] = power_switch

    for power_switch_config in power_switches_config:
      if power_switch_config['id'] in exclude_ids:
        continue

      prev_power_state = terrariumPowerSwitch.OFF

      if power_switch_config['id'] in prev_state and prev_state[power_switch_config['id']] > 0:
        prev_power_state = terrariumPowerSwitch.ON

        if 'dimmer' in power_switch_config['hardwaretype'] or 'brightpi' == power_switch_config['hardwaretype']:
          prev_power_state = (float(prev_state[power_switch_config['id']]) / float(power_switch_config['power_wattage'])) * 100

      if power_switch_config['id'] in [None,'None',''] or power_switch_config['id'] not in self.power_switches:
        # New switch (add)
        if power_switch_config['id'] in prev_state:
          logger.info('Starting up switch {} with state {}'.format(power_switch_config['name'],prev_power_state))

        power_switch = terrariumPowerSwitch(power_switch_config['id'],
                                            power_switch_config['hardwaretype'],
                                            power_switch_config['address'],
                                            power_switch_config['name'],
                                            prev_power_state,
                                            callback=self.toggle_power_switch)
        self.power_switches[power_switch.get_id()] = power_switch
      else:
        # Existing switch
        power_switch = self.power_switches[power_switch_config['id']]
        power_switch.set_address(power_switch_config['address'])
        power_switch.set_name(power_switch_config['name'])
        if power_switch.get_id() in prev_state:
          logger.info('Starting up switch {} with state {}'.format(power_switch_config['name'],prev_power_state))
          power_switch.set_state(prev_power_state)

      power_switch.set_power_wattage(power_switch_config['power_wattage'])
      power_switch.set_water_flow(power_switch_config['water_flow'])

      if 'last_replacement_date' in power_switch_config:
        power_switch.set_last_hardware_replacement(power_switch_config['last_replacement_date'])

      if 'manual_mode' in power_switch_config:
        power_switch.set_manual_mode(power_switch_config['manual_mode'])

      power_switch.set_timer(power_switch_config['timer_start'],
                             power_switch_config['timer_stop'],
                             power_switch_config['timer_on_duration'],
                             power_switch_config['timer_off_duration'],
                             power_switch_config['timer_enabled'])

      if power_switch.is_dimmer():
        power_switch.set_dimmer(power_switch_config['dimmer_duration'],
                                power_switch_config['dimmer_step'],
                                power_switch_config['dimmer_on_duration'],
                                power_switch_config['dimmer_off_duration'],
                                power_switch_config['dimmer_on_percentage'],
                                power_switch_config['dimmer_off_percentage'])

      seen_power_switches.append(power_switch.get_id())

    if not starting_up:
      for power_switch_id in set(self.power_switches) - set(seen_power_switches):
        # clean up old deleted switches
        del(self.power_switches[power_switch_id])

      # Should not be needed.... environment needs callback to engine to get this information
      self.environment.set_power_switches(self.power_switches)

    logger.info('Done %s terrariumPI switches. Found %d switches in %.3f seconds' % ('starting up' if starting_up else 'updating',
                                                                                      len(self.power_switches),
                                                                                      time.time()-starttime))

  def __load_doors(self,data = None):
    # Load Doors, with ID as index
    starttime = time.time()
    reloading = data is not None

    logger.info('%s terrariumPI doors' % ('Reloading' if reloading else 'Loading',))

    door_config = (self.config.get_doors() if not reloading else data)
    if not reloading:
      self.doors = {}

    seen_doors = []
    for doordata in door_config:
      if doordata['id'] is None or doordata['id'] == 'None' or doordata['id'] not in self.doors:
        # New switch (add)
        door = terrariumDoor(None,
                             doordata['hardwaretype'],
                             doordata['address'],
                             doordata['name'],
                             callback=self.toggle_door_status)
        self.doors[door.get_id()] = door
      else:
        # Existing switch
        door = self.doors[doordata['id']]
        # Should not be able to change setings
        #door.set_hardware_type(doordata['hardwaretype'])
        door.set_address(doordata['address'])
        door.set_name(doordata['name'])

      seen_doors.append(door.get_id())

    if reloading:
      for door_id in set(self.doors) - set(seen_doors):
        # clean up old deleted switches
        del(self.doors[door_id])

    logger.info('Done %s terrariumPI doors. Found %d doors in %.3f seconds' % ('reloading' if reloading else 'loading',
                                                                              len(self.doors),
                                                                              time.time()-starttime))

  def __load_webcams(self, data = None):
    # Load Webcams, with ID as index
    starttime = time.time()
    reloading = data is not None

    logger.info('%s terrariumPI webcams' % ('Reloading' if reloading else 'Loading',))

    webcam_config = (self.config.get_webcams() if not reloading else data)
    if not reloading:
      self.webcams = {}

    seen_webcams = []
    for webcamdata in webcam_config:
      if webcamdata['id'] is None or webcamdata['id'] == 'None' or webcamdata['id'] not in self.webcams:
        # New webcam (add)
        width = 640
        height = 480
        awb = 'auto'
        archive = False
        archive_light = 'ignore'
        archive_door = 'ignore'
        motion_boxes = True
        motion_delta_threshold = 25
        motion_min_area = 500
        motion_compare_frame = 'last'

        if 'resolution_width' in webcamdata and 'resolution_height' in webcamdata:
          width = webcamdata['resolution_width']
          height = webcamdata['resolution_height']

        if 'archive' in webcamdata:
          archive = webcamdata['archive']

        if 'archivelight' in webcamdata:
          archive_light = webcamdata['archivelight']

        if 'archivedoor' in webcamdata:
          archive_door = webcamdata['archivedoor']

        if 'motionboxes' in webcamdata:
          motion_boxes = webcamdata['motionboxes']

        if 'motion_delta_threshold' in webcamdata:
          motion_delta_threshold = webcamdata['motiondeltathreshold']

        if 'motion_min_area' in webcamdata:
          motion_min_area = webcamdata['motionminarea']

        if 'motion_compare_frame' in webcamdata:
          motion_compare_frame = webcamdata['motioncompareframe']

        # don't let bad location data kill the system
        try:
          webcam = terrariumWebcam(None,
                                   webcamdata['location'],
                                   webcamdata['name'],
                                   webcamdata['rotation'],
                                   width,
                                   height,
                                   awb,
                                   archive,
                                   archive_light,
                                   archive_door,
                                   self.environment)
          webcam.set_motion_boxes(motion_boxes)
          webcam.set_motion_delta_threshold(motion_delta_threshold)
          webcam.set_motion_min_area(motion_min_area)
          webcam.set_motion_compare_frame(motion_compare_frame)

          self.webcams[webcam.get_id()] = webcam
        except Exception as err:
          print(err)
          continue
      else:
        # Existing webcam
        webcam = self.webcams[webcamdata['id']]
        # Should not be able to change setings
        #webcam.set_hardware_type(doordata['hardwaretype'])
        webcam.set_location(webcamdata['location'])
        webcam.set_name(webcamdata['name'])

      webcam.set_rotation(webcamdata['rotation'])

      if 'resolution_width' in webcamdata and 'resolution_height' in webcamdata:
        webcam.set_resolution(webcamdata['resolution_width'],webcamdata['resolution_height'])

      if 'archive' in webcamdata:
        webcam.set_archive(webcamdata['archive'])

      if 'archivelight' in webcamdata:
        webcam.set_archive_light(webcamdata['archivelight'])

      if 'archivedoor' in webcamdata:
        webcam.set_archive_door(webcamdata['archivedoor'])

      if 'motionboxes' in webcamdata:
        webcam.set_motion_boxes(webcamdata['motionboxes'])

      if 'motiondeltathreshold' in webcamdata:
        webcam.set_motion_delta_threshold(webcamdata['motiondeltathreshold'])

      if 'motionminarea' in webcamdata:
        webcam.set_motion_min_area(webcamdata['motionminarea'])

      if 'motioncompareframe' in webcamdata:
        webcam.set_motion_compare_frame(webcamdata['motioncompareframe'])

      if 'awb' in webcamdata:
        webcam.set_awb(webcamdata['awb'])

      if 'realtimedata' in webcamdata:
        webcam.set_realtimedata(webcamdata['realtimedata'])

      seen_webcams.append(webcam.get_id())

      if reloading and webcam.is_live():
        webcam.start()

    if reloading:
      for webcam_id in set(self.webcams) - set(seen_webcams):
        # clean up old deleted switches
        del(self.webcams[webcam_id])

    logger.info('Done %s terrariumPI webcams. Found %d webcams in %.3f seconds' % ('reloading' if reloading else 'loading',
                                                                              len(self.webcams),
                                                                              time.time()-starttime))

  def __get_current_power_usage_water_flow(self, socket = False):
    data = {'power' : {'current' : self.pi_power_wattage , 'max' : self.pi_power_wattage},
            'water' : {'current' : 0.0 , 'max' : 0.0}}

    for switchid in self.power_switches:
      data['power']['current'] += self.power_switches[switchid].get_current_power_wattage()
      data['power']['max'] += self.power_switches[switchid].get_power_wattage()

      data['water']['current'] += self.power_switches[switchid].get_current_water_flow()
      data['water']['max'] += self.power_switches[switchid].get_water_flow()

    return data

  def __get_total_power_usage_water_flow(self):
    totals = self.collector.get_total_power_water_usage()
    totals['power_wattage']['wattage'] += totals['power_wattage']['duration'] * self.pi_power_wattage

    return totals

  def __webcam_loop(self):
    time_short = 0
    error_counter = 0
    logger.info('Start terrariumPI webcams')
    while self.__running:
      starttime = time.time()
      for webcamid in self.webcams:
        self.webcams[webcamid].update()
        sleep(0.1)

      duration = (time.time() - starttime) + time_short
      if duration < terrariumEngine.LOOP_TIMEOUT:
        if error_counter > 0:
          error_counter -= 1
        logger.info('Webcam update(s) done in %.5f seconds. Waiting for %.5f seconds for next update' % (duration,terrariumEngine.LOOP_TIMEOUT - duration))
        time_short = 0
        sleep(terrariumEngine.LOOP_TIMEOUT - duration) # TODO: Config setting
      else:
        error_counter += 1
        if error_counter > 9:
          logger.error('Webcam update(s) is having problems keeping up. Could not update in 30 seconds for %s times!' % error_counter)

        logger.warning('Webcam update(s) took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumEngine.LOOP_TIMEOUT,terrariumEngine.LOOP_TIMEOUT))
        time_short = duration - terrariumEngine.LOOP_TIMEOUT
        if time_short > 12:
          # More then 12 seconds to late.... probably never fast enough...
          time_short = 0

  def __engine_loop(self):
    time_short = 0
    error_counter = 0
    logger.info('Start terrariumPI engine')
    while self.__running:
      starttime = time.time()

      # Version update check
      self.__update_check()

      motddata = {'average' : [],
                  'system' : 0,
                  'duration' : 0,
                  'error' : ''}

      # Update weather
      if self.weather is not None:
        self.weather.update()
        weather_data = self.weather.get_data()
        if 'hour_forecast' in weather_data and len(weather_data['hour_forecast']) > 0:
          self.collector.log_weather_data(weather_data['hour_forecast'][0])

      # Update sensors
      for sensorid in self.sensors:
        try:
          # Update the current sensor.
          self.sensors[sensorid].update()
          # Save new data to database
          self.collector.log_sensor_data(self.sensors[sensorid].get_data())
          # Websocket callback
          self.get_sensors([sensorid],socket=True)
          # Send notification when needed and enabled
          if self.sensors[sensorid].is_active() and self.sensors[sensorid].notification_enabled() and self.sensors[sensorid].get_alarm():
            self.notification.message('sensor_alarm_' + ('low' if self.sensors[sensorid].get_current() < self.sensors[sensorid].get_alarm_min() else 'high'),self.sensors[sensorid].get_data())

        except Exception as err:
          logger.exception('Engine loop: Sensor has problems: {}'.format(err))

        # Make time for other web request
        sleep(0.1)

      # Update (remote) power switches
      motddata['power_switches'] = []
      for power_switch_id in self.power_switches:
        try:
          # Update timer trigger if activated
          #self.power_switches[power_switch_id].timer()
          # Update the current sensor.
          self.power_switches[power_switch_id].update()
          if self.power_switches[power_switch_id].get_state() > 0:
            power_state = '{}%'.format(self.power_switches[power_switch_id].get_state())
            if not self.power_switches[power_switch_id].is_dimmer():
              power_state = 'on' if self.power_switches[power_switch_id].is_on() else 'off'

            motddata['power_switches'].append({'name' : self.power_switches[power_switch_id].get_name(),
                                               'state' : power_state})

        except Exception as err:
          logger.exception('Engine loop: Power switch has problems: {}'.format(err))

        # Make time for other web request
        sleep(0.1)

      # Get the current average temperatures
      average_data = self.get_sensors(['average'])['sensors']
      motddata['average'] = average_data

      # Websocket callback
      self.__send_message({'type':'sensor_gauge','data':average_data})

      # Websocket messages back
      self.get_uptime(socket=True)
      self.get_power_usage_water_flow(socket=True)
      self.get_environment(socket=True)
      self.get_audio_playing(socket=True)

      # Log system stats
      system_data = self.get_system_stats()
      motddata['system'] = system_data
      self.collector.log_system_data(system_data)
      self.get_system_stats(socket=True)

      display_message = ['%s %s' % (_('Uptime'),terrariumUtils.format_uptime(system_data['uptime']),),
                         '%s %s %s %s' % (_('Load'),system_data['load']['load1'],system_data['load']['load5'],system_data['load']['load15']),
                         '%s %.2f%s' % (_('CPU Temp.'),system_data['temperature'],self.get_temperature_indicator())]

      for env_part in average_data:
        alarm_icon = '!' if average_data[env_part]['alarm'] else ''
        display_message.append('%s%s %.2f%s%s' % (alarm_icon,_(env_part.replace('average_','').title()), average_data[env_part]['current'],average_data[env_part]['indicator'],alarm_icon))

      self.notification.send_display("\n".join(display_message))

      duration = (time.time() - starttime) + time_short
      motddata['duration'] = duration
      if duration < terrariumEngine.LOOP_TIMEOUT:
        if error_counter > 0:
          error_counter -= 1
        logger.info('Update done in %.5f seconds. Waiting for %.5f seconds for next update' % (duration,terrariumEngine.LOOP_TIMEOUT - duration))
        time_short = 0
        sleep(terrariumEngine.LOOP_TIMEOUT - duration) # TODO: Config setting
      else:
        error_counter += 1
        if error_counter > 9:
          error_message = 'Updating is having problems keeping up. Could not update in {} seconds for {} times!'.format(terrariumEngine.LOOP_TIMEOUT,error_counter)
          motddata['error'] = error_message
          logger.error(error_message)

        logger.warning('Updating took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumEngine.LOOP_TIMEOUT,terrariumEngine.LOOP_TIMEOUT))
        time_short = duration - terrariumEngine.LOOP_TIMEOUT
        if time_short > 12:
          # More then 12 seconds to late.... probably never fast enough...
          time_short = 0

      self.__update_motd(motddata)

  def __update_motd(self,data):
    template = """#!/bin/bash

# FIX Colors
export TERM=xterm-256color

# Some colors
black=$(tput setaf 0)
red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
blue=$(tput setaf 4)
purple=$(tput setaf 5)
cyan=$(tput setaf 6)
white=$(tput setaf 7)
gray=$(tput setaf 8)
reset=$(tput sgr0)

# The message
"""

    motd_lines = template.splitlines()

    system_title = self.config.get_system()['title'].replace(self.config.get_system()['version'],'').strip()
    motd_title_part1 = None
    motd_title_part2 = None

    f = pyfiglet.Figlet(font='doom')

    if system_title.lower().endswith('pi'):
      motd_title_part1 = f.renderText(re.sub('pi','',system_title,flags=re.IGNORECASE).strip()).split('\n')
      motd_title_part2 = f.renderText('PI').split('\n')

    else:
      motd_title_part1 =f.renderText(system_title).split('\n')

    spaces = int((80 - (len(max(motd_title_part1,key=len)) + (0 if motd_title_part2 is None else len(max(motd_title_part2,key=len))))) / 2)
    spaces = spaces * ' '

    for counter, line in enumerate(motd_title_part1):
        if len(line.strip()) == 0:
            continue

        motd_line = 'echo "' + spaces + ' ${green}' + line.replace('`','\`')
        if motd_title_part2 is not None and counter < len(motd_title_part2):
            motd_line += ' ${red}' + motd_title_part2[counter].replace('`','\`').strip()

        motd_line += '"'
        motd_lines.append(motd_line)

    motd_lines.append('echo "${reset} "')

    motd_name = '{:<40}'.format(spaces + '   ' + self.config.get_profile_name())

    motd_lines.append('echo "{}{}{}: {}{}{}"'.format(
        '${blue}' + motd_name + '${reset}',
        '${yellow}' if self.update_available else '        ',
        _('Version'),
        self.current_version,
        ' / {}'.format(self.update_version) if self.update_available else '',
        '${reset}' if self.update_available else ''))

    if self.update_available:
      motd_lines.append('echo "  New version available: https://github.com/theyosh/TerrariumPI/releases"')

    motd_lines.append('echo ""')

    left_lines = []
    left_padding = 0
    # Add average values
    avg_order = ['temperature','humidity','moisture','conductivity','distance','ph','light','fertility','co2','volume']
    for avg_type in avg_order:
      avg_key = 'average_{}'.format(avg_type)
      if avg_key in data['average']:
        left_lines.append({'key'   : _('Average {}'.format(avg_type.title())),
                           'value' : '{:8.2f} {:6}'.format(data['average'][avg_key]['current'],data['average'][avg_key]['indicator']),
                           'alarm' : data['average'][avg_key]['alarm']})

    right_lines = []
    right_lines.append({'key'   : _('Uptime'),
                        'value' : terrariumUtils.format_uptime(data['system']['uptime']),
                        'alarm' : False})

    right_lines.append({'key'   : _('Disk usage'),
                        'value' : '{} (Free) / {} (Total)'.format(terrariumUtils.format_filesize(data['system']['disk']['free']),
                                                                  terrariumUtils.format_filesize(data['system']['disk']['total'])),
                        'alarm' : False})

    right_lines.append({'key'   : _('Memory usage'),
                        'value' : '{} (Free) / {} (Total)'.format(terrariumUtils.format_filesize(data['system']['memory']['free']),
                                                                  terrariumUtils.format_filesize(data['system']['memory']['total'])),
                        'alarm' : False})

    right_lines.append({'key'   : _('CPU Load'),
                        'value' : '{:.2f}, {:.2f}, {:.2f}'.format(data['system']['load']['load1'],
                                                                  data['system']['load']['load5'],
                                                                  data['system']['load']['load15']),
                        'alarm' : False})

    right_lines.append({'key'   : _('CPU Temperature'),
                        'value' : '{:.2f} C'.format(data['system']['temperature']),
                        'alarm' : False})

    if len(left_lines) > 0:
      left_padding  = max([len(line['key']) for line in left_lines])
    right_padding = max([len(line['key']) for line in right_lines])

    line_nr = 0
    while line_nr < max(len(left_lines),len(right_lines)):
      motd_line = 'echo "'
      if line_nr < len(left_lines):
        motd_line += '  {:{width}}'.format(left_lines[line_nr]['key'] + ':',width=left_padding+1) + ('${yellow}' if left_lines[line_nr]['alarm'] else '') + left_lines[line_nr]['value'] + ('${reset}' if left_lines[line_nr]['alarm'] else '')
      else:
        motd_line += '                                    '

      if line_nr < len(right_lines):
        motd_line += '{:{width}}'.format(right_lines[line_nr]['key'] + ':',width=right_padding+1) + ' ' + ('${yellow}' if right_lines[line_nr]['alarm'] else '') + right_lines[line_nr]['value'] + ('${reset}' if right_lines[line_nr]['alarm'] else '')

      motd_line += '"'
      motd_lines.append(motd_line)
      line_nr += 1

    motd_lines.append('echo ""')
    motd_lines.append('echo "  Amount of power switches on: {}"'.format(len(data['power_switches'])))
    for line in data['power_switches']:
      motd_lines.append('echo "  Power switch {} is at state: {}"'.format(line['name'],line['state']))

    motd_lines.append('echo ""')
    if '' != data['error']:
      motd_lines.append('echo "  {}{}{}"'.format('${red}',data['error'],'${reset}'))
      motd_lines.append('echo ""')

    motd_lines.append('echo "      {}Last update: {:%d-%m-%Y %H:%M:%S}{}"'.format('${blue}',datetime.datetime.now(),'${reset}'))
    motd_lines.append('echo ""')

    #print('\n'.join(motd_lines))
    with open('motd.sh','w') as motdfile:
      motdfile.write('\n'.join(motd_lines))

    os.chmod('motd.sh', 0o755)

  def __send_message(self,message):
    clients = self.subscribed_queues
    for queue in clients:
      queue.put(message)
      # If more then 50 messages in queue, looks like connection is gone and remove the queue from the list
      if queue.qsize() > 50:
        self.subscribed_queues.remove(queue)

  def __log_tail(self):
    logger.info('Start terrariumPI engine log')
    logtail = subprocess.Popen(['tail','-F','log/terrariumpi.log'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for line in logtail.stdout:
      self.__send_message({'type':'logtail','data':line.strip().decode('utf-8')})
      if not self.__running:
        logger.info('Stopped terrariumPI engine log')
        logtail.kill()

  def __unit_type(self,unittype):
    if unittype in self.__units:
      return self.__units[unittype]

    return None

  def stop(self):
    # Stop engine processing first....
    self.__running = False

    self.environment.stop()

    for sensorid in self.sensors:
      self.sensors[sensorid].stop()
      logger.info('Stopped type {} {} sensor {} at address {}'.format(self.sensors[sensorid].get_type(),self.sensors[sensorid].get_sensor_type(),self.sensors[sensorid].get_name(),self.sensors[sensorid].get_address()))

    for power_switch_id in self.power_switches:
      self.power_switches[power_switch_id].stop()
      logger.info('Stopped power switch {} at address {}'.format(self.power_switches[power_switch_id].get_name(),self.power_switches[power_switch_id].get_address()))

    for door_id in self.doors:
      self.doors[door_id].stop()
      logger.info('Stopped door {} at address {}'.format(self.doors[door_id].get_name(),self.doors[door_id].get_address()))

    for webcam_id in self.webcams:
      self.webcams[webcam_id].stop()
      logger.info('Stopped webcam {} at address {}'.format(self.webcams[webcam_id].get_name(),self.webcams[webcam_id].get_location()))

    self.notification.stop()
    self.collector.stop()

    logger.info('Shutdown engine')
  # End private/internal functions

  # Weather part
  def set_weather_config(self,data):
    try:
      self.weather = terrariumWeather(data['location'],
                                      self.get_temperature_indicator,
                                      self.get_windspeed_indicator,
                                      self.get_weather)
    except terrariumWeatherSourceException as ex:
      return False

    return self.config.save_weather(data)

  def get_weather_config(self):
    if self.weather is None:
      return {}

    return self.weather.get_config()

  def get_weather(self, parameters = [], socket = False):

    try:
      data = self.weather.get_data()
    except Exception as ex:
      # This is happening when during startup the data changes... so save to ignore
#      logger.error('Strange weather.. error https://github.com/theyosh/TerrariumPI/issues/246: {}'.format(ex))
      return None

    self.environment.update()

    if socket:
      self.__send_message({'type':'update_weather','data':data})
    else:
      return data
  # End weather part

  # Sensors part
  def get_sensors(self, parameters = [], socket = False):
    data = []
    filtertype = None
    temperature_type = None

    if len(parameters) > 0 and parameters[-1] in ['celsius','fahrenheit','kelvin']:
      temperature_type = parameters[-1].lower()
      if 'celsius' == temperature_type:
        temperature_type = 'C'
      if 'fahrenheit' == temperature_type:
        temperature_type = 'F'
      if 'kelvin' == temperature_type:
        temperature_type = 'K'

      del(parameters[-1])

    if len(parameters) > 0 and parameters[0] is not None:
      filtertype = parameters[0]

    # Filter is based on sensorid
    if filtertype is not None and filtertype in self.sensors:
      data.append(self.sensors[filtertype].get_data(temperature_type=temperature_type))

    else:
      for sensorid in self.sensors:
        # Filter based on sensor type
        # Exclude Chirp light sensors for average calculation in favour of Lux measurements
        if filtertype is None or (filtertype == 'average' and not (self.sensors[sensorid].get_exclude_avg() or (self.sensors[sensorid].get_sensor_type() == 'light' and self.sensors[sensorid].get_type() == 'chirp'))) or filtertype == self.sensors[sensorid].get_sensor_type():
          data.append(self.sensors[sensorid].get_data(temperature_type=temperature_type))

    if 'average' == filtertype or len(parameters) == 2 and parameters[1] == 'average':
      average = {}
      for sensor in data:
        if sensor['current'] is None:
          continue

        sensor['type'] = 'average_' +  sensor['type']
        if sensor['type'] not in average:
          average[sensor['type']] = {'current' : 0.0, 'alarm_min' : 0.0, 'alarm_max' : 0.0, 'limit_min' : 0.0, 'limit_max':0.0, 'amount' : 0.0}

        average[sensor['type']]['current'] += sensor['current']
        average[sensor['type']]['alarm_min'] += sensor['alarm_min']
        average[sensor['type']]['alarm_max'] += sensor['alarm_max']
        average[sensor['type']]['limit_min'] += sensor['limit_min']
        average[sensor['type']]['limit_max'] += sensor['limit_max']
        average[sensor['type']]['amount'] += 1.0

      for averagetype in average:
        amount = average[averagetype]['amount']
        del(average[averagetype]['amount'])
        for field in average[averagetype]:
          average[averagetype][field] /= amount

        average[averagetype]['alarm'] = not (average[averagetype]['alarm_min'] <= average[averagetype]['current'] <= average[averagetype]['alarm_max'])
        average[averagetype]['type'] = averagetype
        average[averagetype]['indicator'] = temperature_type if 'temperature' == averagetype[8:] and temperature_type is not None else self.__unit_type(averagetype[8:])

      data = average

#    if temperature_type is not None and temperature_type != terrariumConfig.get_temperature_indicator():
#      if 'C' == temperature_type:
#        pass
#      elif 'F' == temperature_type:
#        pass
#      elif 'K' == temperature_type:
#        pass

    if socket:
      self.__send_message({'type':'sensor_gauge','data':data})
    else:
      return {'sensors' : data}

  def get_sensors_config(self, socket = False):
    return self.get_sensors()

  def set_sensors_config(self, data):
    self.__load_sensors(data)
    return self.config.save_sensors(self.sensors)
  # End sensors part

  # Switches part
  def get_switches(self, parameters = [], socket = False):
    data = []
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    if filter is not None and filter in self.power_switches:
      data.append(self.power_switches[filter].get_data())

    else:
      for switchid in self.power_switches:
        data.append(self.power_switches[switchid].get_data())

    if socket:
      self.__send_message({'type':'switches','data':data})
    else:
      return {'switches' : data}

  def get_switches_config(self, socket = False):
    return self.get_switches()

  def set_switches_config(self, data):
    self.__load_power_switches(data)
    return self.config.save_power_switches(self.power_switches)

  def toggle_power_switch(self,data):
    self.collector.log_switch_data(data)
    self.get_switches(socket=True)
    self.get_power_usage_water_flow(socket=True)

    if self.environment is not None:
      self.environment.update(False)
      self.get_environment(socket=True)

    self.notification.message('switch_toggle_' + ('off' if data['state'] == 0 else 'on'),data)
  # End switches part

  # Doors part
  def get_doors(self, parameters = [], socket = False):
    data = []
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    if filter is not None and filter in self.doors:
      data.append(self.doors[filter].get_data())

    else:
      for doorid in self.doors:
        data.append(self.doors[doorid].get_data())

    if socket:
      self.__send_message({'type':'doors','data':data})
    else:
      return {'doors' : data}

  def get_doors_config(self):
    return self.get_doors()

  def set_doors_config(self, data):
    self.__load_doors(data)
    return self.config.save_doors(self.doors)

  def toggle_door_status(self, data):
    if 'state' in data and 'open' == data['state']:
      self.notification.message('door_toggle_open',data)
    elif 'state' in data and 'closed' == data['state']:
      self.notification.message('door_toggle_closed',data)

    self.collector.log_door_data(data)
    self.get_doors_status(socket=True)
    self.get_doors(socket=True)

  def get_doors_status(self, socket = False):
    data = 'disabled'
    if len(self.doors) > 0:
      data = 'closed' if all(self.doors[doorid].get_status() == terrariumDoor.CLOSED for doorid in self.doors) else 'open'

    if socket:
      self.__send_message({'type':'door_status','data': data})
    else:
      return data

  def is_door_open(self):
    return 'open' == self.get_doors_status()

  def is_door_closed(self):
    return not self.is_door_open()
  # End doors part


  # Calender part
  def get_calendar(self, parameters, **kwargs):
    if 'ical' in parameters:
      return self.calendar.get_ical()

    start = kwargs.get('start')
    if start is None:
      start = datetime.datetime.utcnow() -  datetime.timedelta(days=15)
    else:
      start = datetime.datetime.strptime(start,'%Y-%m-%d')

    end = kwargs.get('end')
    if end is None:
      end = start + datetime.timedelta(days=30)
    else:
      end = datetime.datetime.strptime(end,'%Y-%m-%d')

    data = self.calendar.get_events(start,end)

    events = []
    for event_data in data:
      event = {'id': event_data.uid,
               'title': event_data.summary,
               'description' : event_data.description}

      if terrariumUtils.parse_url(event_data.location):
        event['url'] = event_data.location

      if event_data.all_day:
        event['start'] = event_data.start.strftime('%Y-%m-%d')
        event['end'] = event_data.end.strftime('%Y-%m-%d')
      else:
        event['start'] = event_data.start.strftime('%Y-%m-%dT%H:%M')
        event['end'] = event_data.end.strftime('%Y-%m-%dT%H:%M')

      events.append(event)

    return events

  def create_calendar_event(self, title, message = None, location = None, start = None, stop = None, uid = None):
    if start is None:
      start = datetime.date.today()

    else:
      start = datetime.date.fromtimestamp(int(start))

    if stop is None:
      stop = start

    else:
      stop = datetime.date.fromtimestamp(int(stop))

    self.calendar.create_event(uid,title,message,location,start,stop)

  def replace_hardware_calender_event(self,switch_id,device,reminder_amount,reminder_period):
    # Two events:
    # 1. When it happend
    # 2. Reminder for next time

    current_time = datetime.date.today()
    switch = self.power_switches[switch_id]
    switch.set_last_hardware_replacement()
    self.config.save_power_switch(switch.get_data())
    self.calendar.create_event(switch_id,
                               '{} hardware replacement'.format(switch.get_name()),
                               'Replaced \'{}\' at power switch {}'.format(device,switch.get_name()),
                               None,
                               current_time)

    reminder = None
    try:
      if 'days' == reminder_period:
        reminder = datetime.timedelta(days=int(reminder_amount))
      elif 'weeks' == reminder_period:
        reminder = datetime.timedelta(days=(int(reminder_amount) * 7))
      elif 'months' == reminder_period:
        reminder = datetime.timedelta(days=(int(reminder_amount) * 30))
      elif 'years' == reminder_period:
        reminder = datetime.timedelta(days=(int(reminder_amount) * 365))
    except Exception as ex:
      print(ex)

    if reminder is not None:
      current_time += reminder
      self.calendar.create_event(switch_id,
                                 'Reminder {} hardware replacement'.format(switch.get_name()),
                                 'Replace \'{}\' at power switch {}'.format(device,switch.get_name()),
                                 None,
                                 current_time)

  # End Calendar part

  # Webcams part
  def get_webcams(self, parameters = [], socket = False):
    data = []
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    if filter is not None and filter in self.webcams:
      archive = len(parameters) > 1 and 'archive' == parameters[1]
      data.append(self.webcams[filter].get_data(parameters[2:]))

    else:
      for webcamid in self.webcams:
        data.append(self.webcams[webcamid].get_data())

    if socket:
      self.__send_message({'type':'webcams','data':data})
    else:
      return {'webcams' : data}

  def get_webcams_config(self):
    return self.get_webcams()

  def set_webcams_config(self, data):
    self.__load_webcams(data)
    return self.config.save_webcams(self.webcams)
  # End webcams part

  # Start audio files part
  def reload_audio_files(self):
    self.__audio_player.reload_audio_files()

  def upload_audio_file(self):
    pass

  def delete_audio_file(self,audiofileid):
    audio_files = self.__audio_player.get_audio_files()
    if audiofileid in audio_files:
      if audio_files[audiofileid].delete():
        self.reload_audio_files()
        return True

    return False

  def get_audio_files(self, parameters = []):
    audio_files = self.__audio_player.get_audio_files()
    data = []
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    if filter is not None and filter in audio_files:
      data.append(audio_files[filter].get_data())

    else:
      for audiofileid in audio_files:
        data.append(audio_files[audiofileid].get_data())

    return {'audiofiles' : data}

  def get_audio_playlists(self, parameters = [], socket = False):
    playlists = self.__audio_player.get_playlists()
    data = []
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    if filter is not None and filter in playlists:
      data.append(playlists[filter])

    else:
      for playlist_id in playlists:
        data.append(playlists[playlist_id].get_data())

    if socket:
      self.__send_message({'type':'playlists','data': data})
    else:
      return {'playlists' : data}

  def get_audio_playlists_config(self):
    return self.get_audio_playlists()

  def set_audio_playlists_config(self, data):
    self.__audio_player.reload_playlists(data)
    return self.config.save_audio_playlists(self.__audio_player.get_playlists())

  def get_audio_playing(self,socket = False):
    data = self.__audio_player.get_current_state()

    if socket:
      self.__send_message({'type':'player_indicator','data': data})
    else:
      return data

  def start_audio_player(self):
    pass

  def stop_audio_player(self):
    pass

  def audio_player_volume_up(self):
    self.__audio_player.volume_up()
    self.get_audio_playing(True)

  def audio_player_volume_down(self):
    self.__audio_player.volume_down()
    self.get_audio_playing(True)

  # End audio part

  # Environment part
  def get_environment(self, parameters = [], socket = False):
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    data = self.environment.get_data()

    if filter is not None and filter in data:
      data = { filter : data[filter]}

    if socket:
      self.__send_message({'type':'environment','data':data})
    else:
      return { 'environment' : data }

  def get_environment_config(self):
    return self.environment.get_config()

  def set_environment_config(self,data):
    self.environment.load_environment(data)
    return self.config.save_environment(self.environment.get_config())
  # End Environment part

  # Profile part
  def get_profile_config(self):
    data = self.config.get_profile()
    if os.path.isfile('description.txt'):
      with open('description.txt', 'r') as description_file:
        data['description'] = description_file.read()

    return data

  def get_profile(self):
    return self.get_profile_config()

  def get_profile_name(self):
    return self.get_profile_config()['name']

  def get_profile_image(self):
    return self.get_profile_config()['image']

  def set_profile(self,data,files):
    if 'profile_image' in files:
      profile_image = files.get('profile_image')
      name, ext = os.path.splitext(profile_image.filename)
      if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

      profile_image.save('static/images/')
      data['image'] = 'static/images/' + profile_image.filename

    if 'description' in data:
      with open('description.txt', 'wb') as description_file:
        description_file.write(data['description'].encode())
        del(data['description'])

    update_ok = self.config.save_profile(data)
    if update_ok:
      self.notification.set_profile_image(self.get_profile_image())
    return update_ok
  # End profile part


  # Notifications part
  def get_notifications_config(self):
    return self.notification.get_config()

  def set_notifications(self,data):
    return self.notification.set_config(data)
  # End notifications part

  # System functions part
  def authenticate(self,username, password):
    return password and (username in self.authentication) and self.authentication[username] == password

  def set_authentication(self, username, password):
    config = self.config.get_system()
    self.authentication = { username : password }

  def subscribe(self,queue):
    self.subscribed_queues.append(queue)
    self.__send_message({'type':'dashboard_online', 'data':True})

  def get_system_stats(self, socket = False):
    memory = psutil.virtual_memory()
    uptime = self.get_uptime()
    disk = psutil.disk_usage('/')

    cpu_temp = -1
    with open('/sys/class/thermal/thermal_zone0/temp') as temperature:
      cpu_temp = float(temperature.read()) / 1000.0

    data = {'memory' : {'total' : memory.total,
                        'used' : memory.total - memory.available,
                        'free' : memory.available},
            'disk' : {'total' : disk.total,
                        'used' : disk.used,
                        'free' : disk.free},
            'load' : {'load1' : uptime['load'][0],
                      'load5' : uptime['load'][1],
                      'load15' : uptime['load'][2]},
            'uptime' : uptime['uptime'],
            'cores' : psutil.cpu_count(),
            'temperature' : cpu_temp,
            'external_calendar_url': self.config.get_external_calender_url()}

    indicator = self.__unit_type('temperature').lower()
    if 'f' == indicator:
      data['temperature'] = terrariumUtils.to_fahrenheit(data['temperature'])
    elif 'k' == indicator:
      data['temperature'] = terrariumUtils.to_kelvin(data['temperature'])

    if socket:
      gauge_data = {'system_load'        : {'current' : data['load']['load1'] * 100, 'alarm_min' : 0, 'alarm_max': 80, 'limit_min' : 0, 'limit_max': 100, 'cores' : data['cores']},
                    'system_temperature' : {'current' : data['temperature'], 'alarm_min' : 30, 'alarm_max': 60, 'limit_min' : 0, 'limit_max': 80},
                    'system_memory'      : {'current' : data['memory']['used'], 'alarm_min' : data['memory']['total'] * 0.1, 'alarm_max': data['memory']['total'] * 0.9, 'limit_min' : 0, 'limit_max': data['memory']['total']},
                    'system_disk'        : {'current' : data['disk']['used'], 'alarm_min' : data['disk']['total'] * 0.1, 'alarm_max': data['disk']['total'] * 0.9, 'limit_min' : 0, 'limit_max': data['disk']['total']}}

      gauge_data['system_load']['alarm'] = not(gauge_data['system_load']['alarm_min'] <= gauge_data['system_load']['current'] / data['cores'] <= gauge_data['system_load']['alarm_max'])
      gauge_data['system_temperature']['alarm'] = not(gauge_data['system_temperature']['alarm_min'] <= gauge_data['system_temperature']['current'] <= gauge_data['system_temperature']['alarm_max'])
      gauge_data['system_memory']['alarm'] = not(gauge_data['system_memory']['alarm_min'] <= gauge_data['system_memory']['current'] <= gauge_data['system_memory']['alarm_max'])
      gauge_data['system_disk']['alarm'] = not(gauge_data['system_disk']['alarm_min'] <= gauge_data['system_disk']['current'] <= gauge_data['system_disk']['alarm_max'])

      self.__send_message({'type':'sensor_gauge','data':gauge_data})
    else:
      return data

  def get_uptime(self, socket = False):
    data = {'uptime' : uptime.uptime(),
            'timestamp' : int(time.time()),
            'load' : os.getloadavg(),
            'cores' : psutil.cpu_count()}

    if self.weather is not None:
      data['day'] = self.weather.is_day()

    if socket:
      self.__send_message({'type':'uptime','data':data})
    else:
      return data

  def get_power_usage_water_flow(self, socket = False):
    data = self.__get_current_power_usage_water_flow()
    totaldata = self.__get_total_power_usage_water_flow()

    data['power']['total'] = totaldata['power_wattage']['wattage']
    data['power']['duration'] = totaldata['power_wattage']['duration']
    data['power']['price'] = self.config.get_power_price() * (totaldata['power_wattage']['wattage'] / 3600.0 / 1000.0)

    data['water']['total'] = totaldata['water_flow']['water']
    data['water']['duration'] = totaldata['water_flow']['duration']
    data['water']['price'] = self.config.get_water_price() * (totaldata['water_flow']['water'] / 1000.0)

    if socket:
      self.__send_message({'type':'power_usage_water_flow','data':data});
    else:
      return data

  def get_temperature_indicator(self):
    return self.__unit_type('temperature')

  def set_temperature_indicator(self,value):
    self.__units['temperature'] = value

  def get_windspeed_indicator(self):
    return self.__unit_type('windspeed')

  def set_windspeed_indicator(self,value):
    self.__units['windspeed'] = value

  def get_volume_indicator(self):
    return self.__unit_type('volume')

  def set_volume_indicator(self,value):
    self.__units['volume'] = value

  def get_humidity_indicator(self):
    return self.__unit_type('humidity')

  def get_moisture_indicator(self):
    return self.__unit_type('moisture')

  def get_distance_indicator(self):
    return self.__unit_type('distance')

  def set_distance_indicator(self,value):
    self.__units['distance'] = value

  def get_horizontal_graph_legend(self):
    config_data = self.config.get_system()
    if 'horizontal_graph_legend' not in config_data:
      config_data['horizontal_graph_legend'] = False;

    return terrariumUtils.is_true(config_data['horizontal_graph_legend'])

  def get_hide_environment_on_dashboard(self):
    config_data = self.config.get_system()
    if 'hide_environment_on_dashboard' not in config_data:
      config_data['hide_environment_on_dashboard'] = False;

    return terrariumUtils.is_true(config_data['hide_environment_on_dashboard'])

  def get_show_gauge_overview(self):
    config_data = self.config.get_system()
    if 'sensor_gauge_overview' not in config_data:
      config_data['sensor_gauge_overview'] = False;

    return terrariumUtils.is_true(config_data['sensor_gauge_overview'])

  def get_graph_smooth_value(self):
    config_data = self.config.get_system()
    if 'graph_smooth_value' not in config_data:
      # Default 'no' smoothing
      config_data['graph_smooth_value'] = 0;

    return config_data['graph_smooth_value'] * 1

  def get_graph_show_min_max_gauge(self):
    config_data = self.config.get_system()
    if 'graph_show_min_max_gauge' not in config_data:
      config_data['graph_show_min_max_gauge'] = False;

    return terrariumUtils.is_true(config_data['graph_show_min_max_gauge'])
  # End system functions part

  # API Config calls
  def get_config(self, part = None):
    data = {}
    if 'system' == part or part is None:
      data.update(self.get_system_config())

    if 'weather' == part or part is None:
      data.update(self.get_weather_config())

    if 'switches' == part or part is None:
      data.update(self.get_switches_config())

    if 'sensors' == part or part is None:
      data.update(self.get_sensors_config())
      data.update({'hardware' : terrariumSensor.valid_hardware_types2()})

    if 'webcams' == part or part is None:
      data.update(self.get_webcams_config())

    if 'doors' == part or part is None:
      data.update(self.get_doors_config())

    if 'audio' == part or part is None:
      data.update(self.get_audio_playlists_config())

    if 'profile' == part or part is None:
      data.update(self.get_profile_config())

    if 'environment' == part or part is None:
      data.update(self.get_environment_config())

    if 'notifications' == part or part is None:
      data.update({'notifications' : self.get_notifications_config()})

    return data

  def set_config(self,part,data,files = None):
    update_ok = False
    if 'weather' == part:
      update_ok = self.set_weather_config(data)

    elif 'switches' == part:
      update_ok = self.set_switches_config(data)

    elif 'sensors' == part:
      update_ok = self.set_sensors_config(data)

    elif 'webcams' == part:
      update_ok = self.set_webcams_config(data)

    elif 'doors' == part:
      update_ok = self.set_doors_config(data)

    elif 'audio' == part:
      update_ok = self.set_audio_playlists_config(data)

    elif 'environment' == part:
      update_ok = self.set_environment_config(data)

    elif 'profile' == part:
      update_ok = self.set_profile(data,files)

    elif 'notifications' == part:
      update_ok = self.set_notifications(data)

    elif 'system' == part:
      if 'new_password' in data and data['new_password'] != '' and 'cur_password' in data and data['cur_password'] != '' and data['new_password'] != data['cur_password']:
        # check if existing password is correct
        existing_password =  self.config.get_system()['password']
        if existing_password == data['cur_password']:
          data['password'] = data['new_password']
          del(data['new_password'])
          del(data['cur_password'])
        else:
          return False

      update_ok = self.set_system_config(data)
      if update_ok:
        # Update config settings
        self.set_weather_config({'location' : data['location']})
        self.pi_power_wattage = float(self.config.get_pi_power_wattage())
        self.set_authentication(self.config.get_admin(),self.config.get_password())

        self.set_temperature_indicator(self.config.get_temperature_indicator())
        self.set_distance_indicator(self.config.get_distance_indicator())
        self.set_windspeed_indicator(self.config.get_windspeed_indicator())
        self.set_volume_indicator(self.config.get_volume_indicator())

    return update_ok

  def get_system_config(self):
    data = self.config.get_system()
    data['windspeed_indicator'] = self.get_windspeed_indicator()
    data.update(self.config.get_meross_cloud())

    del(data['password'])
    return data

  def set_system_config(self,data):
    return self.config.set_system(data) and self.config.set_meross_cloud(data)

  # End system functions part

  # Histroy part (Collector)
  def get_history(self, parameters = [], socket = False):
    data = {}
    if len(parameters) == 0:
      data = {'history' : 'ERROR, select a history type'}
    else:
      exclude_ids = None
      # We exclude Chirp light sensors for average calculations as they are less reliable
      if 'sensors' in parameters and 'average' in parameters:
        exclude_ids = []
        for sensorid in self.sensors:
          if self.sensors[sensorid].get_exclude_avg() or ('chirp' == self.sensors[sensorid].get_type() and 'light' == self.sensors[sensorid].get_sensor_type()):
            exclude_ids.append(self.sensors[sensorid].get_id())

      stoptime = None
      if 'switches' in parameters and 'lr' in parameters:
        stoptime = int(datetime.datetime.strptime(self.power_switches[parameters[1]].get_last_hardware_replacement(),'%Y-%m-%d').strftime('%s'))

      data = self.collector.get_history(parameters=parameters,stoptime=stoptime,exclude_ids=exclude_ids)

    if socket:
      self.__send_message({'type':'history_graph','data': data})
    else:
      return data
  # End Histroy part (Collector)
