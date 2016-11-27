# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from datetime import datetime, timedelta
from hashlib import md5
import ow

class terrariumSensor:
  valid_sensor_types = ['temperature','humidity']

  def __init__(self, id, type, sensor, name = '', alarm_min = 0, alarm_max = 0, min = 0, max = 100):
    logger.debug('Initializing sensor of type: %s' % (type,))
    self.id = id
    self.type = str(type)
    # OW Sensor object
    self.sensor = sensor
    self.sensor.useCache(True)
    self.sensor_address = self.sensor.address

    self.set_name(name)
    self.set_min(min)
    self.set_max(max)
    self.set_alarm_min(alarm_min)
    self.set_alarm_max(alarm_max)

    self.current = float(0)

    self.last_update = datetime.fromtimestamp(0)
    self.update_timeout = 30 #TODO: Config setting

    logger.info('Loaded %s sensor %s on location %s with values: minimal value %s, maximal value %s, alarm low value %s, alarm high value %s' %
                (self.get_type(),
                 self.get_name(),
                 self.get_address(),
                 str(self.get_min()) + self.get_indicator(),
                 str(self.get_max()) + self.get_indicator(),
                 str(self.get_alarm_min()) + self.get_indicator(),
                 str(self.get_alarm_max()) + self.get_indicator()
                ))

    self.update()

  @staticmethod
  def scan(port,config): # TODO: Wants a callback per sensor here....?
    logger.info('Start scanning for temperature/humidity sensors')
    sensors = []
    try:
      ow.init(str(port));
      sensorsList = ow.Sensor('/').sensorList()
      for sensor in sensorsList:
        sensor_config = {}
        if 'temperature' in sensor.entryList():
          sensor_id = md5(b'' + sensor.address + 'temperature').hexdigest()
          if sensor_id in config:
            sensor_config = config[sensor_id]

          sensors.append(terrariumSensor( sensor_id,
                                          'temperature',
                                          sensor,
                                          sensor_config['name'] if 'name' in sensor_config else '',
                                          sensor_config['alarm_min'] if 'alarm_min' in sensor_config else 0,
                                          sensor_config['alarm_max'] if 'alarm_max' in sensor_config else 0,
                                          sensor_config['min'] if 'min' in sensor_config else 0,
                                          sensor_config['max'] if 'max' in sensor_config else 100))

        if 'humidity' in sensor.entryList():
          sensor_id = md5(b'' + sensor.address + 'humidity').hexdigest()
          if sensor_id in config:
            sensor_config = config[sensor_id]

          sensors.append(terrariumSensor(sensor_id,
                                        'humidity',
                                        sensor,
                                        sensor_config['name'] if 'name' in sensor_config else '',
                                        sensor_config['alarm_min'] if 'alarm_min' in sensor_config else 0,
                                        sensor_config['alarm_max'] if 'alarm_max' in sensor_config else 0,
                                        sensor_config['min'] if 'min' in sensor_config else 0,
                                        sensor_config['max'] if 'max' in sensor_config else 100))

    except ow.exNoController:
      message = '1 Wire file system is not actve / installed on this device!'
      print message
      pass

    logger.info('Found %s temperature/humidity sensors' % (len(sensors)))
    return sensors

  def update(self, force = False):
    now = datetime.now()
    if now - self.last_update > timedelta(seconds=self.update_timeout) or force:
      logger.debug('Updating %s sensor %s' % (self.get_type(), self.get_name()))
      old_current = self.get_current()
      try:
        if 'temperature' == self.get_type():
          self.current = float(self.sensor.temperature)
        elif 'humidity' == self.get_type():
          self.current = float(self.sensor.humidity)
        self.last_update = now
        logger.info('Updated %s sensor %s from %s to %s' % (self.get_type(),
                                                            self.get_name(),
                                                            str(old_current) + self.get_indicator(),
                                                            str(self.get_current()) + self.get_indicator()))
      except Exception, err:
        # error.... don't update
        print err
        pass

  def get_data(self):
    data = {'id' : self.get_id(),
            'address' : self.get_address(),
            'type' : self.get_type(),
            'name' : self.get_name(),
            'current' : self.get_current(),
            'alarm_min' : self.get_alarm_min(),
            'alarm_max' : self.get_alarm_max(),
            'min' : self.get_min(),
            'max' : self.get_max(),
            'alarm' : self.get_alarm()
            }

    return data

  def get_id(self):
    return self.id

  def get_type(self):
    return self.type

  def get_indicator(self):
    indicators = {'temperature' : 'C',
                  'humidity' : '%'}
    return indicators[self.get_type()]

  def get_address(self):
    return self.sensor_address

  def set_name(self,name):
    self.name = str(name)

  def get_name(self):
    return self.name

  def get_alarm_min(self):
    return self.alarm_min

  def set_alarm_min(self,limit):
    self.alarm_min = float(limit)

  def get_alarm_max(self):
    return self.alarm_max

  def set_alarm_max(self,limit):
    self.alarm_max = float(limit)

  def get_min(self):
    return self.min

  def set_min(self,limit):
    self.min = float(limit)

  def get_max(self):
    return self.max

  def set_max(self,limit):
    self.max = float(limit)

  def get_current(self, force = False):
    return self.current

  def get_alarm(self):
    return not self.get_alarm_min() < self.get_current() < self.get_alarm_max()
