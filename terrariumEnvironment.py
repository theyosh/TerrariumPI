# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import thread
import datetime
from threading import Timer
import copy
import time

from terrariumDoor import terrariumDoor

from gevent import monkey, sleep
monkey.patch_all()

class terrariumEnvironment():

  def __init__(self, sensors, power_switches, weather, door_status, config):
    self.config = config
    self.sensors = sensors
    self.power_switches = power_switches

    self.door_status = door_status
    self.weather = weather
    self.reload_config()
    logger.info('Starting environment')
    thread.start_new_thread(self.__engine_loop, ())

  def __parse_config(self):
    config = self.config.get_environment()

    self.light = config['light']
    init = len(self.light) == 0
    if init:
      self.light = {}

    self.light['enabled'] = False if init else (True if self.light['enabled'].lower() in ['true','on','1'] else False)
    self.light['modus'] = None if init else self.light['modus']
    self.light['on'] = 0 if init else int(self.light['on'])
    self.light['off'] = 0 if init else int(self.light['off'])
    self.light['hours_shift'] = 0.0 if init else float(self.light['hours_shift'])
    self.light['min_hours'] = 0.0 if init else float(self.light['min_hours'])
    self.light['max_hours'] = 0.0 if init else float(self.light['max_hours'])
    self.light['power_switches'] = [] if (init or self.light['power_switches'] == '' ) else self.light['power_switches'].split(',')

    self.sprayer = config['sprayer']
    init = len(self.sprayer) == 0
    if init:
      self.sprayer = {}

    self.sprayer['enabled'] = False if init else (True if self.sprayer['enabled'].lower() in ['true','on','1'] else False)
    self.sprayer['night_enabled'] = False if init else (True if self.sprayer['night_enabled'].lower() in ['true','on','1'] else False)
    self.sprayer['spray_duration'] = 0.0 if init else float(self.sprayer['spray_duration'])
    self.sprayer['spray_timeout'] = 0.0 if init else float(self.sprayer['spray_timeout'])
    self.sprayer['power_switches'] = [] if (init or self.sprayer['power_switches'] == '' ) else self.sprayer['power_switches'].split(',')
    self.sprayer['sensors'] = [] if (init or self.sprayer['sensors'] == '' ) else self.sprayer['sensors'].split(',')
    self.sprayer['lastaction'] = datetime.datetime.now()


    self.heater = config['heater']
    init = len(self.heater) == 0
    if init:
      self.heater = {}

    self.heater['enabled'] = False if init else (True if self.heater['enabled'].lower() in ['true','on','1'] else False)
    self.heater['modus'] = None if init else self.heater['modus']
    self.heater['day_enabled'] = False if init else (True if self.heater['day_enabled'].lower() in ['true','on','1'] else False)
    self.heater['power_switches'] = [] if (init or self.heater['power_switches'] == '' ) else self.heater['power_switches'].split(',')
    self.heater['sensors'] = [] if (init or self.heater['sensors'] == '' ) else self.heater['sensors'].split(',')

  def __set_config(self,part,data):
    for field in data:
      if 'light' == part:
        self.light[field] = data[field]
      elif 'sprayer' == part:
        self.sprayer[field] = data[field]
      elif 'heater' == part:
        self.heater[field] = data[field]

  def __engine_loop(self):
    while True:
      starttime = time.time()
      light = self.get_light_state()
      if 'enabled' in light and light['enabled']:
        if light['on'] < int(time.time()) < light['off']:
          self.light_on()
        else:
          self.light_off()

      light = self.get_light_state()
      sprayer = self.get_sprayer_state()
      if 'enabled' in sprayer and 'enabled' in light and sprayer['enabled'] and light['enabled']:
        if self.sprayer['night_enabled'] or light['state'] == 'on':
          if sprayer['alarm'] and self.door_status() == terrariumDoor.CLOSED:
            self.sprayer_on()
          else:
            self.sprayer_off()
        else:
          self.sprayer_off()
      else:
        self.sprayer_off()

      heater = self.get_heater_state()
      if 'enabled' in heater and 'enabled' in light and heater['enabled'] and light['enabled']:
        if self.heater['day_enabled'] or light['state'] == 'off':
          if heater['current'] < heater['alarm_min']:
            self.heater_on()
          elif heater['current'] > heater['alarm_max']:
            self.heater_off()
        else:
          self.heater_off()

      logger.info('Engine loop done in %s seconds' % (time.time() - starttime,))
      sleep(15)

  def __switch_on(self,part, state = None):
    is_on = True
    power_switches = []
    if 'light' == part:
      power_switches = self.light['power_switches']
    elif 'sprayer' == part:
      power_switches = self.sprayer['power_switches']
    elif 'heater' == part:
      power_switches = self.heater['power_switches']

    for switch in power_switches:
      if state is None:
        is_on = is_on and self.power_switches[switch].is_on()
      else:
        if state:
          self.power_switches[switch].on()
        else:
          self.power_switches[switch].off()

        is_on = state

    return is_on

  def __on(self,part):
    return True == self.__switch_on(part,True)

  def __off(self,part):
    return False == self.__switch_on(part,False)

  def __is_on(self,part):
    return self.__switch_on(part)

  def __is_off(self,part):
    return not self.__is_on(part)

  def get_config(self):
    return {'light' : self.get_light_config(),
            'sprayer' : self.get_sprayer_config() ,
            'heater' : self.get_heater_config()}

  def reload_config(self):
    self.__parse_config()

  def get_light_config(self):
    return self.light

  def set_light_config(self,data):
    self.__set_config('light',data)

  def light_on(self):
    return self.__on('light')

  def light_off(self):
    return self.__off('light')

  def is_light_on(self):
    return self.__is_on('light')

  def is_light_off(self):
    return self.__is_off('light')

  def get_light_state(self):
    now = datetime.datetime.now()

    data = {'on' : datetime.datetime.fromtimestamp(0), 'off' : datetime.datetime.fromtimestamp(0), 'modus' : self.light['modus'], 'enabled' : self.light['enabled']}
    if 'weather' == data['modus']:
      data['on'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['rise'])
      data['off'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['set'])

    elif 'timer' == data['modus']:
      data['on'] = datetime.datetime.fromtimestamp(self.light['on'])
      data['off'] = datetime.datetime.fromtimestamp(self.light['off'])

    # Duration check
    duration = data['off'] - data['on']
    # Reduce the amount of hours if to much
    if duration > datetime.timedelta(hours=self.light['max_hours']):
      duration -= datetime.timedelta(hours=self.light['max_hours'])
      data['on'] += datetime.timedelta(seconds=duration.total_seconds()/2)
      data['off'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
    # Increase the amount of hours it to little
    elif duration < datetime.timedelta(hours=self.light['min_hours']):
      duration = datetime.timedelta(hours=self.light['min_hours']) - duration
      data['on'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
      data['off'] += datetime.timedelta(seconds=duration.total_seconds()/2)

    # Shift hours
    data['on'] += datetime.timedelta(hours=self.light['hours_shift'])
    data['off'] += datetime.timedelta(hours=self.light['hours_shift'])

    # Shift time to next day?
    if now > data['off']:
      # Past offtime, so next day
      data['on'] += datetime.timedelta(hours=24)
      data['off'] += datetime.timedelta(hours=24)

    data['on'] = time.mktime(data['on'].timetuple())
    data['off'] = time.mktime(data['off'].timetuple())

    data['state'] = 'on' if self.is_light_on() else 'off'
    return data

  def get_sprayer_config(self):
    data = copy.deepcopy(self.sprayer)
    if 'lastaction' in data:
      del(data['lastaction'])
    return data

  def set_sprayer_config(self,data):
    self.__set_config('sprayer',data)

  def sprayer_on(self):
    if datetime.datetime.now() - self.sprayer['lastaction'] > datetime.timedelta(seconds=self.sprayer['spray_timeout']):
      self.__on('sprayer')
      (Timer(self.sprayer['spray_duration'], self.sprayer_off)).start()
      self.sprayer['lastaction'] = datetime.datetime.now()

  def sprayer_off(self):
    self.__off('sprayer')

  def is_sprayer_on(self):
    return self.__is_on('sprayer')

  def is_sprayer_off(self):
    return self.__is_off('sprayer')

  def get_sprayer_state(self):
    data = self.get_average_humidity()
    if data is None:
      return {}

    data['night_enabled'] = self.sprayer['night_enabled']
    data['enabled'] = self.sprayer['enabled']

    light = self.get_light_state()
    data['alarm'] = (data['night_enabled'] or (light['on'] < int(time.time()) < light['off'])) and data['current'] < data['alarm_min']
    data['state'] = 'on' if self.is_sprayer_on() else 'off'
    return data

  def get_heater_config(self):
    return self.heater

  def set_heater_config(self,data):
    self.__set_config('heater',data)

  def heater_on(self):
    self.__on('heater')

  def heater_off(self):
    self.__off('heater')

  def is_heater_on(self):
    return self.__is_on('heater')

  def is_heater_off(self):
    return self.__is_off('heater')

  def get_heater_state(self):
    data = self.get_average_temperature()
    if data is None:
      return {}

    data['modus'] = self.heater['modus']
    data['day_enabled'] = self.heater['day_enabled']
    data['enabled'] = self.heater['enabled']

    light = self.get_light_state()
    data['alarm'] = (data['day_enabled'] or not (light['on'] < int(time.time()) < light['off'])) and not (data['alarm_max'] >= data['current'] >= data['alarm_min'])
    data['state'] = 'on' if self.is_heater_on() else 'off'
    return data

  def get_average_temperature(self):
    data = self.get_average()
    if 'temperature' in data:
      return data['temperature']

    return None

  def get_average_humidity(self):
    data = self.get_average()
    if 'humidity' in data:
      return data['humidity']

    return None

  def get_average(self):
    average = {}
    for sensorid in self.sprayer['sensors'] + self.heater['sensors']:
      sensor = self.sensors[sensorid]
      sensor_type = sensor.get_type()
      if sensor_type not in average:
        average[sensor_type] = {'current' : 0.0, 'alarm_min' : 0.0, 'alarm_max' : 0.0, 'limit_min' : 0.0, 'limit_max':0.0, 'amount' : 0.0}

      average[sensor_type]['current'] += sensor.get_current()
      average[sensor_type]['alarm_min'] += sensor.get_alarm_min()
      average[sensor_type]['alarm_max'] += sensor.get_alarm_max()
      average[sensor_type]['limit_min'] += sensor.get_limit_min()
      average[sensor_type]['limit_max'] += sensor.get_limit_max()
      average[sensor_type]['amount'] += 1

    for averagetype in average:
      amount = average[averagetype]['amount']
      del(average[averagetype]['amount'])
      for field in average[averagetype]:
        average[averagetype][field] /= amount

      average[averagetype]['alarm'] = not (average[averagetype]['alarm_min'] < average[averagetype]['current'] < average[averagetype]['alarm_max'])
      average[averagetype]['amount'] = amount
      average[averagetype]['type'] = averagetype

    return average
