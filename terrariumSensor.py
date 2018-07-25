# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import datetime
import time
import os.path
import glob
import re
import ow

from hashlib import md5

from terrariumUtils import terrariumUtils, terrariumSingleton
from terrariumAnalogSensor import terrariumSKUSEN0161Sensor
from terrariumBluetoothSensor import terrariumMiFloraSensor
from terrariumGPIOSensor import terrariumYTXXSensorDigital, terrariumDHT11Sensor, terrariumDHT22Sensor, terrariumAM2302Sensor, terrariumHCSR04Sensor
from terrariumI2CSensor import terrariumSHT2XSensor, terrariumHTU21DSensor, terrariumSi7021Sensor, terrariumBME280Sensor, terrariumChirpSensor, terrariumVEML6075Sensor

class terrariumSensorCache(object):
  __metaclass__ = terrariumSingleton

  def __init__(self):
    self.__cache = {}

  def add_sensor(self,address,sensor,force = False):
    if force or address not in self.__cache:
      self.__cache[address] = sensor

  def get_sensor(self,address):
    if address in self.__cache:
      return self.__cache[address]

    return None

class terrariumRemoteSensor(object):
  hardwaretype = 'remote'

  def __init__(self,url):
    self.__url = None
    self.__value = None
    if terrariumUtils.parse_url(url) is not False:
      self.__url = url

  def __get_raw_data(self):
    if self.__url is not None:
      self.__value = terrariumUtils.get_remote_data(self.__url)

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""

  def get_current(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__value) else float(self.__value)

  def get_temperature(self):
    return self.get_current()

  def get_humidity(self):
    return self.get_current()

  def get_moisture(self):
    return self.get_current()

  def get_conductivity(self):
    return self.get_current()

  def get_distance(self):
    return self.get_current()

  def get_ph(self):
    return self.get_current()

  def get_light(self):
    return self.get_current()

  def get_uva(self):
    return self.get_current()

  def get_uvb(self):
    return self.get_current()

  def get_fertility(self):
    return self.get_current()

class terrarium1WSensor(object):
  hardwaretype = 'w1'

  W1_BASE_PATH = '/sys/bus/w1/devices/'
  W1_TEMP_REGEX = re.compile(r'(?P<type>t|f)=(?P<value>[0-9\-]+)',re.IGNORECASE)

  def __init__(self,path):
    self.__path = None
    self.__value = None
    path = os.path.join(terrarium1WSensor.W1_BASE_PATH,path,'w1_slave')
    if os.path.isfile(path):
      self.__path = path

  def __get_raw_data(self):
    if self.__path is not None and os.path.isfile(self.__path):
      with open(self.__path, 'r') as w1data:
        data = w1data.read()
        w1data = terrarium1WSensor.W1_TEMP_REGEX.search(data)
        if w1data:
          # Found data
          self.__value = float(w1data.group('value')) / 1000.0

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""

  def get_current(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__value) else float(self.__value)

  def get_temperature(self):
    return self.get_current()

  @staticmethod
  def scan():
    # Scanning w1 system bus
    for address in glob.iglob(terrarium1WSensor.W1_BASE_PATH + '[1-9][0-9]-*'):
      if not os.path.isfile(address + '/w1_slave'):
        break

      data = ''
      with open(address + '/w1_slave', 'r') as w1data:
        data = w1data.read()

      w1data = terrarium1WSensor.W1_TEMP_REGEX.search(data)
      if w1data:
        # Found valid data
        yield (os.path.basename(address),'temperature' if 't' == w1data.group('type') else 'humidity')

class terrariumOWFSSensor(object):
  hardwaretype = 'owfs'

  def __init__(self,sensor):
    self.__sensor = sensor
    #self.__sensor.useCache(True)
    self.__temperature = None
    self.__humidity = None

  def __get_raw_data(self):
    if 'temperature' in self.__sensor.entryList():
      self.__temperature = self.__sensor.temperature

    if 'humidity' in self.__sensor.entryList():
      self.__humidity = self.__sensor.humidity

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""

  def get_temperature(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__temperature) else float(self.__temperature)

  def get_humidity(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__humidity) else float(self.__humidity)

  @staticmethod
  def scan(port):
    if port > 0:
      try:
        ow.init(str(port));
        sensorsList = ow.Sensor('/').sensorList()
        for sensor in sensorsList:
          if 'temperature' in sensor.entryList():
            yield(sensor,'temperature')

          if 'humidity' in sensor.entryList():
            yield(sensor,'humidity')

      except ow.exNoController:
        logger.debug('OWFS file system is not actve / installed on this device!')
        pass

