# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from pathlib import Path
import inspect
from importlib import import_module
import sys
import statistics
from hashlib import md5
from time import time, sleep
from operator import itemgetter
from func_timeout import func_timeout, FunctionTimedOut

import RPi.GPIO as GPIO
# pip install retry
from retry import retry
# For analog sensors
from gpiozero import MCP3008
# For I2C sensors
import smbus2
# Bluetooth sensors
from bluepy.btle import Scanner

from terrariumUtils import terrariumUtils, terrariumCache, classproperty

class terrariumSensorException(TypeError):
  '''There is a problem with loading a hardware sensor.'''
  pass

class terrariumSensorUnknownHardwareException(terrariumSensorException):
  pass

class terrariumSensorInvalidSensorTypeException(terrariumSensorException):
  pass

class terrariumSensorLoadingException(terrariumSensorException):
  pass

class terrariumSensorUpdateException(terrariumSensorException):
  pass

class terrariumSensor(object):
  HARDWARE = None
  TYPES = []
  NAME = None

  _CACHE_TIMEOUT = 30
  _UPDATE_TIME_OUT = 10

  @classproperty
  def available_hardware(__cls__):
    __CACHE_KEY = 'known_sensors'
    cache = terrariumCache()

    known_sensors = cache.get_data(__CACHE_KEY)
    if known_sensors is None:
      known_sensors = {}
      all_types = []
      # Start dynamically loading sensors (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
      for file in sorted(Path(__file__).parent.glob('*_sensor.py')):
        imported_module = import_module( '.' + file.stem, package='{}'.format(__name__))

        for i in dir(imported_module):
          attribute = getattr(imported_module, i)

          if inspect.isclass(attribute) and attribute != __cls__ and issubclass(attribute, __cls__):
            setattr(sys.modules[__name__], file.stem, attribute)
            if attribute.HARDWARE is not None:
              known_sensors[attribute.HARDWARE] = attribute
              all_types += attribute.TYPES

      # Update sensors that do not have a known type. Those are remote and scripts sensors
      all_types = list(set(all_types))
      for hardware in known_sensors:
        if len(known_sensors[hardware].TYPES) == 0:
          known_sensors[hardware].TYPES = all_types

      cache.set_data(__CACHE_KEY,known_sensors,-1)

    return known_sensors

  # Return a list with type and names of supported switches
  @classproperty
  def available_sensors(__cls__):
    data = []
    all_types = ['conductivity'] # For now 'conductivity' is only available through script or remote
    for (hardware_type, sensor) in __cls__.available_hardware.items():
      if sensor.NAME is not None:
        data.append({'hardware' : hardware_type, 'name' : sensor.NAME, 'types' : sensor.TYPES})
        all_types += sensor.TYPES

    # Remote and script sensors can handle all the known types
    all_types = list(set(all_types))
    for sensor in data:
      if len(sensor['types']) == 0:
        sensor['types'] = all_types

    return sorted(data, key=itemgetter('name'))

  @classproperty
  def sensor_types(__cls__):
    sensor_types = []

    for sensor in __cls__.available_sensors:
      sensor_types += sensor['types']

    return sorted(list(set(sensor_types)))

  # Return polymorph sensor....
  def __new__(cls, sensor_id, hardware_type, sensor_type, address, name = '', unit_value_callback = None, trigger_callback = None):
    known_sensors = terrariumSensor.available_hardware

    if hardware_type not in known_sensors:
      raise terrariumSensorUnknownHardwareException(f'Trying to load an unknown hardware device {hardware_type} at address {address} with name {name}')

    if sensor_type not in known_sensors[hardware_type].TYPES:
      raise terrariumSensorInvalidSensorTypeException(f'Hardware does not have a {sensor_type} sensor at address {address} with name {name}')

    return super(terrariumSensor, cls).__new__(known_sensors[hardware_type])

  def __init__(self, id, _, sensor_type, address, name = '', unit_value_callback = None, trigger_callback = None):
    self._device = {'id'             : None,
                    'name'           : None,
                    'address'        : None,
                    'type'           : sensor_type,  # Readonly property

                    'device'         : None,
                    'cache_key'      : None,
                    'power_mngt'     : None,
                    'erratic_errors' : 0,
                    'last_update'    : 0,
                    'value'          : None}

    self._sensor_cache = terrariumCache()
    self.__unit_value_callback = unit_value_callback
    self.__trigger_callback = trigger_callback

    # Set the properties
    self.id          = id
    self.name        = name
    self.address     = address

    # Load hardware can update the address value that is used for making a unique ID when not set
    self.load_hardware()
    # REMINDER: We do not take a measurement at this point. That is up to the developer to explicit request an update.

  def __power_management(self, on):
    # Some kind of 'power management' with the last gpio pin number :) https://raspberrypi.stackexchange.com/questions/68123/preventing-corrosion-on-yl-69
    if self._device['power_mngt'] is not None:
      logger.debug(f'Sensor {self} has power management enabled')
      if on:
        logger.debug('Enable power to the sensor {self} now.')
        GPIO.output(self._device['power_mngt'], GPIO.HIGH)
        sleep(1)
      else:
        logger.debug('Close power to the sensor {self} now.')
        GPIO.output(self._device['power_mngt'], GPIO.LOW)

  @property
  def __sensor_cache_key(self):
    if self._device['cache_key'] is None:
      self._device['cache_key'] = md5(f'{self.HARDWARE}{self.address}'.encode()).hexdigest()

    return self._device['cache_key']

  @property
  def id(self):
    if self._device['id'] is None:
      self._device['id'] = md5(f'{self.HARDWARE}{self.address}{self.type}'.encode()).hexdigest()

    return self._device['id']

  @id.setter
  def id(self, value):
    if value is not None:
      self._device['id'] = value.strip()

  @property
  def hardware(self):
    return self.HARDWARE

  @property
  def name(self):
    return self._device['name']

  @name.setter
  def name(self, value):
    if '' != value.strip():
      self._device['name'] = value.strip()

  @property
  def address(self):
    return self._device['address']

  @property
  def _address(self):
    address = [ part.strip() for part in self.address.split(',') if '' != part.strip()]
    return address

  @address.setter
  def address(self, value):
    value = terrariumUtils.clean_address(value)
    if value is not None and '' != value:
      self._device['address'] = value

  # Readonly property
  @property
  def device(self):
    return self._device['device']

  # Readonly property
  @property
  def sensor_type(self):
    return self._device['type']

  # Readonly property
  @property
  def type(self):
    return self._device['type']

  @property
  def value(self):
    return self._device['value']

  @property
  def last_update(self):
    return self._device['last_update']

  @property
  def erratic(self):
    return self._device['erratic_errors']

  @erratic.setter
  def erratic(self, value):
    self._device['erratic_errors'] = value

  def get_hardware_state(self):
    pass

  @retry(terrariumSensorLoadingException, tries=3, delay=0.5, max_delay=2, logger=logger)
  def load_hardware(self, reload = False):
    # Get hardware cache key based on the combination of hardware and address
    hardware_cache_key = md5(f'HW-{self.HARDWARE}-{self.address}'.encode()).hexdigest()
    # Load hardware device from cache
    hardware = self._sensor_cache.get_data(hardware_cache_key)
    if reload or hardware is None:
      # Could not find valid hardware cache. So create a new hardware device
      try:
        hardware = func_timeout(self._UPDATE_TIME_OUT, self._load_hardware)
        if hardware is not None:
          # Store the hardware in the cache for unlimited of time
          self._sensor_cache.set_data(hardware_cache_key,hardware,-1)
        else:
          # Raise error that hard is not loaded with an unknown message :(
          raise terrariumSensorLoadingException(f'Unable to load sensor {self}: Did not return a device.')

      except FunctionTimedOut:
      # What ever fails... does not matter, as the data is still None and will raise a terrariumSensorUpdateException and trigger the retry
        raise terrariumSensorLoadingException(f'Unable to load sensor {self}: timed out ({self._UPDATE_TIME_OUT} seconds) during loading.')

      except Exception as ex:
        raise terrariumSensorLoadingException(f'Unable to load sensor {self}: {ex}')

    self._device['device'] = hardware
    # Check for power management features and enable it if set
    if self._device['power_mngt'] is not None:
      GPIO.setup(self._device['power_mngt'], GPIO.OUT)

  # When we get Runtime errors retry up to 3 times
  @retry(terrariumSensorUpdateException, tries=3, delay=0.5, max_delay=2, logger=logger)
  def get_data(self):
    data = None
    self.__power_management(True)

    try:
      data = func_timeout(self._UPDATE_TIME_OUT, self._get_data)
    except FunctionTimedOut:
      # What ever fails... does not matter, as the data is still None and will raise a terrariumSensorUpdateException and trigger the retry
      logger.error(f'Sensor {self} timed out after {self._UPDATE_TIME_OUT} seconds during updating...')
    except Exception as ex:
      logger.error(f'Sensor {self} has exception: {ex}')

    self.__power_management(False)

    if data is None:
      raise terrariumSensorUpdateException(f'Invalid reading from sensor {self}')

    return data


  def update(self, force = False):
    if self._device['device'] is None:
      raise terrariumSensorLoadingException(f'Sensor {self} is not loaded! Can not update!')

    starttime = time()
    data = self._sensor_cache.get_data(self.__sensor_cache_key)

    if (data is None or force) and self._sensor_cache.set_running(self.__sensor_cache_key):
      logger.debug(f'Start getting new data from  sensor {self}')
      try:
        data = self.get_data()
        self._sensor_cache.set_data(self.__sensor_cache_key,data, self._CACHE_TIMEOUT)
      except Exception as ex:
        logger.error(f'Error updating sensor {self}. Check your hardware! {ex}')

      self._sensor_cache.clear_running(self.__sensor_cache_key)

    current = None if data is None or self.sensor_type not in data else data[self.sensor_type]

    if current is None:
      self._sensor_cache.clear_data(self.__sensor_cache_key)

    else:
      self._device['last_update'] = int(starttime)
      self._device['value'] = current
      return current

  def stop(self):
    if self._device['power_mngt'] is not None:
      GPIO.cleanup(self._device['power_mngt'])

  def __repr__(self):
    return f'{self.NAME} {self.type} named \'{self.name}\' at address \'{self.address}\''


  # Auto discovery of known and connected sensors
  @staticmethod
  def scan_sensors(unit_value_callback = None, trigger_callback = None, **kwargs):
    for (hardware_type,sensor_device) in terrariumSensor.available_hardware.items():
      try:
        for sensor in sensor_device._scan_sensors(unit_value_callback, trigger_callback, **kwargs):
          yield sensor
      except AttributeError as ex:
        # Scanning not supported, just ignore
        pass

