# -*- coding: utf-8 -*-
from terrariumDoor import terrariumDoor
from terrariumSensor import terrariumSensor
from terrariumSwitchboard import terrariumSwitchboard
from terrariumWeather import terrariumWeather
from terrariumWebcam import terrariumWebcam
from terrariumCollector import terrariumCollector
from terrariumEnvironment import terrariumEnvironment
from terrariumConfig import terrariumConfig

import thread
import time
import uptime
import os
import datetime
import psutil

from gevent import monkey, sleep
monkey.patch_all()

class terrariumEngine():

  def __init__(self):
    # List of queues for websocket communication
    self.subscribed_queues = []
    # Default power usage for a PI
    self.pi_power_wattage = 5

    self.switch_board = None #TODO: Fix proper
    self.environment = None

    # Load config
    self.config = terrariumConfig()
    self.set_authentication(self.config.get_admin(),self.config.get_password())

    # Load data collector for historical data
    self.collector = terrariumCollector()

    # Set the Pi power usage (including usb devices directly on the PI)
    self.pi_power_wattage = float(self.config.get_pi_power_wattage())

    # Load Weather part
    self.weather = terrariumWeather(self.config.get_weather_location(),
                                    self.config.get_weather_windspeed(),
                                    self.config.get_weather_temperature(),
                                    self.get_weather)

    # Load Powerswitches part
    self.power_switches = {}
    self.switch_board = terrariumSwitchboard(self.config,self.toggle_switch)
    self.power_switches = self.switch_board.switches

    # Load Door part
    self.door_sensor = terrariumDoor(self.config.get_door_pin(),self.door_status)

    # Load Sensors, with ID as index
    self.sensors = {}
    for sensor in terrariumSensor.scan(self.config.get_1wire_port(), self.config.get_sensors()):
      self.sensors[sensor.get_id()] = sensor

    # Load the environment system. This will controll the lights, sprayer and heaters
    self.environment = terrariumEnvironment(self.sensors, self.power_switches, self.door_sensor, self.weather, self.config)

    # Load webcams from config
    self.webcams = {}
    webcams = self.config.get_webcams()
    for webcamid in webcams:
      self.webcams[webcams[webcamid]['id']] = terrariumWebcam(webcams[webcamid]['id'],webcams[webcamid]['location'],webcams[webcamid]['name'],webcams[webcamid]['rotation'])

    # Start system update loop
    thread.start_new_thread(self.__engine_loop, ())

  def __get_power_usage_water_flow(self, socket = False):
    data = {'power' : {'current' : self.pi_power_wattage , 'max' : self.pi_power_wattage},
            'water' : {'current' : 0.0 , 'max' : 0.0}}

    for switchid in self.power_switches:
      data['power']['current'] += self.power_switches[switchid].get_power_wattage() if self.power_switches[switchid].is_on() else 0.0
      data['power']['max'] += self.power_switches[switchid].get_power_wattage()

      data['water']['current'] += self.power_switches[switchid].get_water_flow() if self.power_switches[switchid].is_on() else 0.0
      data['water']['max'] += self.power_switches[switchid].get_water_flow()

    return data

  def __calculate_power_usage_water_flow(self):
    data = {'power_wattage' : 0.0,
            'water_flow' : 0.0,
            'total_power': 0.0,
            'total_water' : 0.0}

    today = datetime.date.today()
    today = int(time.mktime(today.timetuple()))
    now = int(time.time())
    uptime = self.get_uptime()['uptime']
    if uptime > now - today:
      uptime = now -today

    data['power_wattage'] = (float(uptime) / 3600.0) * float(self.pi_power_wattage)
    prev_data = self.collector.get_history(['switches','summary'])['switches']['summary']

    for fieldname in prev_data:
      for data_item in prev_data[fieldname]:
        if data_item[0] / 1000 < today:
          data[fieldname] = float(data_item[1])

    history_data = self.collector.get_history(['switches'])['switches']

    for switchid in history_data:
      if switchid not in history_data or len(history_data[switchid]['state']) == 0:
        continue

      if switchid in self.power_switches and self.power_switches[switchid].is_on() and not history_data[switchid]['state'][len(history_data[switchid]['state'])-1][1]:
        # Fake end state
        history_data[switchid]['state'].append([now * 1000 , False])

      for counter in range(0,len(history_data[switchid]['state'])):
        if counter > 0 and (history_data[switchid]['state'][counter][0] / 1000) >= today and not history_data[switchid]['state'][counter][1] and history_data[switchid]['state'][counter-1][1]:
          duration = (float(history_data[switchid]['state'][counter][0]) - float(history_data[switchid]['state'][counter-1][0])) / 1000.0
          data['power_wattage'] += (duration / 3600.0) * float(history_data[switchid]['power_wattage'][counter-1][1])
          data['water_flow'] += (duration / 60.0) * float(history_data[switchid]['water_flow'][counter-1][1])

    data['total_power'] += data['power_wattage']
    data['total_water'] += data['water_flow']
    return data

  def __engine_loop(self):
    while True:
      for sensorid in self.sensors:
        # Update the current temperature.
        self.sensors[sensorid].update()
        # Save new data to database TODO: UPDATE to get the right fields
        self.collector.log_sensor_data(self.sensors[sensorid])
        # Websocket callback
        self.get_sensors([sensorid],socket=True)
        # Make time for other web request
        sleep(0.2)

      # Get the current average temperatures
      average_data = self.get_sensors(['average'])['sensors']
      for averagetype in average_data:
        # Save data in database per type
        self.collector.log_summary_sensor_data(averagetype,average_data[averagetype])

      # Websocket callback
      self.__send_message({'type':'sensor_gauge','data':average_data})

      # Calculate power and water usage per day
      self.collector.log_power_usage_water_flow(self.__calculate_power_usage_water_flow())

      # Websocket messages back
      self.get_uptime(socket=True)
      self.get_power_usage_water_flow(socket=True)
      self.get_environment(socket=True)

      # Update weather
      self.weather.update()
      self.collector.log_weather_data(self.weather.get_data()['hour_forecast'][0])

      # Log system stats
      self.collector.log_system_data(self.get_system_stats())
      self.get_system_stats(socket=True)

      for webcamid in self.webcams:
        self.webcams[webcamid].update()
        sleep(0.2)

      sleep(30) # TODO: Config setting

  def __send_message(self,message):
    for queue in self.subscribed_queues:
      queue.put(message)

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
      gauge_data = {'system_load'        : {'current' : data['load']['load1'] * 100, 'alarm_min' : 0, 'alarm_max': 80, 'min' : 0, 'max': 100},
                    'system_temperature' : {'current' : data['temperature'], 'alarm_min' : 30, 'alarm_max': 60, 'min' : 0, 'max': 80},
                    'system_memory'      : {'current' : data['memory']['used'] / (1024 * 1024), 'alarm_min' : data['memory']['total'] / (1024 * 1024) * 0.1, 'alarm_max': data['memory']['total'] / (1024 * 1024) * 0.9, 'min' : 0, 'max': data['memory']['total'] / (1024 * 1024)}}

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
    data = self.__get_power_usage_water_flow()
    totaldata = self.__calculate_power_usage_water_flow()

    data['power']['total'] = totaldata['total_power']
    data['water']['total'] = totaldata['total_water']

    if socket:
      self.__send_message({'type':'power_usage_water_flow','data':data});
    else:
      return data

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

    if 'environment' == part or part is None:
      data.update(self.get_environment_config())

    return data

  def set_config(self,part,data):
    update_ok = False
    if 'weather' == part:
      update_ok = self.set_weather_config(data)

    elif 'switches' == part:
      update_ok = self.set_switches_config(data)

    elif 'sensors' == part:
      update_ok = self.set_sensors_config(data)

    elif 'webcams' == part:
      update_ok = self.set_webcams_config(data)

    elif 'environment' == part:
      update_ok = self.set_environment_config(data)

    elif 'system' == part:
      update_ok = self.set_system_config(data)
      if update_ok:
        # Update config settings
        self.pi_power_wattage = float(self.config.get_pi_power_wattage())
        self.door_sensor.set_gpio_pin(self.config.get_door_pin())
        self.set_authentication(self.config.get_admin(),self.config.get_password())

    return update_ok

  def get_system_config(self):
    return self.config.get_system()

  def set_system_config(self,data):
    return self.config.set_system(data)

  # Weather part
  def set_weather_config(self,data):
    self.weather.set_location(data['location'])
    self.weather.set_windspeed_indicator(data['windspeed'])
    self.weather.set_temperature_indicator(data['temperature'])

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

  # Door part
  def door_status(self, socket = False):
    data = self.door_sensor.get_status()

    if socket:
      self.__send_message({'type':'door_indicator','data': data})
    else:
      return data

  def is_door_open(self):
    return self.door_sensor.is_open()

  def is_door_closed(self):
    return self.door_sensor.is_closed()
  # End door part


  # Sensors part
  def get_sensors_config(self, socket = False):
    return self.get_sensors()

  def set_sensors_config(self, data):
    update_ok = True
    for sensordata in data:
      sensor = self.sensors[sensordata['id']]
      sensor.set_name(sensordata['name'])
      sensor.set_alarm_min(sensordata['alarm_min'])
      sensor.set_alarm_max(sensordata['alarm_max'])
      sensor.set_min(sensordata['min'])
      sensor.set_max(sensordata['max'])

      update_ok = update_ok and self.config.save_sensor(sensor.get_data())

    return update_ok

  def get_amount_of_sensors(self, type = None):
    if type is None:
      return len(self.sensors)

    amount = 0
    for sensorid in self.sensors:
      if self.sensors[sensorid].get_type() == type:
        amount += 1

    return amount

  def get_sensors(self, parameters = [], socket = False):
    data = []
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    if filter is not None and filter in self.sensors:
      data.append(self.sensors[filter].get_data())

    else:
      for sensorid in self.sensors:
        if filter is None or filter == 'average' or filter == self.sensors[sensorid].get_type():
          data.append(self.sensors[sensorid].get_data())

    if 'average' == filter or len(parameters) == 2 and parameters[1] == 'average':
      average = {}
      for sensor in data:
        if sensor['type'] not in average:
          average[sensor['type']] = {'current' : 0.0, 'alarm_min' : 0.0, 'alarm_max' : 0.0, 'min' : 0.0, 'max':0.0, 'amount' : 0.0}

        average[sensor['type']]['current'] += sensor['current']
        average[sensor['type']]['alarm_min'] += sensor['alarm_min']
        average[sensor['type']]['alarm_max'] += sensor['alarm_max']
        average[sensor['type']]['min'] += sensor['min']
        average[sensor['type']]['max'] += sensor['max']
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
  # End sensors part

  # Switch part
  def get_switches_config(self, socket = False):
    return self.get_switches()

  def set_switches_config(self, data):
    update_ok = True
    for switchdata in data:
      switch = self.power_switches[switchdata['id']]
      switch.set_name(switchdata['name'])
      switch.set_power_wattage(switchdata['power_wattage'])
      switch.set_water_flow(switchdata['water_flow'])

      update_ok = update_ok and self.config.save_switch(switch.get_data())

    if update_ok:
      self.power_switches = {}
      self.switch_board = terrariumSwitchboard(self.config,self.toggle_switch)
      self.power_switches = self.switch_board.switches

    return update_ok

  def get_amount_of_switches(self):
    return len(self.power_switches)

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

  def toggle_switch(self,data):
    self.collector.log_switch_data(data)
    self.get_switches(socket=True)
    self.get_power_usage_water_flow(socket=True)

    if self.environment is not None:
      self.get_environment(socket=True)

  def get_max_switches_config(self):
    return int(self.config.get_system()['max_switches'])
  # End switch part

  # Webcam part
  def get_amount_of_webcams(self):
    return len(self.webcams)

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

  def get_webcams_config(self):
    return self.get_webcams()

  def set_webcams_config(self, data):
    update_ok = True
    for webcamdata in data:

      if webcamdata['id'] == '' or webcamdata['id'] not in self.webcams:
        # Create new one
        if webcamdata['location'] != '':
          webcam = terrariumWebcam(None,webcamdata['location'],webcamdata['name'],webcamdata['rotation'])
      else:
        webcam = self.webcams[webcamdata['id']]
        webcam.set_name(webcamdata['name'])
        webcam.set_location(webcamdata['location'])
        webcam.set_rotation(webcamdata['rotation'])

      update_ok = update_ok and self.config.save_webcam(webcam.get_data())

    return update_ok
  # End webcam part

  # Environment part
  def get_environment(self, parameters = [], socket = False):
    filter = None
    if len(parameters) > 0 and parameters[0] is not None:
      filter = parameters[0]

    data = self.environment.get_average()
    data['light'] = self.environment.get_light_state()
    data['sprayer'] = self.environment.get_sprayer_state()
    data['heater'] = self.environment.get_heater_state()

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

    update_ok = self.config.save_environment(self.environment.get_config())
    if update_ok:
      self.environment.reload_config()
    return update_ok
  # End Environment part


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
