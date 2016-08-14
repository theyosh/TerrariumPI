# -*- coding: utf-8 -*-
import thread
import datetime
from threading import Timer
import copy
import time

from gevent import monkey, sleep
monkey.patch_all()

class terrariumEnvironment():

  def __init__(self, sensors, power_switches, door_sensor, weather, config):
    self.config = config
    self.sensors = sensors
    self.power_switches = power_switches
    self.door_sensor = door_sensor
    self.weather = weather
    self.__load_enironment_settings()
    thread.start_new_thread(self.__engine_loop, ())

  def reload_settings(self):
    self.__load_enironment_settings()

  def __load_enironment_settings(self):
    config = self.config.get_environment()
    self.lights = config['lights']

    self.lights['enabled'] = True if self.lights['enabled'].lower() in ['true','on','1'] else False
    self.lights['on'] = int(self.lights['on'])
    self.lights['off'] = int(self.lights['off'])
    self.lights['hours_shift'] = float(self.lights['hours_shift'])
    self.lights['min_hours'] = float(self.lights['min_hours'])
    self.lights['max_hours'] = float(self.lights['max_hours'])
    self.lights['power_switches'] = self.lights['power_switches'].split(',')

    self.humidity = config['humidity']
    self.humidity['enabled'] = True if self.humidity['enabled'].lower() in ['true','on','1'] else False
    self.humidity['night_enabled'] = True if self.humidity['night_enabled'].lower() in ['true','on','1'] else False
    self.humidity['spray_duration'] = float(self.humidity['spray_duration'])
    self.humidity['spray_timeout'] = float(self.humidity['spray_timeout'])

    self.humidity['power_switches'] = self.humidity['power_switches'].split(',')
    self.humidity['sensors'] = self.humidity['sensors'].split(',')
    self.humidity['lastaction'] = datetime.datetime.now()

    self.heater = config['heater']
    self.heater['enabled'] =True if self.heater['enabled'].lower() in ['true','on','1'] else False
    self.heater['day_enabled'] = True if self.heater['day_enabled'].lower() in ['true','on','1'] else False
    self.heater['power_switches'] = self.heater['power_switches'].split(',')
    self.heater['sensors'] = self.heater['sensors'].split(',')

  def __engine_loop(self):
    while True:
      now = int(time.time())
      lights = self.get_lights_state()

      if self.lights['enabled']:
        if lights['on'] < now < lights['off']:
          self.lights_on()
        else:
          self.lights_off()

      if self.humidity['enabled']:
        humidity = self.get_humidity_state()

        if humidity['current'] < humidity['alarm_min']:
          self.waterspray_on()

      if self.heater['enabled']:
        if self.heater['day_enabled']:
          if not (self.heater['day_enabled'] and lights['on'] < now < lights['off']):
            heater = self.get_heater_state()

            if heater['current'] < heater['alarm_min']:
              self.heater_on()
            elif heater['current'] > heater['alarm_max']:
              self.heater_off()
          else:
            self.heater_off()

      sleep(60)

  def get_config(self):
    return {'lights' : self.get_light_settings(),
            'humidity' : self.get_humidity_settings() ,
            'heater' : self.get_heater_settings()}

  def get_light_settings(self):
    return self.lights

  def set_light_settings(self,data):
    for field in data:
      self.lights[field] = data[field]

    #self.__load_enironment_settings()

  def lights_on(self):
    for switch in self.lights['power_switches']:
      print 'Switch on: ' + self.power_switches[switch].get_name()
      self.power_switches[switch].on();

  def lights_off(self):
    for switch in self.lights['power_switches']:
      print 'Switch off: ' + self.power_switches[switch].get_name()
      self.power_switches[switch].off();

  def get_humidity_settings(self):
    data = copy.deepcopy(self.humidity)
    del(data['lastaction'])
    return data

  def set_humidity_settings(self,data):
    print data
    for field in data:
      self.humidity[field] = data[field]

    #self.__load_enironment_settings()

  def waterspray_on(self):
    if datetime.datetime.now() - self.humidity['lastaction'] > datetime.timedelta(seconds=self.humidity['spray_timeout']):
      for switch in self.humidity['power_switches']:
        print 'Switch on: ' + self.power_switches[switch].get_name()
        self.power_switches[switch].on();

      (Timer(self.humidity['spray_duration'], self.waterspray_off)).start()