class terrariumAnalogSensor(terrariumSensor):
  HARDWARE = None
  TYPES = []
  NAME = None

  __AMOUNT_OF_MEASUREMENTS = 5

  def _load_hardware(self):
    address = self._address
    # Load the analog converter here
    device = MCP3008(channel=int(address[0]), device=0 if len(address) == 1 or int(address[1]) < 0 else int(address[1]))
    return device

  def _get_data(self):
    # This will return the measured voltage of the analog device.
    values = []
    for counter in range(self.__AMOUNT_OF_MEASUREMENTS):
      value = self.device.value
      if terrariumUtils.is_float(value):
        values.append(float(value))
      sleep(0.2)

    # sort values from low to high
    values.sort()
    # Calculate average. Exclude the min and max value.
    return statistics.mean(values[1:-1])

class terrariumI2CSensor(terrariumSensor):

  @property
  def _address(self):
    address = super()._address
    if type(address[0]) is str:
      if not address[0].startswith('0x'):
        address[0] = '0x' + address[0]
      address[0] = int(address[0],16)

    return address

  def _open_hardware(self):
    address = self._address

    return smbus2.SMBus(1 if len(address) == 1 or int(address[1]) < 1 else int(address[1]))

  def _load_hardware(self):
    address = self._address
    device  = (address[0], smbus2.SMBus(1 if len(address) == 1 or int(address[1]) < 1 else int(address[1])))
    return device

  # def __exit__(self):
  #   print('I2C close with block')

