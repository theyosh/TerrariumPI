# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from datetime import datetime, timedelta
import time
from hashlib import md5
import ow
import Adafruit_DHT as dht
import glob
import re

class terrariumSensor:
  valid_hardware_types = ['owfs','w1']
  valid_sensor_types   = ['temperature','humidity']
  valid_dht_sensors    = { 'dht11' : dht.DHT11,
                           'dht22' : dht.DHT22,
                           'am2302': dht.AM2302 }
  valid_hardware_types += valid_dht_sensors.keys()
  valid_indicators     = {'temperature' : 'C',
                          'humidity' : '%'}

  w1_base_path = '/sys/bus/w1/devices/'
  w1_temp_regex = re.compile(r'(?P<type>t|f)=(?P<value>[0-9]+)',re.IGNORECASE)

  def __init__(self, id, hardware_type, sensor_type, sensor, name = '', alarm_min = 0, alarm_max = 0, limit_min = 0, limit_max = 100):
    self.id = id
    self.set_hardware_type(hardware_type)

    if self.get_hardware_type() == 'owfs':
      # OW Sensor object
      self.sensor = sensor
      self.sensor.useCache(True)
      self.sensor_address = self.sensor.address
    elif self.get_hardware_type() == 'w1':
      # Dirty hack to replace OWFS sensor object for W1 path
      self.sensor_address = sensor
    elif self.get_hardware_type() in terrariumSensor.valid_dht_sensors.keys():
      # Adafruit_DHT
      self.sensor = dht
      # Dirty hack to replace OWFS sensor object for GPIO pin nr
      self.sensor_address = sensor

    self.set_name(name)
    self.set_type(sensor_type)
    self.set_alarm_min(alarm_min)
    self.set_alarm_max(alarm_max)
    self.set_limit_min(limit_min)
    self.set_limit_max(limit_max)

    if self.id is None:
      self.id = md5(b'' + self.get_address() + self.get_type()).hexdigest()

    self.current = float(0)

    self.last_update = datetime.fromtimestamp(0)
    self.update_timeout = 30 #TODO: Config setting

    logger.info('Loaded %s %s sensor \'%s\' on location %s with minimal value %.2f%s, maximum value %.2f%s, alarm low value %.2f%s, alarm high value %.2f%s' %
                (self.get_hardware_type(),
                 self.get_type(),
                 self.get_name(),
                 self.get_address(),
                 self.get_limit_min(),
                 self.get_indicator(),
                 self.get_limit_max(),
                 self.get_indicator(),
                 self.get_alarm_min(),
                 self.get_indicator(),
                 self.get_alarm_max(),
                 self.get_indicator()
                ))

    self.update()

  @staticmethod
  def scan(port,config): # TODO: Wants a callback per sensor here....?
    logger.debug('Start scanning for temperature/humidity sensors')
    sensors = []
    done_sensors = []

    if port > 0:
      try:
        ow.init(str(port));
        sensorsList = ow.Sensor('/').sensorList()
        for sensor in sensorsList:
          if 'temperature' in sensor.entryList():
            sensor_id = md5(b'' + sensor.address + 'temperature').hexdigest()
            sensor_config = {}
            if sensor_id in config:
              sensor_config = config[sensor_id]
              done_sensors.append(sensor_id)

            sensors.append(terrariumSensor( sensor_id,
                                            'owfs',
                                            'temperature',
                                            sensor,
                                            sensor_config['name'] if 'name' in sensor_config else '',
                                            sensor_config['alarm_min'] if 'alarm_min' in sensor_config else 0,
                                            sensor_config['alarm_max'] if 'alarm_max' in sensor_config else 0,
                                            sensor_config['limit_min'] if 'limit_min' in sensor_config else 0,
                                            sensor_config['limit_max'] if 'limit_max' in sensor_config else 100))

          if 'humidity' in sensor.entryList():
            sensor_id = md5(b'' + sensor.address + 'humidity').hexdigest()
            sensor_config = {}
            if sensor_id in config:
              sensor_config = config[sensor_id]
              done_sensors.append(sensor_id)

            sensors.append(terrariumSensor(sensor_id,
                                           'owfs',
                                          'humidity',
                                          sensor,
                                          sensor_config['name'] if 'name' in sensor_config else '',
                                          sensor_config['alarm_min'] if 'alarm_min' in sensor_config else 0,
                                          sensor_config['alarm_max'] if 'alarm_max' in sensor_config else 0,
                                          sensor_config['limit_min'] if 'limit_min' in sensor_config else 0,
                                          sensor_config['limit_max'] if 'limit_max' in sensor_config else 100))

      except ow.exNoController:
        logger.debug('OWFS file system is not actve / installed on this device!')
        pass

    # Scanning w1 system bus
    for address in glob.iglob(terrariumSensor.w1_base_path + '[1-9][0-9]-*'):
      data = ''
      with open(address + '/w1_slave', 'r') as w1data:
        data = w1data.read()

      w1data = terrariumSensor.w1_temp_regex.search(data)
      if w1data:
        # Found valid data
        sensor_type = ('temperature' if w1data.group('type') == 't' else 'humidity')
        # We expect temperature in Celcius degrees
        sensor_value = float(w1data.group('value')) / 1000
        sensor_id = md5(b'' + address.replace(terrariumSensor.w1_base_path,'').replace('-','').upper() + sensor_type).hexdigest()

        sensor_config = {}
        if sensor_id in config:
          sensor_config = config[sensor_id]
          done_sensors.append(sensor_id)

        sensors.append(terrariumSensor(sensor_id,
                                       'w1',
                                       sensor_config['type'] if 'type' in sensor_config else sensor_type,
                                       sensor_config['address'] if 'address' in sensor_config else address.replace(terrariumSensor.w1_base_path,''),
                                       sensor_config['name'] if 'name' in sensor_config else '',
                                       sensor_config['alarm_min'] if 'alarm_min' in sensor_config else 0,
                                       sensor_config['alarm_max'] if 'alarm_max' in sensor_config else 0,
                                       sensor_config['limit_min'] if 'limit_min' in sensor_config else 0,
                                       sensor_config['limit_max'] if 'limit_max' in sensor_config else 100))

    # 'Scanning' for GPIO sensors. These are the remaining sensors based on config
    for sensor_id in set(config.keys()) - set(done_sensors):
      sensor_config = {}
      if sensor_id in config:
        sensor_config = config[sensor_id]

      sensors.append(terrariumSensor(sensor_id,
                                      sensor_config['hardwaretype'] if 'hardwaretype' in sensor_config else 'dht22',
                                      sensor_config['type'] if 'type' in sensor_config else 'temperature',
                                      sensor_config['address'] if 'address' in sensor_config else 1,
                                      sensor_config['name'] if 'name' in sensor_config else '',
                                      sensor_config['alarm_min'] if 'alarm_min' in sensor_config else 0,
                                      sensor_config['alarm_max'] if 'alarm_max' in sensor_config else 0,
                                      sensor_config['limit_min'] if 'limit_min' in sensor_config else 0,
                                      sensor_config['limit_max'] if 'limit_max' in sensor_config else 100))

    logger.debug('Found %d temperature/humidity sensors' % (len(sensors)))
    return sensors

  def update(self, force = False):
    now = datetime.now()
    if now - self.last_update > timedelta(seconds=self.update_timeout) or force:
      logger.debug('Updating %s %s sensor \'%s\'' % (self.get_hardware_type(),self.get_type(), self.get_name()))
      old_current = self.get_current()
      current = None
      try:
        starttime = time.time()
        if 'temperature' == self.get_type():
          if self.get_hardware_type() == 'owfs':
            current = float(self.sensor.temperature)
          elif self.get_hardware_type() == 'w1':
            data = ''
            with open(terrariumSensor.w1_base_path + self.get_address() + '/w1_slave', 'r') as w1data:
              data = w1data.read()

            w1data = terrariumSensor.w1_temp_regex.search(data)
            if w1data:
              # Found data
              temperature = float(w1data.group('value')) / 1000
              current = float(temperature)
          elif self.get_hardware_type() in terrariumSensor.valid_dht_sensors.keys():
            humidity, temperature = self.sensor.read_retry(terrariumSensor.valid_dht_sensors[self.get_hardware_type()], self.sensor_address)
            current = float(temperature)
        elif 'humidity' == self.get_type():
          if self.get_hardware_type() == 'owfs':
            current = float(self.sensor.humidity)
          elif self.get_hardware_type() == 'w1':
            # Not tested / No hardware to test with
            pass
          elif self.get_hardware_type() in terrariumSensor.valid_dht_sensors.keys():
            humidity, temperature = self.sensor.read_retry(terrariumSensor.valid_dht_sensors[self.get_hardware_type()], self.sensor_address)
            current = float(humidity)

        if current is None or not (self.get_limit_min() < current < self.get_limit_max()):
          # Invalid current value.... log and ingore
          logger.warn('Error on %s sensor \'%s\'! Got invalid value %f%s in %.5f seconds' % (self.get_type(),
                                                                                             self.get_name(),
                                                                                             current,
                                                                                             self.get_indicator(),
                                                                                             time.time()-starttime))

        else:
          self.current = current
          self.last_update = now
          logger.info('Updated %s sensor \'%s\' from %.2f%s to %.2f%s in %.5f seconds' % (self.get_type(),
                                                                                          self.get_name(),
                                                                                          old_current,
                                                                                          self.get_indicator(),
                                                                                          self.get_current(),
                                                                                          self.get_indicator(),
                                                                                          time.time()-starttime))
      except Exception, err:
        logger.error('Error updating %s %s sensor \'%s\' with error: %s' % (self.get_hardware_type(),
                                                                            self.get_type(),
                                                                            self.get_name(),
                                                                            err))
        pass

  def get_data(self):
    data = {'id' : self.get_id(),
            'hardwaretype' : self.get_hardware_type(),
            'address' : self.get_address(),
            'type' : self.get_type(),
            'name' : self.get_name(),
            'current' : self.get_current(),
            'alarm_min' : self.get_alarm_min(),
            'alarm_max' : self.get_alarm_max(),
            'limit_min' : self.get_limit_min(),
            'limit_max' : self.get_limit_max(),
            'alarm' : self.get_alarm()
            }

    return data

  def get_id(self):
    return self.id

  def get_hardware_type(self):
    return self.hardwaretype

  def set_hardware_type(self,type):
    if type in terrariumSensor.valid_hardware_types:
      self.hardwaretype = type

  def set_type(self,type):
    if type in terrariumSensor.valid_sensor_types:
      self.type = type

  def get_type(self):
    return self.type

  def get_indicator(self):
    return terrariumSensor.valid_indicators[self.get_type()]

  def get_address(self):
    return self.sensor_address

  def set_address(self,address):
    # Can't set OWFS or W1 sensor addresses. This is done by the OWFS software or kernel OS
    if self.get_hardware_type() not in  ['owfs','w1']:
      self.sensor_address = address

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

  def get_limit_min(self):
    return self.limit_min

  def set_limit_min(self,limit):
    self.limit_min = float(limit)

  def get_limit_max(self):
    return self.limit_max

  def set_limit_max(self,limit):
    self.limit_max = float(limit)

  def get_current(self, force = False):
    return self.current

  def get_alarm(self):
    return not self.get_alarm_min() < self.get_current() < self.get_alarm_max()