#        t.start()
      self.humidity['lastaction'] = datetime.datetime.now()

  def waterspray_off(self):
    for switch in self.humidity['power_switches']:
      print 'Switch off: ' + self.power_switches[switch].get_name()
      self.power_switches[switch].off();

  def get_heater_settings(self):
    return self.heater

  def set_heater_settings(self,data):
    for field in data:
      self.heater[field] = data[field]

    #self.__load_enironment_settings()

  def heater_on(self):
    for switch in self.heater['power_switches']:
      print 'Switch on: ' + self.power_switches[switch].get_name()
      self.power_switches[switch].on();

  def heater_off(self):
    for switch in self.heater['power_switches']:
      print 'Switch off: ' + self.power_switches[switch].get_name()
      self.power_switches[switch].off();

  def get_lights_state(self):
    now = datetime.datetime.now()
    data = {'on' : 0, 'off' : 0}
    if 'weather' == self.lights['modus']:
      data['on'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['rise'])
      data['off'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['set'])

    elif 'timer' == self.lights['modus']:
      data['on'] = self.lights['on']
      data['off'] = self.lights['off']

    # Duration check
    duration = data['off'] - data['on']
    # Reduce the amount of hours if to much
    if duration > datetime.timedelta(hours=self.lights['max_hours']):
      duration -= datetime.timedelta(hours=self.lights['max_hours'])
      data['on'] += datetime.timedelta(seconds=duration.total_seconds()/2)
      data['off'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
    # Increase the amount of hours it to little
    elif duration < datetime.timedelta(hours=self.lights['min_hours']):
      duration = datetime.timedelta(hours=self.lights['min_hours']) - duration
      data['on'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
      data['off'] += datetime.timedelta(seconds=duration.total_seconds()/2)

    # Shift hours
    data['on'] += datetime.timedelta(hours=self.lights['hours_shift'])
    data['off'] += datetime.timedelta(hours=self.lights['hours_shift'])

    # Shift time to next day?
    if now > data['off']:
      # Past offtime, so next day
      data['on'] += datetime.timedelta(hours=24)
      data['off'] += datetime.timedelta(hours=24)

    data['on'] = time.mktime(data['on'].timetuple())
    data['off'] = time.mktime(data['off'].timetuple())

    return data

  def get_humidity_state(self):
    amount = float(len(self.humidity['sensors']))
    data = {'current' : sum(self.sensors[sensor].get_current() for sensor in self.humidity['sensors']) / amount,
            'alarm_min' : sum(self.sensors[sensor].get_alarm_min() for sensor in self.humidity['sensors']) / amount}

    return data

  def get_heater_state(self):
    amount = float(len(self.heater['sensors']))
    data = {'current' : sum(self.sensors[sensor].get_current() for sensor in self.heater['sensors']) / amount,
          'alarm_min' : sum(self.sensors[sensor].get_alarm_min() for sensor in self.heater['sensors']) / amount,
          'alarm_max' : sum(self.sensors[sensor].get_alarm_max() for sensor in self.heater['sensors']) / amount}

    return data

  def get_average_temperature(self):
    return self.get_average('temperature')

  def get_average_humidity(self):
    return self.get_average('humidity')

  def get_average(self, type = None):
    average = {'temperature' : {'current': float(0), 'alarm_min' : float(0), 'alarm_max' : float(0), 'min' : float(0), 'max' : float(0), 'amount' : float(0), 'alarm' : False},
               'humidity'    : {'current': float(0), 'alarm_min' : float(0), 'alarm_max' : float(0), 'min' : float(0), 'max' : float(0), 'amount' : float(0), 'alarm' : False}}

    for sensorid in self.sensors:
      sensor = self.sensors[sensorid]
      sensor_type = sensor.get_type()
      average[sensor_type]['current'] += sensor.get_current()
      average[sensor_type]['alarm_min'] += sensor.get_alarm_min()
      average[sensor_type]['alarm_max'] += sensor.get_alarm_max()
      average[sensor_type]['min'] += sensor.get_min()
      average[sensor_type]['max'] += sensor.get_max()
      average[sensor_type]['amount'] += 1

    for sensortype in average:
        average[sensortype]['current'] /= average[sensortype]['amount']
        average[sensortype]['alarm_min'] /= average[sensortype]['amount']
        average[sensortype]['alarm_max'] /= average[sensortype]['amount']
        average[sensortype]['min'] /= average[sensortype]['amount']
        average[sensortype]['max'] /= average[sensortype]['amount']
        average[sensortype]['alarm'] = not average[sensortype]['alarm_min'] <  average[sensortype]['current'] < average[sensortype]['alarm_max']

        del(average[sensortype]['amount'])

    if type is not None and type in average:
      return { type : average[type] }

    return average