class terrariumI2CSensorMixin():

  # control constants
  SOFTRESET = 0xFE
  SOFTRESET_TIMEOUT = 0.1

  TEMPERATURE_TRIGGER_NO_HOLD = 0xF3
  TEMPERATURE_WAIT_TIME = 0.1

  HUMIDITY_TRIGGER_NO_HOLD = 0xF5
  HUMIDITY_WAIT_TIME = 0.1

  def __soft_reset(self, i2c_bus):
    i2c_bus.write_byte(self.device[0], self.SOFTRESET)
    sleep(self.SOFTRESET_TIMEOUT)

  def __get_data(self,i2c_bus, trigger, timeout):
    data1 = data2 = None
    # Send request for data
    i2c_bus.write_byte(self.device[0], trigger)
    sleep(timeout)

    data1 = i2c_bus.read_byte(self.device[0])
    try:
      data2 = i2c_bus.read_byte(self.device[0])
    except Exception as ex:
      data2 = data1

    return (data1,data2)

  def _get_data(self):
    data = {}
    with self._open_hardware() as i2c_bus:
      # Datasheet recommend do Soft Reset before measurement:
      self.__soft_reset(i2c_bus)
      if 'temperature' in self.TYPES:
        bytedata = self.__get_data(i2c_bus, self.TEMPERATURE_TRIGGER_NO_HOLD,self.TEMPERATURE_WAIT_TIME)
        data['temperature'] = ((bytedata[0]*256.0+bytedata[1])*175.72/65536.0)-46.85
      if 'humidity' in self.TYPES:
        bytedata = self.__get_data(i2c_bus, self.HUMIDITY_TRIGGER_NO_HOLD,self.HUMIDITY_WAIT_TIME)
        data['humidity'] = ((bytedata[0]*256.0+bytedata[1])*125.0/65536.0)-6.0

    return data


