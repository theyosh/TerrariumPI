# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import thread
import time
import uptime
import os
import psutil

from terrariumConfig import terrariumConfig

from terrariumWeather import terrariumWeather
from terrariumSensor import terrariumSensor
from terrariumSwitch import terrariumSwitch
from terrariumDoor import terrariumDoor
from terrariumWebcam import terrariumWebcam

from terrariumCollector import terrariumCollector
from terrariumEnvironment import terrariumEnvironment

from gevent import monkey, sleep
monkey.patch_all()

class terrariumEngine():

  LOOP_TIMEOUT = 30

  def __init__(self):
    # List of queues for websocket communication
    self.subscribed_queues = []
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
    self.collector = terrariumCollector()
    logger.info('Done loading terrariumPI collector')

    # Set the Pi power usage (including usb devices directly on the PI)
    logger.info('Loading terrariumPI PI power setting')
    self.pi_power_wattage = float(self.config.get_pi_power_wattage())
    logger.info('Done loading terrariumPI PI power setting')

    # Set the system temperature indicator
    logger.info('Loading terrariumPI PI temperature indicator')
    self.temperature_indicator = self.config.get_temperature_indicator()

    logger.info('Done loading terrariumPI PI temperature indicator')

    # Load Weather part
    logger.info('Loading terrariumPI weather data')
    self.weather = terrariumWeather(self.config.get_weather_location(),
                                    self.config.get_weather_windspeed(),
                                    self.get_temperature_indicator,
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
    self.environment = terrariumEnvironment(self.sensors, self.power_switches, self.weather, self.door_status, self.config)
    logger.debug('Done loading terrariumPI environment system')

    # Load webcams from config
    self.__load_webcams();

    # Start system update loop
    logger.info('Start terrariumPI engine')
    thread.start_new_thread(self.__engine_loop, ())

  # Private/internal functions
  def __load_sensors(self,reloading = False):
    # Load Sensors, with ID as index
    starttime = time.time()
    logger.info('%s terrariumPI temperature/humidity sensors' % ('Reloading' if reloading else 'Loading'),)
    self.sensors = {}
    for sensor in terrariumSensor.scan(self.config.get_owfs_port(), self.config.get_sensors(), self.get_temperature_indicator):
      self.sensors[sensor.get_id()] = sensor

    if reloading:
      self.environment.set_sensors(self.sensors)

    logger.info('Done %s terrariumPI temperature/humidity sensors. Found %d sensors in %.3f seconds' % ('reloading' if reloading else 'loading',
                                                                                                        len(self.sensors),
                                                                                                        time.time()-starttime))

  def __load_power_switches(self,reloading = False):
    # Load Switches, with ID as index
    starttime = time.time()
    logger.info('%s terrariumPI switches' % ('Reloading' if reloading else 'Loading',))
    switch_config = self.config.get_power_switches()
    if not reloading:
      self.power_switches = {}

    seen_switches = []
    for power_switch_config in switch_config:
      power_switch_id = switch_config[power_switch_config]['id']
      seen_switches.append(power_switch_id)
      if not power_switch_id in self.power_switches:
        # Add new switch
        power_switch = terrariumSwitch(switch_config[power_switch_config]['id'],
                                       switch_config[power_switch_config]['hardwaretype'],
                                       switch_config[power_switch_config]['address'],
                                       callback=self.toggle_switch)
        power_switch_id = power_switch.get_id()
        self.power_switches[power_switch_id] = power_switch

      # Update switch
      self.power_switches[power_switch_id].set_name(switch_config[power_switch_config]['name'])
      self.power_switches[power_switch_id].set_power_wattage(switch_config[power_switch_config]['power_wattage'])
      self.power_switches[power_switch_id].set_water_flow(switch_config[power_switch_config]['water_flow'])

      if 'dimmer_duration' in switch_config[power_switch_config]:
        self.power_switches[power_switch_id].set_dimmer_duration(switch_config[power_switch_config]['dimmer_duration'])
      if 'dimmer_on_duration' in switch_config[power_switch_config]:
        self.power_switches[power_switch_id].set_dimmer_on_duration(switch_config[power_switch_config]['dimmer_on_duration'])
      if 'dimmer_on_percentage' in switch_config[power_switch_config]:
        self.power_switches[power_switch_id].set_dimmer_on_percentage(switch_config[power_switch_config]['dimmer_on_percentage'])
      if 'dimmer_off_duration' in switch_config[power_switch_config]:
        self.power_switches[power_switch_id].set_dimmer_off_duration(switch_config[power_switch_config]['dimmer_off_duration'])
      if 'dimmer_off_percentage' in switch_config[power_switch_config]:
        self.power_switches[power_switch_id].set_dimmer_off_percentage(switch_config[power_switch_config]['dimmer_off_percentage'])

    for power_switch_id in set(self.power_switches) - set(seen_switches):
      # clean up old deleted switches
      del(self.power_switches[power_switch_id])

    if reloading:
      self.environment.set_power_switches(self.power_switches)

    logger.info('Done %s terrariumPI switches. Found %d switches in %.3f seconds' % ('reloading' if reloading else 'loading',
                                                                                      len(self.power_switches),
                                                                                      time.time()-starttime))

  def __load_doors(self, reloading = False):
    # Load Doors, with ID as index
    starttime = time.time()
    logger.info('%s terrariumPI doors' % ('Reloading' if reloading else 'Loading',))
    doors_config = self.config.get_doors()
    self.doors = {}
    for door_id in doors_config:
      door = terrariumDoor(
        doors_config[door_id]['id'],
        doors_config[door_id]['hardwaretype'],
        doors_config[door_id]['address'],
        doors_config[door_id]['name'],
        self.toggle_door_status
      )
      self.doors[door.get_id()] = door

      if not reloading:
        self.toggle_door_status(door.get_data())

    logger.info('Done %s terrariumPI doors. Found %d doors in %.3f seconds' % ('reloading' if reloading else 'loading',
                                                                                len(self.doors),
                                                                                time.time()-starttime))

  def __load_webcams(self, reloading = False):
    # Load Webcams, with ID as index
    starttime = time.time()
    logger.info('%s terrariumPI webcams' % ('Reloading' if reloading else 'Loading',))
    webcams_config = self.config.get_webcams()
    self.webcams = {}
    for webcam_id in webcams_config:
      webcam = terrariumWebcam(
        webcams_config[webcam_id]['id'],
        webcams_config[webcam_id]['location'],
        webcams_config[webcam_id]['name'],
        webcams_config[webcam_id]['rotation']
      )
      self.webcams[webcam.get_id()] = webcam

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
    while True:
      starttime = time.time()

      # Update weather
      self.weather.update()
      self.collector.log_weather_data(self.weather.get_data()['hour_forecast'][0])

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

      # Websocket messages back
      self.get_uptime(socket=True)
      self.get_power_usage_water_flow(socket=True)
      self.get_environment(socket=True)

      # Log system stats
      self.collector.log_system_data(self.get_system_stats())
      self.get_system_stats(socket=True)

      for webcamid in self.webcams:
        self.webcams[webcamid].update()
        sleep(0.2)

      duration = time.time() - starttime
      if duration < terrariumEngine.LOOP_TIMEOUT:
        logger.info('Engine loop done in %.5f seconds. Waiting for %.5f seconds for next round' % (duration,terrariumEngine.LOOP_TIMEOUT - duration))
        sleep(terrariumEngine.LOOP_TIMEOUT - duration) # TODO: Config setting
      else:
        logger.warning('Engine took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumEngine.LOOP_TIMEOUT,terrariumEngine.LOOP_TIMEOUT))

  def __send_message(self,message):
    for queue in self.subscribed_queues:
      queue.put(message)

  # End private/internal functions


  # Weather part
  def set_weather_config(self,data):
    self.weather.set_source(data['location'])
    self.weather.set_windspeed_indicator(data['windspeed'])

    update_ok = self.config.save_weather(self.weather.get_config())
    return update_ok

  def get_weather_config(self):
    return self.weather.get_config()

  def get_weather(self, parameters = [], socket = False):
    data = self.weather.get_data()

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

        average[averagetype]['alarm'] = not (average[averagetype]['alarm_min'] < average[averagetype]['current'] < average[averagetype]['alarm_max'])
        average[averagetype]['amount'] = amount
        average[averagetype]['type'] = averagetype

      data = average

    if socket:
      self.__send_message({'type':'sensor_gauge','data':data})
    else:
      return {'sensors' : data}

  def get_amount_of_sensors(self, filtertype = None):
    if filtertype is None:
      return len(self.sensors)
    else:
      return len(self.get_sensors([filtertype])['sensors'])

  def get_sensors_config(self, socket = False):
    return self.get_sensors()

  def set_sensors_config(self, data):
    new_sensors = {}
    for sensordata in data:
      if sensordata['id'] is None or sensordata['id'] == 'None' or sensordata['id'] not in self.sensors:
        # New sensor
        sensor = terrariumSensor(None,sensordata['hardwaretype'],sensordata['type'],sensordata['address'],indicator=self.get_temperature_indicator)
      else:
        # Existing sensor
        sensor = self.sensors[sensordata['id']]
        # Should not be able to change setings
        #sensor.set_hardware_type(sensordata['hardwaretype'])
        #sensor.set_type(sensordata['type'])

      # Updating address will softly fail when updating OWFS sensors.
      sensor.set_address(sensordata['address'])
      sensor.set_name(sensordata['name'])
      sensor.set_alarm_min(sensordata['alarm_min'])
      sensor.set_alarm_max(sensordata['alarm_max'])
      sensor.set_limit_min(sensordata['limit_min'])
      sensor.set_limit_max(sensordata['limit_max'])

      new_sensors[sensor.get_id()] = sensor

    self.sensors = new_sensors
    if self.config.save_sensors(self.sensors):
      self.__load_sensors(True)
      return True

    return False
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
      self.__send_message({'type':'power_switches','data':data})
    else:
      return {'switches' : data}

  def get_amount_of_switches(self):
    return len(self.power_switches)

  def get_switches_config(self, socket = False):
    return self.get_switches()

  def set_switches_config(self, data):
    new_switches = {}
    for switchdata in data:
      if switchdata['id'] is None or switchdata['id'] == 'None' or switchdata['id'] not in self.power_switches:
        # New switch (add)
        power_switch = terrariumSwitch(None,switchdata['hardwaretype'],switchdata['address'],callback=self.toggle_switch)
      else:
        # Existing switch
        power_switch = self.power_switches[switchdata['id']]
        # Should not be able to change setings
        #power_switch.set_hardware_type(switchdata['hardwaretype'])

      power_switch.set_address(switchdata['address'])
      power_switch.set_name(switchdata['name'])
      power_switch.set_power_wattage(switchdata['power_wattage'])
      power_switch.set_water_flow(switchdata['water_flow'])
      if 'dimmer_duration' in switchdata:
        power_switch.set_dimmer_duration(switchdata['dimmer_duration'])
      if 'dimmer_on_duration' in switchdata:
        power_switch.set_dimmer_on_duration(switchdata['dimmer_on_duration'])
      if 'dimmer_on_percentage' in switchdata:
        power_switch.set_dimmer_on_percentage(switchdata['dimmer_on_percentage'])
      if 'dimmer_off_duration' in switchdata:
        power_switch.set_dimmer_off_duration(switchdata['dimmer_off_duration'])
      if 'dimmer_off_percentage' in switchdata:
        power_switch.set_dimmer_off_percentage(switchdata['dimmer_off_percentage'])

      new_switches[power_switch.get_id()] = power_switch

    self.power_switches = new_switches
    if self.config.save_power_switches(self.power_switches):
      self.__load_power_switches(True)
      return True

    return False

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
      self.__send_message({'type':'door_data','data':data})
    else:
      return {'doors' : data}

  def get_amount_of_doors(self):
    return len(self.doors)

  def get_doors_config(self):
    return self.get_doors()

  def set_doors_config(self, data):
    new_doors = {}
    for doordata in data:
      if doordata['id'] is None or doordata['id'] == 'None' or doordata['id'] not in self.doors:
        # New switch (add)
        door = terrariumDoor(None,doordata['hardwaretype'],doordata['address'])
      else:
        # Existing door
        door = self.doors[doordata['id']]
        # Should not be able to change setings
        #power_switch.set_hardware_type(switchdata['hardwaretype'])

      door.set_address(doordata['address'])
      door.set_name(doordata['name'])

      new_doors[door.get_id()] = door

    self.doors = new_doors
    if self.config.save_doors(self.doors):
      self.__load_doors(True)
      return True

    return False

  def toggle_door_status(self, data, socket = False):
    self.collector.log_door_data(data)
    if socket:
      self.door_status(True)

  def door_status(self, socket = False):
    door_closed = True
    for doorid in self.doors:
      door_closed = door_closed and self.doors[doorid].get_status() == terrariumDoor.CLOSED

    data = terrariumDoor.CLOSED if door_closed else terrariumDoor.OPEN

    if socket:
      self.__send_message({'type':'door_indicator','data': data})
    else:
      return data

  def is_door_open(self):
    return self.door_status() == terrariumDoor.OPEN

  def is_door_closed(self):
    return self.door_status() == terrariumDoor.CLOSED
  # End doors part


  # Webcams part
  def get_webcams(self, parameters = [], socket = False):
    data = []
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    if filter is not None and filter in self.webcams:
      data.append(self.webcams[filter].get_data())

    else:
      for webcamid in self.webcams:
        data.append(self.webcams[webcamid].get_data())

    if socket:
      self.__send_message({'type':'webcam_data','data':data})
    else:
      return {'webcams' : data}

  def get_amount_of_webcams(self):
    return len(self.webcams)

  def get_webcams_config(self):
    return self.get_webcams()

  def set_webcams_config(self, data):
    new_webcams = {}
    for webcamdata in data:
      if webcamdata['id'] is None or webcamdata['id'] == 'None' or webcamdata['id'] not in self.webcams:
        # New webcam (add)
        webcam = terrariumWebcam(None,webcamdata['location'],webcamdata['name'])
      else:
        # Existing webcam
        webcam = self.webcams[webcamdata['id']]

      webcam.set_location(webcamdata['location'])
      webcam.set_name(webcamdata['name'])
      webcam.set_rotation(webcamdata['rotation'])

      new_webcams[webcam.get_id()] = webcam

    self.webcams = new_webcams
    if self.config.save_webcams(self.webcams):
      self.__load_webcams(True)
      return True

    return False
  # End webcams part


  # Environment part
  def get_environment(self, parameters = [], socket = False):
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    data = self.environment.get_average()
    data['light'] = self.environment.get_light_state()
    data['sprayer'] = self.environment.get_sprayer_state()
    data['heater'] = self.environment.get_heater_state()
    data['cooler'] = self.environment.get_cooler_state()

    if filter is not None:
      data = { filter: data[filter]}

    if socket:
      self.__send_message({'type':'environment','data':data})
    else:
      return { 'environment' : data }

  def get_environment_config(self):
    return self.environment.get_config()

  def set_environment_config(self,data):
    if 'light' in data:
      self.environment.set_light_config(data['light'])

    if 'sprayer' in data:
      self.environment.set_sprayer_config(data['sprayer'])

    if 'heater' in data:
      self.environment.set_heater_config(data['heater'])

    if 'cooler' in data:
      self.environment.set_cooler_config(data['cooler'])

    update_ok = self.config.save_environment(self.environment.get_config())
    if update_ok:
      self.environment.reload_config()
    return update_ok
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

    cpu_temp = -1
    with open('/sys/class/thermal/thermal_zone0/temp') as temperature:
      cpu_temp = float(temperature.read()) / 1000.0

    data = {'memory' : {'total' : memory.total,
                        'used' : memory.used,
                        'free' : memory.free},
            'load' : {'load1' : uptime['load'][0],
                      'load5' : uptime['load'][1],
                      'load15' : uptime['load'][2]},
            'uptime' : uptime['uptime'],
            'cores' : psutil.cpu_count(),
            'temperature' : cpu_temp}

    if socket:
      gauge_data = {'system_load'        : {'current' : data['load']['load1'] * 100, 'alarm_min' : 0, 'alarm_max': 80, 'limit_min' : 0, 'limit_max': 100},
                    'system_temperature' : {'current' : data['temperature'], 'alarm_min' : 30, 'alarm_max': 60, 'limit_min' : 0, 'limit_max': 80},
                    'system_memory'      : {'current' : data['memory']['used'] / (1024 * 1024), 'alarm_min' : data['memory']['total'] / (1024 * 1024) * 0.1, 'alarm_max': data['memory']['total'] / (1024 * 1024) * 0.9, 'limit_min' : 0, 'limit_max': data['memory']['total'] / (1024 * 1024)}}

      gauge_data['system_load']['alarm'] = not(gauge_data['system_load']['alarm_min'] < gauge_data['system_load']['current'] < gauge_data['system_load']['alarm_max'])
      gauge_data['system_temperature']['alarm'] = not(gauge_data['system_temperature']['alarm_min'] < gauge_data['system_temperature']['current'] < gauge_data['system_temperature']['alarm_max'])
      gauge_data['system_memory']['alarm'] = not(gauge_data['system_memory']['alarm_min'] < gauge_data['system_memory']['current'] < gauge_data['system_memory']['alarm_max'])

      self.__send_message({'type':'sensor_gauge','data':gauge_data})
    else:
      return data

  def get_uptime(self, socket = False):
    data = {'uptime' : uptime.uptime(),
            'timestamp' : int(time.time()),
            'day' : self.weather.is_day(),
            'load' : os.getloadavg()}

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
    return self.temperature_indicator

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

      update_ok = self.set_system_config(data)
      if update_ok:
        # Update config settings
        self.pi_power_wattage = float(self.config.get_pi_power_wattage())
        self.set_authentication(self.config.get_admin(),self.config.get_password())
        self.temperature_indicator = self.config.get_temperature_indicator()

    return update_ok

  def get_system_config(self):
    data = self.config.get_system()
    del(data['password'])
    return data

  def set_system_config(self,data):
    return self.config.set_system(data)

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
