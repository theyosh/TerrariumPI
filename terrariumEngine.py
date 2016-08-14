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

    self.collector = terrariumCollector()

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

    self.environment = terrariumEnvironment(self.sensors, self.power_switches, self.door_sensor, self.weather, self.config)

    # Start uptime timer
    thread.start_new_thread(self.get_uptime, (True,))

    # Start sensors update loop
    thread.start_new_thread(self.__engine_loop, ())

  def __get_power_usage_water_flow(self, socket = False):
    data = {'power' : {'current' : self.pi_power_wattage , 'max' : self.pi_power_wattage, 'history' : 0},
            'water' : {'current' : 0 , 'max' : 0, 'history' : 0}}

    for switch in self.switch_board.get_switches()['switches']:
      data['power']['current'] += switch['power_wattage'] if switch['state'] else 0
      data['power']['max'] += switch['power_wattage']

      data['water']['current'] += switch['water_flow'] if switch['state'] else 0
      data['water']['max'] += switch['water_flow']

    return data

  def __calculate_power_usage_water_flow(self):
    data = {'power_wattage' : 0.0,
            'water_flow' : 0.0,
            'total_power': 0.0,
            'total_water' : 0.0}

    today = datetime.date.today()
    today = int(time.mktime(today.timetuple()))
    now = int(time.time())
    duration = self.get_uptime()['uptime']
    if duration > now - today:
      duration = now -today

    data['power_wattage'] = (float(duration) / 3600.0) * float(self.pi_power_wattage)

    prev_data = self.collector.get_history('switches','summary')['switches']['summary']
    for fieldname in prev_data:
      for data_item in prev_data[fieldname]:
        if data_item[0] / 1000 < today:
          data[fieldname] = data_item[1]

    history_data = self.collector.get_history('switches')['switches']
    for switchid in history_data:
      if len(history_data[switchid]['state']) == 0:
        continue

      if self.power_switches[switchid].is_on() and history_data[switchid]['state'][len(history_data[switchid]['state'])-1][1]:
        # Fake end state
        history_data[switchid]['state'].append([now * 1000 , False])

      for counter in range(0,len(history_data[switchid]['state'])):
        if counter > 0 and (history_data[switchid]['state'][counter][0] / 1000) >= today and not history_data[switchid]['state'][counter][1]:
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

      # Decide if need a sensor callback update
      self.__send_message({'type':'sensor_gauge','data':average_data})

      self.weather.update()
      self.collector.log_weather_data(self.weather.get_data()['hour_forecast'][0])

      # Calculate power and water usage per day
      data = self.__calculate_power_usage_water_flow()
      self.__send_message({'type':'power_usage_water_flow','data':{
          'total_power' : data['power_wattage'] / 1000.0,
          'total_water' : data['water_flow']
      }})
      self.collector.log_power_usage_water_flow(data)

      sleep(30) # TODO: Config setting

  def __send_message(self,message):
    for queue in self.subscribed_queues:
      queue.put(message)

  def subscribe(self,queue):
    self.subscribed_queues.append(queue)
    self.__send_message({'type':'dashboard_online', 'data':True})

  def get_uptime(self, socket = False):
    data = {'uptime' : uptime.uptime(),
              'load' : os.getloadavg()}

    if not socket:
      return data

    while True:
      self.__send_message({'type':'dashboard_uptime','data':data})
      sleep(60)


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
      self.__send_message({'type':'dashboard_weather','data':data})
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
      self.__send_message({'type':'dashboard_switches','data':data});
      self.get_power_usage_water_flow(True);
    else:
      return data

  def toggle_switch(self,data):
    self.collector.log_switch_data(data)
    self.get_switches(True)

  def get_power_usage_water_flow(self, socket = False):
    data = self.__get_power_usage_water_flow()
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
    data['lights'] = self.environment.get_lights_state()
    data['lights']['modus'] = self.environment.get_light_settings()['modus']
    data['lights']['enabled'] = self.environment.get_light_settings()['enabled']
    data['lights']['state'] = 'on' if data['lights']['on'] < int(time.time()) < data['lights']['off'] else 'off'

    data['sprayer'] = self.environment.get_humidity_state()
    data['sprayer']['enabled'] = self.environment.get_humidity_settings()['enabled']
    data['sprayer']['alarm'] = data['sprayer']['current'] <  data['sprayer']['alarm_min']

    data['heater'] = self.environment.get_heater_state()
    data['heater']['modus'] = self.environment.get_heater_settings()['modus']
    data['heater']['enabled'] = self.environment.get_heater_settings()['enabled']
    data['heater']['alarm'] = not (data['heater']['alarm_max'] > data['heater']['current'] >  data['heater']['alarm_min'])

    if filter is not None:
      data = { filter: data[filter]}

    if socket:
      pass
      #self.__send_message({'type':'dashboard_sensors','data':data})
    else:
      return { 'environment' : data }

  def get_environment_config(self):
    return self.environment.get_config()

  def set_environment_config(self,data):
    if 'lights' in data:
      self.environment.set_light_settings(data['lights'])

    if 'humidity' in data:
      self.environment.set_humidity_settings(data['humidity'])

    if 'heater' in data:
      self.environment.set_heater_settings(data['heater'])

    update_ok = self.config.save_environment(self.environment.get_config())
    self.environment.reload_settings()
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
    if type == 'sensors' or type == 'switches':
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