"""
TCA9548A I2C switch driver, Texas instruments
8 bidirectional translating switches
I2C SMBus protocol
Manual: tca9548.pdf
Source: https://github.com/IRNAS/tca9548a-python/blob/master/tca9548a.py
Added option for different I2C bus
"""
# import smbus
# import logging

class TCA9548A(object):
    def __init__(self, address, bus = 1):
        """Init smbus channel and tca driver on specified address."""
        try:
            self.PORTS_COUNT = 8     # number of switches

            self.i2c_bus = smbus2.SMBus(bus)
            self.i2c_address = address
            if self.get_control_register() is None:
                raise ValueError
        except ValueError:
            logger.error("No device found on specified address!")
            self.i2c_bus = None
        except:
            logger.error("Bus on channel {} is not available.".format(bus))
            logger.info("Available busses are listed as /dev/i2c*")
            self.i2c_bus = None

    def get_control_register(self):
        """Read value (length: 1 byte) from control register."""
        try:
            value = self.i2c_bus.read_byte(self.i2c_address)
            return value
        except:
            return None

    def get_channel(self, ch_num):
        """Get channel state (specified with ch_num), return 0=disabled or 1=enabled."""
        if ch_num < 0 or ch_num > self.PORTS_COUNT - 1:
            return None
        register = self.get_control_register()
        if register is None:
            return None
        value = ((register >> ch_num) & 1)
        return value

    def set_control_register(self, value):
        """Write value (length: 1 byte) to control register."""
        try:
            if value < 0 or value > 255:
                return False
            self.i2c_bus.write_byte(self.i2c_address, value)
            return True
        except:
            return False

    def set_channel(self, ch_num, state):
        """Change state (0=disable, 1=enable) of a channel specified in ch_num."""
        if ch_num < 0 or ch_num > self.PORTS_COUNT - 1:
            return False
        if state != 0 and state != 1:
            return False
        current_value = self.get_control_register()
        if current_value is None:
            return False
        if state:
            new_value = current_value | 1 << ch_num
        else:
            new_value = current_value & (255 - (1 << ch_num))
        return_value = self.set_control_register(new_value)
        return return_value

    def __del__(self):
        """Driver destructor."""
        self.i2c_bus = None

class terrariumBluetoothSensor(terrariumSensor):

  __MIN_DB = -90
  __SCAN_TIME = 3

  @property
  def _address(self):
    address = super()._address
    if len(address) == 1:
      address.append(0)
    elif len(address) == 2:
      address[1] = int(address[1]) if terrariumUtils.is_float(address[1]) and terrariumUtils.is_float(address[1]) > 0 else 0

    return address

  @staticmethod
  def _scan_sensors(sensorclass, ids = [], unit_value_callback = None, trigger_callback = None):
    # Due to multiple bluetooth dongles, we are looping 10 times to see which devices can scan. Exit after first success
    ok = True
    for counter in range(10):
      try:
        devices = Scanner(counter).scan(terrariumBluetoothSensor.__SCAN_TIME)
        for device in devices:
          if device.rssi > terrariumBluetoothSensor.__MIN_DB and device.getValueText(9) is not None and device.getValueText(9).lower() in ids:
            for sensor_type in sensorclass.TYPES:
              logger.debug(sensor_type, sensorclass, device.addr)
              yield terrariumSensor(None,
                                    sensorclass.HARDWARE,
                                    sensor_type,
                                    device.addr + ('' if counter == 0 else f',{counter}'),
                                    f'{sensorclass.NAME} measuring {sensor_type}',
                                    unit_value_callback = unit_value_callback,
                                    trigger_callback    = trigger_callback)

        # we found devices, so this device is ok! Stop trying more bluetooth devices
        break

      except Exception as ex:
        ok = False

    if not ok:
      logger.warning('Bluetooth scanning is not enabled for normal users or there are zero Bluetooth LE devices available.... bluetooth is disabled!')

    return []
