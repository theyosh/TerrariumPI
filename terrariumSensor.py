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
import RPi.GPIO as GPIO

from hashlib import md5
from terrariumUtils import terrariumUtils

class terrariumSensor:
  UPDATE_TIMEOUT = 30
  VALID_SENSOR_TYPES   = ['temperature','humidity','distance']
  VALID_DHT_SENSORS    = { 'dht11' : dht.DHT11,
                           'dht22' : dht.DHT22,
                           'am2302': dht.AM2302 }
  VALID_HARDWARE_TYPES = ['owfs','w1','remote','hc-sr04'] + VALID_DHT_SENSORS.keys()

  W1_BASE_PATH = '/sys/bus/w1/devices/'
  W1_TEMP_REGEX = re.compile(r'(?P<type>t|f)=(?P<value>[0-9]+)',re.IGNORECASE)

  def __init__(self, id, hardware_type, sensor_type, sensor, name = '', indicator = None):
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
    elif self.get_hardware_type() == 'hc-sr04':
      # Adafruit_DHT
      #self.sensor = dht
      # Dirty hack to replace OWFS sensor object for GPIO pin nr
      sensor = sensor.split(',')
      self.sensor_address = {'TRIG' : sensor[0] , 'ECHO' : sensor[1]}
      GPIO.setmode(GPIO.BCM)
      try:
        GPIO.setup(terrariumUtils.to_BCM_port_number(self.sensor_address['TRIG']),GPIO.OUT)
        GPIO.setup(terrariumUtils.to_BCM_port_number(self.sensor_address['ECHO']),GPIO.IN)

      except Exception, err:
        logger.warning(err)
        pass


    elif 'remote' == self.get_hardware_type():
      self.sensor_address = sensor

    self.set_name(name)
    self.set_type(sensor_type,indicator)
    self.set_alarm_min(0)
    self.set_alarm_max(0)
    self.set_limit_min(0)
    self.set_limit_max(100)
    if self.get_hardware_type() == 'hc-sr04':
      # Limit 10 meters
      self.set_limit_max(100000)

    if self.id is None:
      self.id = md5(b'' + self.get_address().replace('-','').upper() + self.get_type()).hexdigest()

    self.current = float(0)
    self.last_update = datetime.datetime.fromtimestamp(0)
    logger.info('Loaded %s %s sensor \'%s\' on location %s.' % (self.get_hardware_type(),self.get_type(),self.get_name(),self.get_address()))
    self.update()

  @staticmethod
  def scan(port,temperature_indicator): # TODO: Wants a callback per sensor here....?
    starttime = time.time()
    logger.debug('Start scanning for temperature/humidity sensors')
    sensor_list = []

    if port > 0:
      try:
        ow.init(str(port));
        sensorsList = ow.Sensor('/').sensorList()
        for sensor in sensorsList:
          if 'temperature' in sensor.entryList():
            sensor_list.append(terrariumSensor(None,
                                            'owfs',
                                            'temperature',
                                            sensor,
                                            indicator=temperature_indicator))

          if 'humidity' in sensor.entryList():
            sensor_list.append(terrariumSensor(None,
                                           'owfs',
                                          'humidity',
                                          sensor))

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
        sensor_list.append(terrariumSensor(None,
                                       'w1',
                                       ('temperature' if w1data.group('type') == 't' else 'humidity'),
                                       address.replace(terrariumSensor.W1_BASE_PATH,''),
                                       indicator=temperature_indicator))

    logger.info('Found %d temperature/humidity sensors in %.5f seconds' % (len(sensor_list),time.time() - starttime))
    return sensor_list

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

        elif 'hc-sr04' == self.get_hardware_type():
          GPIO.output(terrariumUtils.to_BCM_port_number(self.sensor_address['TRIG']), False)
          time.sleep(2)
          GPIO.output(terrariumUtils.to_BCM_port_number(self.sensor_address['TRIG']), True)
          time.sleep(0.00001)
          GPIO.output(terrariumUtils.to_BCM_port_number(self.sensor_address['TRIG']), False)
          while GPIO.input(terrariumUtils.to_BCM_port_number(self.sensor_address['ECHO']))==0:
            pulse_start = time.time()
          while GPIO.input(terrariumUtils.to_BCM_port_number(self.sensor_address['ECHO']))==1:
            pulse_end = time.time()

          pulse_duration = pulse_end - pulse_start
          # Measure in millimetre
          current = round(pulse_duration * 171500,2)

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
      except Exception, ex:
        print ex
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

    if self.get_type() == 'distance':
      return 'mm'

    return self.indicator().upper()

  def get_address(self):
    address = self.sensor_address
    if self.get_hardware_type() == 'hc-sr04':
      address = str(self.sensor_address['TRIG']) + ',' + str(self.sensor_address['ECHO'])

    return address

  def set_address(self,address):
    # Can't set OWFS or W1 sensor addresses. This is done by the OWFS software or kernel OS
    if self.get_hardware_type() not in ['owfs','w1']:
      self.sensor_address = address

      if self.get_hardware_type() == 'hc-sr04':
        sensor = address.split(',')
        self.sensor_address = {'TRIG' : int(sensor[0]) , 'ECHO' : int(sensor[1])}
        GPIO.setmode(GPIO.BCM)
        try:
          GPIO.setup(self.sensor_address['TRIG'],GPIO.OUT)
          GPIO.setup(self.sensor_address['ECHO'],GPIO.IN)

        except Exception, err:
          logger.warning(err)
          pass

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