class terrariumSensor(object):
  UPDATE_TIMEOUT = 30
  ERROR_TIMEOUT = 10

  VALID_SENSOR_TYPES   = ['temperature','humidity','moisture','conductivity','distance','ph','light','uva','uvb','fertility']
  VALID_HARDWARE_TYPES = []

  # Append OWFS to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrariumOWFSSensor.hardwaretype)

  # Append remote sensor(s) to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrariumRemoteSensor.hardwaretype)

  # Append 1-wire sensor(s) to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrarium1WSensor.hardwaretype)

  # Append DHT sensor(s) to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrariumDHT11Sensor.hardwaretype)
  VALID_HARDWARE_TYPES.append(terrariumDHT22Sensor.hardwaretype)
  VALID_HARDWARE_TYPES.append(terrariumAM2302Sensor.hardwaretype)

  # Append I2C sensor(s) to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrariumSHT2XSensor.hardwaretype)
  VALID_HARDWARE_TYPES.append(terrariumHTU21DSensor.hardwaretype)
  VALID_HARDWARE_TYPES.append(terrariumSi7021Sensor.hardwaretype)
  VALID_HARDWARE_TYPES.append(terrariumBME280Sensor.hardwaretype)
  VALID_HARDWARE_TYPES.append(terrariumChirpSensor.hardwaretype)
  VALID_HARDWARE_TYPES.append(terrariumVEML6075Sensor.hardwaretype)

  # Append YTXX sensor(s) to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrariumYTXXSensorDigital.hardwaretype)

  # Append hc-sr04 sensor(s) to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrariumHCSR04Sensor.hardwaretype)

  # Appand analog sensor(s) to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrariumSKUSEN0161Sensor.hardwaretype)

  # Appand analog sensor(s) to the list of valid sensors
  VALID_HARDWARE_TYPES.append(terrariumMiFloraSensor.hardwaretype)

  def __init__(self, id, hardware_type, sensor_type, sensor, name = '', callback_indicator = None):
    self.__sensor_cache = terrariumSensorCache()

    self.id = id

    self.__miflora_firmware = None
    self.__miflora_battery = None

    self.notification = True

    self.set_hardware_type(hardware_type)
    self.set_address(sensor)
    self.set_name(name)
    self.set_type(sensor_type,callback_indicator)
    self.set_alarm_min(0)
    self.set_alarm_max(0)
    self.set_limit_min(0)
    # For hc-sr04 set at 10 meters else just '100' value
    self.set_limit_max(100000 if terrariumHCSR04Sensor.hardwaretype == self.get_hardware_type() else 100)

    # Set custom Chirp calibration values to default
    if 'chirp' == self.get_hardware_type():
      self.set_min_moist_calibration(160)
      self.set_max_moist_calibration(720)
      self.set_temperature_offset_calibration(0)

    if self.id is None:
      self.id = md5(b'' + self.get_address().replace('-','').upper() + self.get_type()).hexdigest()

    self.current = float(0)
    self.last_update = datetime.datetime.fromtimestamp(0)
    logger.info('Loaded %s %s sensor \'%s\' on location %s.' % (self.get_hardware_type(),self.get_type(),self.get_name(),self.get_address()))

    self.update()

  @staticmethod
  def scan(port,unit_indicator):
    starttime = time.time()
    logger.debug('Start scanning for temperature/humidity sensors')
    sensor_list = []

    # Scanning OWFS sensors
    if port > 0:
      for (owfssensor,owfstype) in terrariumOWFSSensor.scan(port):
        sensor_list.append(terrariumSensor(None,
                                           'owfs',
                                           owfstype,
                                           owfssensor,
                                           callback_indicator=unit_indicator))

    # Scanning w1 system bus
    for (w1sensor,w1type) in terrarium1WSensor.scan():
      sensor_list.append(terrariumSensor(None,
                                         'w1',
                                         w1type,
                                         w1sensor,
                                         callback_indicator=unit_indicator))

    # Scanning bluetooth devices
    for (sensor,sensortype) in terrariumMiFloraSensor.scan():
      sensor_list.append(terrariumSensor(None,
                                         terrariumMiFloraSensor.hardwaretype,
                                         sensortype,
                                         sensor,
                                         callback_indicator=unit_indicator))

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
        hardwaresensor = None
        address = [self.get_address(),None,None] if ',' not in self.get_address() else self.get_address().split(',')
        if len(address) == 2:
          address.append(None)

        cache_hash = md5(b'' + self.get_address().replace('-','').upper() + self.get_hardware_type()).hexdigest()
        hardwaresensor = self.__sensor_cache.get_sensor(cache_hash)

        if hardwaresensor is None:
          if terrariumRemoteSensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumRemoteSensor(address[0])
          elif terrarium1WSensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrarium1WSensor(address[0])
          elif terrariumOWFSSensor.hardwaretype == self.get_hardware_type():
            # Dirty hack for OWFS sensors.... ;)
            hardwaresensor = terrariumOWFSSensor(self.__sensor)

          elif terrariumSHT2XSensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumSHT2XSensor(address[0],address[1])
          elif terrariumHTU21DSensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumHTU21DSensor(address[0],address[1])
          elif terrariumSi7021Sensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumSi7021Sensor(address[0],address[1])
          elif terrariumBME280Sensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumBME280Sensor(address[0],address[1])
          elif terrariumVEML6075Sensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumVEML6075Sensor(address[0],address[1])

          elif terrariumChirpSensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumChirpSensor(address[0],address[1],self.get_min_moist_calibration(),
                                                                        self.get_max_moist_calibration(),
                                                                        self.get_temperature_offset_calibration())

          elif terrariumYTXXSensorDigital.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumYTXXSensorDigital(address[0],address[1])

          elif terrariumDHT11Sensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumDHT11Sensor(address[0],address[1])
          elif terrariumDHT22Sensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumDHT22Sensor(address[0],address[1])
          elif terrariumAM2302Sensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumAM2302Sensor(address[0],address[1])

          elif terrariumSKUSEN0161Sensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumSKUSEN0161Sensor(address[0],address[1])

          elif terrariumHCSR04Sensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumHCSR04Sensor(address[0],address[1],address[2])

          elif terrariumMiFloraSensor.hardwaretype == self.get_hardware_type():
            hardwaresensor = terrariumMiFloraSensor(address[0])

          self.__sensor_cache.add_sensor(cache_hash,hardwaresensor)

        if hardwaresensor is not None:
          if terrariumMiFloraSensor.hardwaretype == self.get_hardware_type():
            self.__miflora_firmware = hardwaresensor.get_firmware()
            self.__miflora_battery = hardwaresensor.get_battery()

          with hardwaresensor as sensor:
            if 'temperature' == self.get_type():
              current = sensor.get_temperature()
            elif 'humidity' == self.get_type():
              current = sensor.get_humidity()
            elif 'moisture' == self.get_type():
              current = sensor.get_moisture()
            elif 'conductivity' == self.get_type():
              current = sensor.get_conductivity()
            elif 'distance' == self.get_type():
              current = sensor.get_distance()
            elif 'ph' == self.get_type():
              current = sensor.get_ph()
            elif 'light' == self.get_type():
              current = sensor.get_light()
            elif 'uva' == self.get_type():
              current = sensor.get_uva()
            elif 'uvb' == self.get_type():
              current = sensor.get_uvb()
            elif 'fertility' == self.get_type():
              current = sensor.get_fertility()

          del hardwaresensor

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
        logger.exception(ex)

  def get_data(self):
    data = {'id' : self.get_id(),
            'hardwaretype' : self.get_hardware_type(),
            'address' : self.get_address(),
            'type' : self.get_type(),
            'indicator' : self.get_indicator(),
            'name' : self.get_name(),
            'current' : self.get_current(),
            'alarm_min' : self.get_alarm_min(),
            'alarm_max' : self.get_alarm_max(),
            'limit_min' : self.get_limit_min(),
            'limit_max' : self.get_limit_max(),
            'alarm' : self.get_alarm(),
            'error' : not self.is_active()
            }

    if 'chirp' == self.get_hardware_type():
      data['min_moist'] = self.get_min_moist_calibration()
      data['max_moist'] = self.get_max_moist_calibration()
      data['temp_offset'] = self.get_temperature_offset_calibration()

    if 'miflora' == self.get_hardware_type():
      data['firmware'] = self.__miflora_firmware
      data['battery'] = self.__miflora_battery

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
      self.__indicator = indicator

  def get_type(self):
    return self.type

  def get_indicator(self):
    # Use a callback from terrariumEngine for 'realtime' updates
    return self.__indicator(self.get_type())

  def get_address(self):
    return self.sensor_address

  def set_address(self,address):
    if isinstance(address, basestring):
      self.sensor_address = address

    elif terrariumOWFSSensor.hardwaretype == self.get_hardware_type() and not isinstance(address, basestring):
      # OW Sensor object
      self.__sensor = address
      self.sensor_address = self.__sensor.address

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

  def set_min_moist_calibration(self,limit):
    self.__min_moist = float(limit)

  def get_min_moist_calibration(self):
    return self.__min_moist

  def set_max_moist_calibration(self,limit):
    self.__max_moist = float(limit)

  def get_max_moist_calibration(self):
    return self.__max_moist

  def set_temperature_offset_calibration(self,limit):
    self.__temp_offset = float(limit)

  def get_temperature_offset_calibration(self):
    return self.__temp_offset

  def get_current(self, force = False):
    current = self.current
    indicator = self.get_indicator().lower()

    if 'f' == indicator:
      current = terrariumUtils.to_fahrenheit(self.current)
    elif 'inch' == indicator:
      current = terrariumUtils.to_inches(self.current)

    return float(current)

  def get_alarm(self):
    return not self.get_alarm_min() <= self.get_current() <= self.get_alarm_max()

  def is_active(self):
    return datetime.datetime.now() - self.last_update < datetime.timedelta(minutes=terrariumSensor.ERROR_TIMEOUT)

  def notification_enabled(self):
    return self.notification == True

  def stop(self):
    logger.info('Cleaned up sensor %s at location %s' % (self.get_name(), self.get_address()))
