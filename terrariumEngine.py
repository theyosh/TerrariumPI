# -*- coding: utf-8 -*-
from terrariumDoor import terrariumDoor
from terrariumSensor import terrariumSensor
from terrariumSwitchboard import terrariumSwitchboard
from terrariumWeather import terrariumWeather
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

    # Load config
    self.config = terrariumConfig(self.get_config)

    # Load data collector for historical data
    self.collector = terrariumCollector()

    # Set the Pi power usage (including usb devices directly on the PI)
    self.pi_power_wattage = float(self.config.get_pi_power_wattage())

    # Load Weather part
    self.weather = terrariumWeather(self.config.get_weather_location(),
                                    self.config.get_weather_windspeed(),
                                    self.config.get_weather_temperature(),
                                    self.get_weather)

    # Load Powerswitches part TODO: Refactor
    self.switch_board = terrariumSwitchboard(self.config,self.toggle_switch)
    self.power_switches = {}
    for power_switch in self.switch_board.switches:
      self.power_switches[power_switch.get_id()] = power_switch

    # Load Door part
    self.door_sensor = terrariumDoor(self.config.get_door_pin(),None)

    # Load Sensors, with ID as index
    self.sensors = {}
    for sensor in terrariumSensor.scan(self.config.get_1wire_port(), self.config.get_sensors()):
      self.sensors[sensor.get_id()] = sensor

    # Load the environment system. This will controll the lights, sprayer and heaters
    self.environment = terrariumEnvironment(self.sensors, self.power_switches, self.door_sensor, self.weather, self.config)

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
    prev_data = self.collector.get_history('switches','summary')['switches']['summary']
    for fieldname in prev_data:
      for data_item in prev_data[fieldname]:
        if data_item[0] / 1000 < today:
          data[fieldname] = float(data_item[1])

    history_data = self.collector.get_history('switches')['switches']
    for switchid in history_data:
      if len(history_data[switchid]['state']) == 0:
        continue

      if self.power_switches[switchid].is_on() and history_data[switchid]['state'][len(history_data[switchid]['state'])-1][1]:
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
        # Save new data to database
        self.collector.log_sensor_data(self.sensors[sensorid])
        # Websocket callback
        self.get_sensors(sensorid,True)
        # Make time for other web request
        sleep(0.2)

      # Get the current average temperatures
      average_data = self.environment.get_average()
      for sensortype in average_data:
        # Save data in database per type
        self.collector.log_environment_data(sensortype,average_data[sensortype])

      # Websocket callback
      self.__send_message({'type':'sensor_gauge','data':average_data})

      # Calculate power and water usage per day
      self.collector.log_power_usage_water_flow(self.__calculate_power_usage_water_flow())

      # Websocket messages back
      self.get_uptime(True)
      self.get_power_usage_water_flow(True)
      self.get_environment(None,True)

      # Update weather
      self.weather.update()
      self.collector.log_weather_data(self.weather.get_data()['hour_forecast'][0])

      self.get_system_stats()

      sleep(30) # TODO: Config setting

  def __send_message(self,message):
    for queue in self.subscribed_queues:
      queue.put(message)

  def subscribe(self,queue):
    self.subscribed_queues.append(queue)
    self.__send_message({'type':'dashboard_online', 'data':True})

  def get_system_stats(self):
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
            'temperature' : cpu_temp}

    self.collector.log_system_data(data)

  def get_uptime(self, socket = False):
    data = {'uptime' : uptime.uptime(),
              'load' : os.getloadavg()}

    if socket:
      self.__send_message({'type':'dashboard_uptime','data':data})
    else:
      return data

  # API Config calls
  def get_config(self, part = None):
    data = {}
    if 'system' == part:
      data = self.get_system_config()

    elif 'weather' == part:
      data = self.get_weather_config()

    elif 'switches' == part:
      data = self.get_switches_config()

    elif 'sensors' == part:
      data = self.get_sensors_config()

    elif 'environment' == part:
      data = self.get_environment_config()

    elif part is None:
      data = self.config.get_full_config()

    return data

  def set_config(self,part,data):
    update_ok = False
    if 'weather' == part:
      update_ok = self.set_weather_config(data)

    elif 'switches' == part:
      update_ok = self.set_switches_config(data)

    elif 'sensors' == part:
      update_ok = self.set_sensors_config(data)

    elif 'environment' == part:
      update_ok = self.set_environment_config(data)

    return update_ok

  def get_system_config(self):
    return self.config.get_system()

  def set_weather_config(self,data):
    self.weather.set_location(data['location'])
    self.weather.set_windspeed_indicator(data['windspeed'])
    self.weather.set_temperature_indicator(data['temperature'])

    update_ok = self.config.save_weather(self.weather.get_config())
    return update_ok

  def get_weather_config(self):
    return self.weather.get_config()

  def get_weather(self, socket = False):
    data = self.weather.get_data()

    if socket:
      self.__send_message({'type':'update_weather','data':data})
    else:
      return data

  def set_switches_config(self,data):
    update_ok = True
    for switchdata in data:
      switch = self.power_switches[switchdata['id']]
      switch.set_name(switchdata['name'])
      switch.set_power_wattage(switchdata['power_wattage'])
      switch.set_water_flow(switchdata['water_flow'])

      update_ok = update_ok and self.config.save_switch(switch.get_data())

    return update_ok

  def get_switches_config(self):
    return self.switch_board.get_config()

  def get_switches(self, socket = False):
    if self.switch_board is None:
      return False

    data = self.switch_board.get_switches()
    if socket:
      self.__send_message({'type':'power_switches','data':data})
      self.get_power_usage_water_flow(True)
      self.get_environment(None,True)
    else:
      return data

  def toggle_switch(self,data):
    self.collector.log_switch_data(data)
    self.get_switches(True)

  def get_power_usage_water_flow(self, socket = False):
    data = self.__get_power_usage_water_flow()
    totaldata = self.__calculate_power_usage_water_flow()

    data['power']['total'] = totaldata['total_power']
    data['water']['total'] = totaldata['total_water']

    if socket:
      self.__send_message({'type':'dashboard_power_usage','data':data['power']});
      self.__send_message({'type':'dashboard_water_flow','data':data['water']});
    else:
      return data

  def get_total_power_usage_water_flow(self, socket = False):
    data = self.__calculate_power_usage_water_flow()
    if socket:
      self.__send_message({'type':'power_usage_water_flow','data':{
          'total_power' : data['power_wattage'] / 1000.0,
          'total_water' : data['water_flow']
        }})
    else:
      return data

  def get_amount_of_switches(self):
    return len(self.power_switches)

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

  def get_average_temperature(self, socket = False):
    return self.get_average_sensors('temperature', socket)

  def get_average_humidity(self, socket = False):
    return self.get_average_sensors('humidity', socket)

  def get_average_sensors(self, type = None, socket = False):
    data = self.environment.get_average()

    if socket:
      self.__send_message({'type':'dashboard_sensors','data':data})
    else:
      return data

  # Environment part
  def get_environment(self, filter = None, socket = False):
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
    self.environment.reload_config()
    return True

  # End Environment part


  # Sensor part
  def get_sensors(self, filter = None, socket = False):
    data = []
    if filter is not None and filter in self.sensors:
      data.append(self.sensors[filter].get_data())

    else:
      for sensorid in self.sensors:
        if filter is None or filter == self.sensors[sensorid].get_type():
          data.append(self.sensors[sensorid].get_data())

    if socket:
      self.__send_message({'type':'sensor_gauge','data':data})
    else:
      return {'sensors' : data}
  # End Sensor part


  # Histroy part (Collector)
  def get_history(self, type = None, subtype = None, id = None, socket = False):
    data = {}
    if type == 'sensors' or type == 'switches' or type == 'system':
      if id is not None and id in self.sensors:
        data = self.collector.get_history(type,self.sensors[id].get_type(),id)

      else:
        data = self.collector.get_history(type,subtype,id)

    if socket:
      self.__send_message({'type':'history_graph','data': data})
    else:
      return data
  # End Histroy part (Collector)


  def door_status(self):
    return self.door_status.get_status()

  def is_door_open(self):
    return self.door_status.is_open()

  def is_door_closed(self):
    return self.door_status.is_closed()
