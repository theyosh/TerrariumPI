# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import datetime
import time
import ow
import Adafruit_DHT as dht
import glob
import re
import requests

from hashlib import md5
from terrariumUtils import terrariumUtils

class terrariumSensor:
  UPDATE_TIMEOUT = 30
  VALID_SENSOR_TYPES   = ['temperature','humidity']
  VALID_DHT_SENSORS    = { 'dht11' : dht.DHT11,
                           'dht22' : dht.DHT22,
                           'am2302': dht.AM2302 }
  VALID_HARDWARE_TYPES = ['owfs','w1','remote'] + VALID_DHT_SENSORS.keys()

  W1_BASE_PATH = '/sys/bus/w1/devices/'
  W1_TEMP_REGEX = re.compile(r'(?P<type>t|f)=(?P<value>[0-9]+)',re.IGNORECASE)

  def __init__(self, id, hardware_type, sensor_type, sensor, name = '', alarm_min = 0, alarm_max = 0, limit_min = 0, limit_max = 100, indicator = None):
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
    elif self.get_hardware_type() in terrariumSensor.VALID_DHT_SENSORS.keys():
      # Adafruit_DHT
      self.sensor = dht
      # Dirty hack to replace OWFS sensor object for GPIO pin nr
      self.sensor_address = sensor
    elif 'remote' == self.get_hardware_type():
      self.sensor_address = sensor

    self.set_name(name)
    self.set_type(sensor_type,indicator)
    self.set_alarm_min(alarm_min)
    self.set_alarm_max(alarm_max)
    self.set_limit_min(limit_min)
    self.set_limit_max(limit_max)

    if self.id is None:
      self.id = md5(b'' + self.get_address().replace('-','').upper() + self.get_type()).hexdigest()

    self.current = float(0)

    self.last_update = datetime.datetime.fromtimestamp(0)

    logger.info('Loaded %s %s sensor \'%s\' on location %s with minimum value %.2f%s, maximum value %.2f%s, alarm low value %.2f%s, alarm high value %.2f%s' %
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
  def scan(port,config,temperature_indicator): # TODO: Wants a callback per sensor here....?
    starttime = time.time()
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
                                            sensor_config['limit_max'] if 'limit_max' in sensor_config else 100,
                                            temperature_indicator))

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
    for address in glob.iglob(terrariumSensor.W1_BASE_PATH + '[1-9][0-9]-*'):
      data = ''
      with open(address + '/w1_slave', 'r') as w1data:
        data = w1data.read()

      w1data = terrariumSensor.W1_TEMP_REGEX.search(data)
      if w1data:
        # Found valid data
        sensor_type = ('temperature' if w1data.group('type') == 't' else 'humidity')
        sensor_address = address.replace(terrariumSensor.W1_BASE_PATH,'')
        sensor_id = md5(b'' + sensor_address.replace('-','').upper() + sensor_type).hexdigest()

        sensor_config = {}
        if sensor_id in config:
          sensor_config = config[sensor_id]
          done_sensors.append(sensor_id)

        sensors.append(terrariumSensor(sensor_id,
                                       'w1',
                                       sensor_config['type'] if 'type' in sensor_config else sensor_type,
                                       sensor_config['address'] if 'address' in sensor_config else sensor_address,
                                       sensor_config['name'] if 'name' in sensor_config else '',
                                       sensor_config['alarm_min'] if 'alarm_min' in sensor_config else 0,
                                       sensor_config['alarm_max'] if 'alarm_max' in sensor_config else 0,
                                       sensor_config['limit_min'] if 'limit_min' in sensor_config else 0,
                                       sensor_config['limit_max'] if 'limit_max' in sensor_config else 100,
                                       temperature_indicator))

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
                                      sensor_config['limit_max'] if 'limit_max' in sensor_config else 100,
                                      temperature_indicator))

    logger.info('Found %d temperature/humidity sensors in %.5f seconds' % (len(sensors),time.time() - starttime))
    return sensors

  def update(self, force = False):
    now = datetime.datetime.now()
    if now - self.last_update > datetime.timedelta(seconds=terrariumSensor.UPDATE_TIMEOUT) or force:
      logger.debug('Updating %s %s sensor \'%s\'' % (self.get_hardware_type(),self.get_type(), self.get_name()))
      old_current = self.get_current()
      current = None
      try:
        starttime = time.time()
        if 'remote' == self.get_hardware_type():
          url_data = terrariumUtils.parse_url(self.get_address())
          if url_data is False:
            logger.error('Remote url \'%s\' for sensor \'%s\' is not a valid remote source url!' % (self.get_address(),self.get_name()))
          else:
            data = requests.get(self.get_address(),auth=(url_data['username'],url_data['password']),timeout=3)

            if data.status_code == 200:
              data = data.json()
              json_path = url_data['fragment'].split('/') if 'fragment' in url_data and url_data['fragment'] is not None else []

              for item in json_path:
                # Dirty hack to process array data....
                try:
                  item = int(item)
                except Exception, ex:
                  item = str(item)

                data = data[item]
              current = float(data)
            else:
              logger.warning('Remote sensor \'%s\' got error from remote source \'%s\': %s' % (self.get_name(),self.get_address(),data.status_code))

        elif 'temperature' == self.get_type():
          if self.get_hardware_type() == 'owfs':
            current = float(self.sensor.temperature)

          elif self.get_hardware_type() == 'w1':
            data = ''
            with open(terrariumSensor.W1_BASE_PATH + self.get_address() + '/w1_slave', 'r') as w1data:
              data = w1data.read()

            w1data = terrariumSensor.W1_TEMP_REGEX.search(data)
            if w1data:
              # Found data
              current = float(w1data.group('value')) / 1000
          elif self.get_hardware_type() in terrariumSensor.VALID_DHT_SENSORS.keys():
            humidity, temperature = self.sensor.read_retry(terrariumSensor.VALID_DHT_SENSORS[self.get_hardware_type()],
                                                           float(terrariumUtils.to_BCM_port_number(self.sensor_address)),
                                                           5)
            if temperature is not None:
              current = float(temperature)

        elif 'humidity' == self.get_type():
          if self.get_hardware_type() == 'owfs':
            current = float(self.sensor.humidity)

          elif self.get_hardware_type() == 'w1':
            # Not tested / No hardware to test with
            pass

          elif self.get_hardware_type() in terrariumSensor.VALID_DHT_SENSORS.keys():
            humidity, temperature = self.sensor.read_retry(terrariumSensor.VALID_DHT_SENSORS[self.get_hardware_type()],
                                                           float(terrariumUtils.to_BCM_port_number(self.sensor_address)),
                                                           5)
            if humidity is not None:
              current = float(humidity)

        if current is None or not (self.get_limit_min() <= current <= self.get_limit_max()):
          # Invalid current value.... log and ingore
          logger.warn('Measured value %s%s from %s sensor \'%s\' is outside valid range %.2f%s - %.2f%s in %.5f seconds.' % (current,
                                                                                                                             self.get_indicator(),
                                                                                                                             self.get_type(),
                                                                                                                             self.get_name(),
                                                                                                                             self.get_limit_min(),
                                                                                                                             self.get_indicator(),
                                                                                                                             self.get_limit_max(),
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
      except Exception:
        logger.exception('Error updating %s %s sensor \'%s\' with error:' % (self.get_hardware_type(),
                                                                              self.get_type(),
                                                                              self.get_name()))

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
    if type in terrariumSensor.VALID_HARDWARE_TYPES:
      self.hardwaretype = type

  def set_type(self,type,indicator):
    if type in terrariumSensor.VALID_SENSOR_TYPES:
      self.type = type
      self.indicator = indicator

  def get_type(self):
    return self.type

  def get_indicator(self):
    # Use a callback from terrariumEngine for 'realtime' updates
    if self.get_type() == 'humidity':
      return '%'

    return self.indicator().upper()

  def get_address(self):
    return self.sensor_address

  def set_address(self,address):
    # Can't set OWFS or W1 sensor addresses. This is done by the OWFS software or kernel OS
    if self.get_hardware_type() not in ['owfs','w1']:
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
    return float(terrariumUtils.to_fahrenheit(self.current) if self.get_indicator() == 'F' else self.current)

  def get_alarm(self):
    return not self.get_alarm_min() < self.get_current() < self.get_alarm_max()
