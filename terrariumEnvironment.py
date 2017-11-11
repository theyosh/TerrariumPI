# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import thread
import datetime
import time
import copy

from threading import Timer
from terrariumDoor import terrariumDoor

from gevent import monkey, sleep
monkey.patch_all()

class terrariumEnvironment():
  LOOP_TIMEOUT = 15

  def __init__(self, sensors, power_switches, weather, door_status, config):
    logger.debug('Init terrariumPI environment')

    self.config = config
    self.door_status = door_status

    self.sensors = sensors
    self.power_switches = power_switches

    self.weather = weather

    self.reload_config()
    thread.start_new_thread(self.__engine_loop, ())

  # Private functions
  def __parse_config(self):
    config = self.config.get_environment()

    self.light = config['light']
    if len(self.light.keys()) == 0:
      self.light = {}

    self.light['enabled']        = False if 'enabled' not in self.light else (self.light['enabled'].lower() in ['true','on','1','yes'])
    self.light['mode']           = None  if 'mode' not in self.light else self.light['mode']
    self.light['on']             = 0     if 'on' not in self.light else int(self.light['on'])
    self.light['off']            = 0     if 'off' not in self.light else int(self.light['off'])
    self.light['hours_shift']    = 0.0   if 'hours_shift' not in self.light else float(self.light['hours_shift'])
    self.light['min_hours']      = 0.0   if 'min_hours' not in self.light else float(self.light['min_hours'])
    self.light['max_hours']      = 0.0   if 'max_hours' not in self.light else float(self.light['max_hours'])
    self.light['power_switches'] = []    if ('power_switches' not in self.light or self.light['power_switches'] == '') else self.light['power_switches'].split(',')

    self.sprayer = config['sprayer']
    if len(self.sprayer.keys()) == 0:
      self.sprayer = {}

    self.sprayer['enabled']        = False if 'enabled' not in self.sprayer else (self.sprayer['enabled'].lower() in ['true','on','1','yes'])
    self.sprayer['mode']           = 'sensor'
    self.sprayer['night_enabled']  = False if 'night_enabled' not in self.sprayer else (self.sprayer['night_enabled'].lower() in ['true','on','1','yes'])
    self.sprayer['spray_duration'] = 0.0   if 'spray_duration' not in self.sprayer else float(self.sprayer['spray_duration'])
    self.sprayer['spray_timeout']  = 0.0   if 'spray_timeout' not in self.sprayer else float(self.sprayer['spray_timeout'])
    self.sprayer['power_switches'] = []    if ('power_switches' not in self.sprayer or self.sprayer['power_switches'] == '') else self.sprayer['power_switches'].split(',')
    self.sprayer['sensors']        = []    if ('sensors' not in self.sprayer or self.sprayer['sensors'] == '') else self.sprayer['sensors'].split(',')
    self.sprayer['lastaction']     = int(time.time())

    self.heater = config['heater']
    if len(self.heater.keys()) == 0:
      self.heater = {}

    self.heater['enabled']        = False if 'enabled' not in self.heater else (self.heater['enabled'].lower() in ['true','on','1','yes'])
    self.heater['mode']           = None  if 'mode' not in self.heater else self.heater['mode']
    self.heater['on']             = 0     if 'on' not in self.heater else int(self.heater['on'])
    self.heater['off']            = 0     if 'off' not in self.heater else int(self.heater['off'])
    self.heater['day_enabled']    = False if 'day_enabled' not in self.heater else (self.heater['day_enabled'].lower() in ['true','on','1','yes'])
    self.heater['power_switches'] = []    if ('power_switches' not in self.heater or self.heater['power_switches'] == '') else self.heater['power_switches'].split(',')
    self.heater['sensors']        = []    if ('sensors' not in self.heater or self.heater['sensors'] == '') else self.heater['sensors'].split(',')

    self.cooler = config['cooler']
    if len(self.cooler.keys()) == 0:
      self.cooler = {}

    self.cooler['enabled']        = False if 'enabled' not in self.cooler else (self.cooler['enabled'].lower() in ['true','on','1','yes'])
    self.cooler['mode']           = None  if 'mode' not in self.cooler else self.cooler['mode']
    self.cooler['on']             = 0     if 'on' not in self.cooler else int(self.cooler['on'])
    self.cooler['off']            = 0     if 'off' not in self.cooler else int(self.cooler['off'])
    self.cooler['night_enabled']  = False if 'night_enabled' not in self.cooler else (self.cooler['night_enabled'].lower() in ['true','on','1','yes'])
    self.cooler['power_switches'] = []    if ('power_switches' not in self.cooler or self.cooler['power_switches'] == '') else self.cooler['power_switches'].split(',')
    self.cooler['sensors']        = []    if ('sensors' not in self.cooler or self.cooler['sensors'] == '') else self.cooler['sensors'].split(',')

  def __engine_loop(self):
    while True:
      starttime = time.time()
      light = self.get_light_state()
      if light['enabled']:
        if light['on'] < int(starttime) < light['off']:
          self.light_on()
        else:
          self.light_off()

      # Reread the light status.... above check could changed it
      light = self.get_light_state()
      sprayer = self.get_sprayer_state()
      if sprayer['enabled'] and light['enabled']:
        if sprayer['night_enabled'] or light['state'] == 'on':
          if sprayer['current'] < sprayer['alarm_min']:
            # To low humidity. Put sprayer on
            if self.door_status() == terrariumDoor.CLOSED:
              # Door is closed, so we can spray
              self.sprayer_on()
              logger.info('Humdity value %f is to low. Sprayer will run for %f seconds' % (sprayer['current'],self.sprayer['spray_duration']))
            else:
              # Door is open!! Cannot spray!
              self.sprayer_off()
              logger.warning('Humdity value %f is to low. But door is open, so we cannot spray water' % sprayer['current'])
          else:
            # Humidity is ok. Make sure sprayer is off
            self.sprayer_off()
        else:
          # Lights are off and not night enabled, make sure sprayer is off
          self.sprayer_off()
      else:
        # Sprayer system disabled, make sure sprayer is off
        self.sprayer_off()

      heater = self.get_heater_state()
      if heater['enabled'] and light['enabled']:
        if heater['day_enabled'] or light['state'] == 'off':
          # Heater controll starts here...
          if heater['mode'] == 'sensor':
            # Trigger on sensor data only when lights are off
            if heater['current'] < heater['alarm_min']:
              self.heater_on()
            elif heater['current'] > heater['alarm_max']:
              self.heater_off()

          elif heater['mode'] == 'timer' or heater['mode'] == 'weather':
            # Trigger on specified time
            if heater['on'] < int(starttime) < heater['off']:
              # Are there extra sensors available
              sensor_check = len(heater['sensors']) > 0
              # When there are sensors available, the heater will start when to cold, and shutdown when to hot. This preserve some power comsumption
              if (sensor_check and heater['current'] < heater['alarm_min']) or not sensor_check:
                self.heater_on()
              elif (sensor_check and heater['current'] > heater['alarm_max']):
                self.heater_off()
            else:
              # Outside 'on' window. Shut down
              self.heater_off()
        else:
          # Heater should not be running when the ligts are on. (Default)
          self.heater_off()
      else:
        # Heater disabled, make sure it is off
        self.heater_off()

      cooler = self.get_cooler_state()
      if cooler['enabled'] and light['enabled']:
        if cooler['night_enabled'] or light['state'] == 'on':
          # Heater controll starts here...
          if cooler['mode'] == 'sensor':
            # Trigger on sensor data only when lights are off
            if cooler['current'] > cooler['alarm_max']:
              self.cooler_on()
            elif cooler['current'] < cooler['alarm_min']:
              self.cooler_off()

          elif cooler['mode'] == 'timer' or cooler['mode'] == 'weather':
            # Trigger on specified time
            if cooler['on'] < int(starttime) < cooler['off']:
              # Are there extra sensors available
              sensor_check = len(cooler['sensors']) > 0
              if (sensor_check and cooler['current'] > cooler['alarm_max']) or not sensor_check:
                self.cooler_on()
              elif (sensor_check and cooler['current'] < cooler['alarm_min']):
                self.cooler_off()
            else:
              # Outside 'on' window. Shut down
              self.cooler_off()

        else:
          # Cooler should not be running when the ligts are off. (Default)
          self.cooler_off()
      else:
        # Cooler is disabled. Make sure cooler is off
        self.cooler_off()

      duration = time.time() - starttime
      if duration < terrariumEnvironment.LOOP_TIMEOUT:
        logger.info('Engine loop done in %.5f seconds. Waiting for %.5f seconds for next round' % (duration,terrariumEnvironment.LOOP_TIMEOUT - duration))
        sleep(terrariumEnvironment.LOOP_TIMEOUT - duration) # TODO: Config setting
      else:
        logger.warning('Engine took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumEnvironment.LOOP_TIMEOUT,terrariumEnvironment.LOOP_TIMEOUT))

  def __set_config(self,part,data):
    for field in data:
      if 'light' == part:
        self.light[field] = data[field]
      elif 'sprayer' == part:
        self.sprayer[field] = data[field]
      elif 'heater' == part:
        self.heater[field] = data[field]
      elif 'cooler' == part:
        self.cooler[field] = data[field]

  def __on_off(self,part, state = None):
    is_on = True
    power_switches = []
    if 'light' == part:
      power_switches = self.light['power_switches']
    elif 'sprayer' == part:
      power_switches = self.sprayer['power_switches']
    elif 'heater' == part:
      power_switches = self.heater['power_switches']
    elif 'cooler' == part:
      power_switches = self.cooler['power_switches']

    for switch_id in power_switches:
      if switch_id not in self.power_switches:
        is_on = False
      elif state is None:
        is_on = is_on and self.power_switches[switch_id].is_on()
      else:
        if state:
          self.power_switches[switch_id].on()
        else:
          self.power_switches[switch_id].off()

        is_on = state

    return is_on

  def __switch_on(self,part):
    return True == self.__on_off(part,True)

  def __switch_off(self,part):
    return False == self.__on_off(part,False)

  def __is_on(self,part):
    return self.__on_off(part) == True

  def __is_off(self,part):
    return not self.__is_on(part)

  def __get_state(self,part):
    now = datetime.datetime.now()

    data = {}
    state_data = {}
    average = {}
    state = False

    if part == 'light':
      state_data = self.light
      state = self.is_light_on()
    elif part == 'sprayer':
      state_data = self.sprayer
      average = self.get_average_humidity()
      state = self.is_sprayer_on()
    elif part == 'heater':
      state_data = self.heater
      average = self.get_average_temperature()
      state = self.is_heater_on()
    elif part == 'cooler':
      state_data = self.cooler
      average = self.get_average_temperature()
      state = self.is_cooler_on()

    for key in state_data:
      data[key] = state_data[key]
    data.update(average)

    if 'weather' == data['mode']:
      if 'light' == part or 'cooler' == part:
        data['on'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['rise'])
        data['off'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['set'])
      elif 'heater' == part:
        data['on'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['set'])
        data['off'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['rise']) + datetime.timedelta(hours=24)

    elif 'timer' == data['mode']:
      data['on'] = datetime.datetime.fromtimestamp(state_data['on']).replace(year=int(now.strftime('%Y')),
                                                                             month=int(now.strftime('%m')),
                                                                             day=int(now.strftime('%d')))
      data['off'] = datetime.datetime.fromtimestamp(state_data['off']).replace(year=int(now.strftime('%Y')),
                                                                               month=int(now.strftime('%m')),
                                                                               day=int(now.strftime('%d')))

      if data['on'] > data['off']:
        if now > data['off']:
          data['off'] += datetime.timedelta(hours=24)
        else:
          data['on'] -= datetime.timedelta(hours=24)

    if 'light' == part and data['enabled']:
      # Duration check
      duration = data['off'] - data['on']
      # Reduce the amount of hours if to much
      if duration > datetime.timedelta(hours=state_data['max_hours']):
        duration -= datetime.timedelta(hours=state_data['max_hours'])
        data['on'] += datetime.timedelta(seconds=duration.total_seconds()/2)
        data['off'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
      # Increase the amount of hours if to little
      elif duration < datetime.timedelta(hours=state_data['min_hours']):
        duration = datetime.timedelta(hours=state_data['min_hours']) - duration
        data['on'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
        data['off'] += datetime.timedelta(seconds=duration.total_seconds()/2)

      # Shift hours
      data['on'] += datetime.timedelta(hours=state_data['hours_shift'])
      data['off'] += datetime.timedelta(hours=state_data['hours_shift'])

    # Shift time to next day?
    if 'weather' == data['mode'] or 'timer' == data['mode']:
      if now > data['off']:
        # Past offtime, so next day
        data['on'] += datetime.timedelta(hours=24)
        data['off'] += datetime.timedelta(hours=24)

      data['on'] = time.mktime(data['on'].timetuple())
      data['off'] = time.mktime(data['off'].timetuple())

    # Reset alarm for to high mudity and sprayer, to hot and heater, or to cool and cooling
    if 'alarm' not in data or \
       (part in ['sprayer','heater'] and data['current'] >= data['alarm_max']) or \
       (part == 'cooler'  and data['current'] <= data['alarm_max']):
      data['alarm'] = False

    data['state'] = 'on' if state else 'off'
    return data
  # End private functions

  # System functions
  def set_power_switches(self,data):
    self.power_switches = data
    self.reload_config()

  def set_sensors(self,data):
    self.sensors = data
    self.reload_config()

  def get_config(self):
    return {'light'   : self.get_light_config(),
            'sprayer' : self.get_sprayer_config() ,
            'heater'  : self.get_heater_config(),
            'cooler'  : self.get_cooler_config()}

  def reload_config(self):
    self.__parse_config()

  def get_average_temperature(self):
    data = self.get_average()
    if 'temperature' in data:
      return data['temperature']

    return {'current'   : 0.0,
            'alarm_min' : 0.0,
            'alarm_max' : 0.0,
            'limit_min' : 0.0,
            'limit_max' : 0.0,
            'amount'    : 0.0,
            'alarm'     : False}


  def get_average_humidity(self):
    data = self.get_average()
    if 'humidity' in data:
      return data['humidity']

    return {'current'   : 0.0,
            'alarm_min' : 0.0,
            'alarm_max' : 0.0,
            'limit_min' : 0.0,
            'limit_max' : 0.0,
            'amount'    : 0.0,
            'alarm'     : False}

  def get_average(self):
    average = {}
    # Make a set, in order to get a list of unique sensorids. In other words, set will remove duplicate sensorids
    for sensorid in set(self.sprayer['sensors'] + self.heater['sensors'] + self.cooler['sensors']):
      if sensorid not in self.sensors:
        part = ''
        if sensorid in self.sprayer['sensors']:
          part += 'sprayer,'
        if sensorid in self.heater['sensors']:
          part += 'heater,'
        if sensorid in self.cooler['sensors']:
          part += 'cooler,'

        part = part[:-1]

        logger.error('Error getting average data from sensor with id %s. Sensor is specified in \'%s\' part, but the sensor is not known anymore in confg' % (sensorid,part))
        continue

      sensor = self.sensors[sensorid]
      sensor_type = sensor.get_type()

      if sensor_type not in average:
        average[sensor_type] = {'current'   : 0.0,
                                'alarm_min' : 0.0,
                                'alarm_max' : 0.0,
                                'limit_min' : 0.0,
                                'limit_max' : 0.0,
                                'amount'    : 0.0,
                                'alarm'     : False}

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
  # End system functions


  # Light functions
  def get_light_config(self):
    data = copy.deepcopy(self.light)
    return data

  def set_light_config(self,data):
    self.__set_config('light',data)

  def light_on(self):
    return self.__switch_on('light')

  def light_off(self):
    return self.__switch_off('light')

  def is_light_on(self):
    return self.__is_on('light')

  def is_light_off(self):
    return self.__is_off('light')

  def get_light_state(self):
    return self.__get_state('light')
  # End light functions


  # Sprayer functions
  def get_sprayer_config(self):
    data = copy.deepcopy(self.sprayer)
    if 'lastaction' in data:
      del(data['lastaction'])
    return data

  def set_sprayer_config(self,data):
    self.__set_config('sprayer',data)

  def sprayer_on(self):
    if int(time.time()) - self.sprayer['lastaction'] > self.sprayer['spray_timeout']:
      self.__switch_on('sprayer')
      (Timer(self.sprayer['spray_duration'], self.sprayer_off)).start()
      self.sprayer['lastaction'] = int(time.time())

  def sprayer_off(self):
    self.__switch_off('sprayer')

  def is_sprayer_on(self):
    return self.__is_on('sprayer')

  def is_sprayer_off(self):
    return self.__is_off('sprayer')

  def get_sprayer_state(self):
    return self.__get_state('sprayer')
  # End sprayer functions


  # Heater functions
  def get_heater_config(self):
    data = copy.deepcopy(self.heater)
    return data

  def set_heater_config(self,data):
    self.__set_config('heater',data)

  def heater_on(self):
    self.__switch_on('heater')

  def heater_off(self):
    self.__switch_off('heater')

  def is_heater_on(self):
    return self.__is_on('heater')

  def is_heater_off(self):
    return self.__is_off('heater')

  def get_heater_state(self):
    return self.__get_state('heater')
  # End heater functions


  # Cooler functions
  def get_cooler_config(self):
    data = copy.deepcopy(self.cooler)
    return data

  def set_cooler_config(self,data):
    self.__set_config('cooler',data)

  def cooler_on(self):
    self.__switch_on('cooler')

  def cooler_off(self):
    self.__switch_off('cooler')

  def is_cooler_on(self):
    return self.__is_on('cooler')

  def is_cooler_off(self):
    return self.__is_off('cooler')

  def get_cooler_state(self):
    return self.__get_state('cooler')
  # End cooler functions
