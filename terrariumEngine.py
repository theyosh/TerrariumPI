# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import RPi.GPIO as GPIO
#GPIO.setwarnings(False)
## set GPIO mode to BCM. This is needed to support analog devices through gpiozero
logger.debug('Setting terrariumPI GPIO Mode to %s' % (GPIO.BCM,))
GPIO.setmode(GPIO.BCM)
logger.debug('Done setting terrariumPI GPIO Mode to %s' % (GPIO.BCM,))

import thread
import time
import uptime
import os
import psutil
import subprocess
import re
from hashlib import md5

from terrariumConfig import terrariumConfig
from terrariumWeather import terrariumWeather
from terrariumSensor import terrariumSensor
from terrariumSwitch import terrariumSwitch
from terrariumDoor import terrariumDoor
from terrariumWebcam import terrariumWebcam
from terrariumAudio import terrariumAudioPlayer
from terrariumCollector import terrariumCollector
from terrariumEnvironment import terrariumEnvironment
from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumEngine(object):

  LOOP_TIMEOUT = 30

  def __init__(self):

    # Default system units
    self.__units = {'temperature' : 'C',
                    'distance'    : 'cm',
                    'humidity'    : '%',
                    'moisture'    : '',
                    'conductivity': 'mS',
                    'ph'          : 'Ph'}

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

    logger.info('Setting terrariumPI authentication')
    self.set_authentication(self.config.get_admin(),self.config.get_password())
    logger.info('Done setting terrariumPI authentication')

    # Load data collector for historical data
    logger.info('Loading terrariumPI collector')
    self.collector = terrariumCollector(self.config.get_system()['version'])
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

    # Load Weather part
    logger.info('Loading terrariumPI weather data')
    self.weather = terrariumWeather(self.config.get_weather_location(),
                                    self.config.get_weather_windspeed(),
                                    self.__unit_type,
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
    self.environment = terrariumEnvironment(self.sensors, self.power_switches, self.weather, self.is_door_open, self.config.get_environment)
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
    thread.start_new_thread(self.__engine_loop, ())
    thread.start_new_thread(self.__log_tail, ())
    logger.info('TerrariumPI engine is running')

  # Private/internal functions
  def __load_sensors(self,data = None):
    # Load Sensors, with ID as index
    starttime = time.time()
    reloading = data is not None

    logger.info('%s terrariumPI sensors' % ('Reloading' if reloading else 'Loading',))

    sensor_config = (self.config.get_sensors() if not reloading else data)
    if not reloading:
      self.sensors = {}

    seen_sensors = []
    for sensor in terrariumSensor.scan(self.config.get_owfs_port(), self.__unit_type):
      self.sensors[sensor.get_id()] = sensor

    for sensordata in sensor_config:
      if sensordata['id'] is None or sensordata['id'] == 'None' or sensordata['id'] not in self.sensors:
        # New sensor (add)
        sensor = terrariumSensor( None,
                                 sensordata['hardwaretype'],
                                 sensordata['type'],
                                 sensordata['address'],
                                 sensordata['name'],
                                 self.__unit_type)

        self.sensors[sensor.get_id()] = sensor
      else:
        # Existing sensor
        sensor = self.sensors[sensordata['id']]
        # Should not be able to change setings
        #sensor.set_hardware_type(sensordata['hardwaretype'])
        sensor.set_type(sensordata['type'],self.__unit_type)
        sensor.set_address(sensordata['address'])
        sensor.set_name(sensordata['name'])

      sensor.set_alarm_min(sensordata['alarm_min'])
      sensor.set_alarm_max(sensordata['alarm_max'])
      sensor.set_limit_min(sensordata['limit_min'])
      sensor.set_limit_max(sensordata['limit_max'])

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
    reloading = data is not None

    logger.info('%s terrariumPI switches' % ('Reloading' if reloading else 'Loading',))

    switch_config = (self.config.get_power_switches() if not reloading else data)
    if not reloading:
      self.power_switches = {}

    seen_switches = []
    for switchdata in switch_config:
      if switchdata['id'] is None or switchdata['id'] == 'None' or switchdata['id'] not in self.power_switches:
        # New switch (add)
        power_switch = terrariumSwitch(None,
                                       switchdata['hardwaretype'],
                                       switchdata['address'],
                                       switchdata['name'],
                                       switchdata['power_wattage'],
                                       switchdata['water_flow'],
                                       callback=self.toggle_switch)
        self.power_switches[power_switch.get_id()] = power_switch
      else:
        # Existing switch
        power_switch = self.power_switches[switchdata['id']]
        # Should not be able to change setings
        #power_switch.set_hardware_type(switchdata['hardwaretype'])
        power_switch.set_address(switchdata['address'])
        power_switch.set_name(switchdata['name'])
        power_switch.set_power_wattage(switchdata['power_wattage'])
        power_switch.set_water_flow(switchdata['water_flow'])

      if 'dimmer_duration' in switchdata and switchdata['dimmer_duration'] is not None:
        power_switch.set_dimmer_duration(switchdata['dimmer_duration'])
      if 'dimmer_on_duration' in switchdata and switchdata['dimmer_on_duration'] is not None:
        power_switch.set_dimmer_on_duration(switchdata['dimmer_on_duration'])
      if 'dimmer_on_percentage' in switchdata and switchdata['dimmer_on_percentage'] is not None:
        power_switch.set_dimmer_on_percentage(switchdata['dimmer_on_percentage'])
      if 'dimmer_off_duration' in switchdata and switchdata['dimmer_off_duration'] is not None:
        power_switch.set_dimmer_off_duration(switchdata['dimmer_off_duration'])
      if 'dimmer_off_percentage' in switchdata and switchdata['dimmer_off_percentage'] is not None:
        power_switch.set_dimmer_off_percentage(switchdata['dimmer_off_percentage'])

      if 'timer_enabled' in switchdata and switchdata['timer_enabled'] is not None:
        power_switch.set_timer_enabled(switchdata['timer_enabled'])
      if 'timer_start' in switchdata and switchdata['timer_start'] is not None:
        power_switch.set_timer_start(switchdata['timer_start'])
      if 'timer_stop' in switchdata and switchdata['timer_stop'] is not None:
        power_switch.set_timer_stop(switchdata['timer_stop'])
      if 'timer_on_duration' in switchdata and switchdata['timer_on_duration'] is not None:
        power_switch.set_timer_on_duration(switchdata['timer_on_duration'])
      if 'timer_off_duration' in switchdata and switchdata['timer_off_duration'] is not None:
        power_switch.set_timer_off_duration(switchdata['timer_off_duration'])

      seen_switches.append(power_switch.get_id())

    if reloading:
      for power_switch_id in set(self.power_switches) - set(seen_switches):
        # clean up old deleted switches
        del(self.power_switches[power_switch_id])

      self.environment.set_power_switches(self.power_switches)

    logger.info('Done %s terrariumPI switches. Found %d switches in %.3f seconds' % ('reloading' if reloading else 'loading',
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
        # New switch (add)
        width = 640
        height = 480
        archive = False
        if 'resolution_width' in webcamdata and 'resolution_height' in webcamdata:
          width = webcamdata['resolution_width']
          height = webcamdata['resolution_height']

        if 'archive' in webcamdata:
          archive = webcamdata['archive']

        webcam = terrariumWebcam(None,
                                 webcamdata['location'],
                                 webcamdata['name'],
                                 webcamdata['rotation'],
                                 width,height,
                                 archive)
        self.webcams[webcam.get_id()] = webcam
      else:
        # Existing switch
        webcam = self.webcams[webcamdata['id']]
        # Should not be able to change setings
        #door.set_hardware_type(doordata['hardwaretype'])
        webcam.set_location(webcamdata['location'])
        webcam.set_name(webcamdata['name'])

      webcam.set_rotation(webcamdata['rotation'])

      if 'resolution_width' in webcamdata and 'resolution_height' in webcamdata:
        webcam.set_resolution(webcamdata['resolution_width'],webcamdata['resolution_height'])

      if 'archive' in webcamdata:
        webcam.set_archive(webcamdata['archive'])

      seen_webcams.append(webcam.get_id())

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
      data['power']['current'] += self.power_switches[switchid].get_current_power_wattage() if self.power_switches[switchid].is_on() else 0.0
      data['power']['max'] += self.power_switches[switchid].get_power_wattage()

      data['water']['current'] += self.power_switches[switchid].get_current_water_flow() if self.power_switches[switchid].is_on() else 0.0
      data['water']['max'] += self.power_switches[switchid].get_water_flow()

    return data

  def __get_total_power_usage_water_flow(self):
    totals = {'power_wattage' : {'duration' : int(time.time()) , 'wattage' : 0.0},
              'water_flow'    : {'duration' : int(time.time()) , 'water'   : 0.0}}

    history = self.collector.get_history(['switches'],int(time.time()),0)

    if 'switches' not in history:
      return totals

    for switchid in history['switches']:
      totals['power_wattage']['wattage'] += history['switches'][switchid]['totals']['power_wattage']['wattage']
      totals['water_flow']['water'] += history['switches'][switchid]['totals']['water_flow']['water']

      if history['switches'][switchid]['power_wattage'][0][0] / 1000.0 < totals['power_wattage']['duration']:
        totals['power_wattage']['duration'] = history['switches'][switchid]['power_wattage'][0][0] / 1000.0

      if history['switches'][switchid]['water_flow'][0][0] / 1000.0 < totals['water_flow']['duration']:
        totals['water_flow']['duration'] = history['switches'][switchid]['water_flow'][0][0] / 1000.0

    totals['power_wattage']['duration'] = max(self.get_uptime()['uptime'],int(time.time()) - totals['power_wattage']['duration'],int(time.time()) - totals['water_flow']['duration'])
    totals['water_flow']['duration'] = totals['power_wattage']['duration']

    totals['power_wattage']['wattage'] += totals['power_wattage']['duration'] * self.pi_power_wattage

    return totals

  def __engine_loop(self):
    logger.info('Start terrariumPI engine')
    while self.__running:
      starttime = time.time()

      try:
        # Update weather
        self.weather.update()
        weather_data = self.weather.get_data()
        if 'hour_forecast' in weather_data and len(weather_data['hour_forecast']) > 0:
          self.collector.log_weather_data(weather_data['hour_forecast'][0])

        # Update sensors
        for sensorid in self.sensors:
          # Update the current sensor.
          self.sensors[sensorid].update()
          # Save new data to database
          self.collector.log_sensor_data(self.sensors[sensorid].get_data())
          # Websocket callback
          self.get_sensors([sensorid],socket=True)
          # Make time for other web request
          sleep(0.1)

        # Get the current average temperatures
        average_data = self.get_sensors(['average'])['sensors']

        # Websocket callback
        self.__send_message({'type':'sensor_gauge','data':average_data})

        # Update (remote) power switches
        for power_switch_id in self.power_switches:
          # Update timer trigger if activated
          self.power_switches[power_switch_id].timer()
          # Update the current sensor.
          self.power_switches[power_switch_id].update()
          # Make time for other web request
          sleep(0.1)

        # Websocket messages back
        self.get_uptime(socket=True)
        self.get_power_usage_water_flow(socket=True)
        self.get_environment(socket=True)
        self.get_audio_playing(socket=True)

        # Log system stats
        self.collector.log_system_data(self.get_system_stats())
        self.get_system_stats(socket=True)

        for webcamid in self.webcams:
          self.webcams[webcamid].update()
          sleep(0.1)

      except Exception, err:
        print err

      duration = time.time() - starttime
      if duration < terrariumEngine.LOOP_TIMEOUT:
        logger.info('Update done in %.5f seconds. Waiting for %.5f seconds for next round' % (duration,terrariumEngine.LOOP_TIMEOUT - duration))
        sleep(terrariumEngine.LOOP_TIMEOUT - duration) # TODO: Config setting
      else:
        logger.warning('Updating took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumEngine.LOOP_TIMEOUT,terrariumEngine.LOOP_TIMEOUT))

  def __send_message(self,message):
    for queue in self.subscribed_queues:
      queue.put(message)

  def __log_tail(self):
    logger.info('Start terrariumPI engine log')
    logtail = subprocess.Popen(['tail','-F','log/terrariumpi.log'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for line in logtail.stdout:
      self.__send_message({'type':'logtail','data':line.strip()})

  def __unit_type(self,unittype):
    if unittype in self.__units:
      return self.__units[unittype]

    return None

  def stop(self):
    self.environment.stop()
    for sensorid in self.sensors:
      self.sensors[sensorid].stop()

    for power_switch_id in self.power_switches:
      self.power_switches[power_switch_id].stop()

    self.collector.stop()
    self.__running = False
    logger.info('Shutdown engine')
  # End private/internal functions

  # Weather part
  def set_weather_config(self,data):
    update_ok = self.config.save_weather(data)
    if update_ok:
      self.weather.set_source(self.config.get_weather_location())
      self.weather.set_windspeed_indicator(self.config.get_weather_windspeed())

    return update_ok

  def get_weather_config(self):
    return self.weather.get_config()

  def get_weather(self, parameters = [], socket = False):
    data = self.weather.get_data()
    self.environment.update_timing()

    if socket:
      self.__send_message({'type':'update_weather','data':data})
    else:
      return data
  # End weather part

  # Sensors part
  def get_sensors(self, parameters = [], socket = False):
    data = []
    filtertype = None
    if len(parameters) > 0 and parameters[0] is not None:
      filtertype = parameters[0]

    # Filter is based on sensorid
    if filtertype is not None and filtertype in self.sensors:
      data.append(self.sensors[filtertype].get_data())

    else:
      for sensorid in self.sensors:
        # Filter based on sensor type
        if filtertype is None or filtertype == 'average' or filtertype == self.sensors[sensorid].get_type():
          data.append(self.sensors[sensorid].get_data())

    if 'average' == filtertype or len(parameters) == 2 and parameters[1] == 'average':
      average = {}
      for sensor in data:
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
        average[averagetype]['indicator'] = self.__unit_type(averagetype[8:])

      data = average

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

  def toggle_switch(self,data):
    self.collector.log_switch_data(data)
    self.get_switches(socket=True)
    self.get_power_usage_water_flow(socket=True)

    if self.environment is not None:
      self.get_environment(socket=True)
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

  # Webcams part
  def get_webcams(self, parameters = [], socket = False):
    data = []
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    if filter is not None and filter in self.webcams:
      archive = len(parameters) > 1 and 'archive' == parameters[1]
      data.append(self.webcams[filter].get_data(archive))

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

    data = self.get_sensors(['average'])['sensors']
    data['light']     = self.environment.get_light_state()
    data['sprayer']   = self.environment.get_sprayer_state()
    data['heater']    = self.environment.get_heater_state()
    data['cooler']    = self.environment.get_cooler_state()
    data['watertank'] = self.environment.get_watertank_state()

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
    if 'profile_image' in files.keys():
      profile_image = files.get('profile_image')
      name, ext = os.path.splitext(profile_image.filename)
      if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

      profile_image.save('static/images/')
      data['image'] = 'static/images/' + profile_image.filename

    if 'description' in data:
      with open('description.txt', 'wb') as description_file:
        description_file.write(data['description'])
        del(data['description'])

    update_ok = self.config.save_profile(data)
    return update_ok
  # End profile part

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
            'day' : self.weather.is_day(),
            'load' : os.getloadavg(),
            'cores' : psutil.cpu_count()}

    if socket:
      self.__send_message({'type':'uptime','data':data})
    else:
      return data

  def get_power_usage_water_flow(self, socket = False):
    data = self.__get_current_power_usage_water_flow()
    totaldata = self.__get_total_power_usage_water_flow()

    data['power']['total'] = totaldata['power_wattage']['wattage']
    data['power']['duration'] = totaldata['power_wattage']['duration']
    data['power']['price'] = self.config.get_power_price() * (totaldata['power_wattage']['wattage'] / (3600.0 * 1000.0))

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

      # Update weather data
      self.set_weather_config({'location' : data['location'], 'windspeed' : data['windspeed']})

      update_ok = self.set_system_config(data)
      if update_ok:
        # Update config settings
        self.pi_power_wattage = float(self.config.get_pi_power_wattage())
        self.set_authentication(self.config.get_admin(),self.config.get_password())

        self.set_temperature_indicator(self.config.get_temperature_indicator())
        self.set_distance_indicator(self.config.get_distance_indicator())

        #self.temperature_indicator = self.config.get_temperature_indicator()

    return update_ok

  def get_system_config(self):
    data = self.config.get_system()
    del(data['password'])
    return data

  def set_system_config(self,data):
    return self.config.set_system(data)

  # End system functions part

  # Histroy part (Collector)
  def get_history(self, parameters = [], socket = False):
    data = {}
    if len(parameters) == 0:
      data = {'history' : 'ERROR, select a history type'}
    else:
      data = self.collector.get_history(parameters)

    if socket:
      self.__send_message({'type':'history_graph','data': data})
    else:
      return data
  # End Histroy part (Collector)
