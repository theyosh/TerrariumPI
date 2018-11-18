# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from struct import unpack
from bluepy.btle import Scanner, Peripheral
import time

from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumMiFloraSensor(object):
  __CACHE_TIMEOUT = 29
  __MIFLORA_FIRMWARE_AND_BATTERY = 56
  __MIFLORA_REALTIME_DATA_TRIGGER = 51
  __MIFLORA_GET_DATA = 53

  hardwaretype = 'miflora'

  def __init__(self,address):
    starttime = int(time.time())

    self.__cached_data = {'firmware'    : None,
                          'battery'     : None,
                          'temperature' : None,
                          'light'       : None,
                          'moisture'    : None,
                          'fertility'   : None,
                          'last_update' : 0}

    self.__address = address
    self.__errors = 0
    if not self.__check_connection():
      self.__address = None
      logger.error('Initializing failed for sensor type \'%s\' at address %s after %s seconds' % (self.__class__.__name__,self.__address,int(time.time())-starttime))

    logger.debug('Initialized sensor type \'%s\' at address %s in %s seconds' % (self.__class__.__name__,self.__address,int(time.time())-starttime))

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def __check_connection(self):
    if self.__address is None:
      return False

    try:
      miflora_dev = Peripheral(self.__address)
      #Read battery and firmware version attribute
      self.__cached_data['battery'], self.__cached_data['firmware'] = unpack('<xB5s',miflora_dev.readCharacteristic(terrariumMiFloraSensor.__MIFLORA_FIRMWARE_AND_BATTERY))
      miflora_dev.disconnect()
      return True
    except Exception as ex:
      logger.error('Error checking online state sensor at address: \'%s\'. Error: %s' % (self.__address,ex))

    return False

  def __get_raw_data(self,force_update = False):
    if self.__address is None:
      return

    starttime = int(time.time())

    if force_update or starttime - self.__cached_data['last_update'] > terrariumMiFloraSensor.__CACHE_TIMEOUT:
      try:
        cached_data = {}
        for item in self.__cached_data:
          cached_data[item] = None

        miflora_dev = Peripheral(self.__address)
        #Read battery and firmware version attribute
        cached_data['battery'], cached_data['firmware'] = unpack('<xB5s',miflora_dev.readCharacteristic(terrariumMiFloraSensor.__MIFLORA_FIRMWARE_AND_BATTERY))

        #Enable real-time data reading
        miflora_dev.writeCharacteristic(terrariumMiFloraSensor.__MIFLORA_REALTIME_DATA_TRIGGER, bytearray([0xa0, 0x1f]), True)

        #Read plant data
        cached_data['temperature'], cached_data['light'], cached_data['moisture'], cached_data['fertility'] = unpack('<hxIBHxxxxxx',miflora_dev.readCharacteristic(terrariumMiFloraSensor.__MIFLORA_GET_DATA))

        # Close connection...
        miflora_dev.disconnect()

        cached_data['last_update'] = starttime
        for item in self.__cached_data:
          self.__cached_data[item] = cached_data[item]

        self.__errors = 0

      except Exception as ex:
        self.__errors += 1
        if self.__errors > 3:
          logger.error('Error getting new data from sensor at address: \'%s\'. Error: %s' % (self.__address,ex))
        else:
          logger.warning('Error getting new data from sensor at address: \'%s\'. Error: %s' % (self.__address,ex))

  def __get_data(self,sensortype):
    value = None
    logger.debug('Read %s value from sensor type \'%s\' with address %s' % (sensortype,self.__class__.__name__,self.__address))
    self.__get_raw_data()
    if 'firmware' == sensortype:
      value = self.__cached_data[sensortype].decode()
    elif terrariumUtils.is_float(self.__cached_data[sensortype]):
      value = float(self.__cached_data[sensortype])
      if 'temperature' == sensortype:
        value /= 10.0

    logger.debug('Got data from %s sensor type \'%s\' with address %s: temperature: %s' % (sensortype,self.__class__.__name__,self.__address,value))
    return value

  def get_temperature(self):
    return self.__get_data('temperature')

  def get_moisture(self):
    return self.__get_data('moisture')

  def get_light(self):
    return self.__get_data('light')

  def get_fertility(self):
    return self.__get_data('fertility')

  def get_firmware(self):
    return self.__get_data('firmware')

  def get_battery(self):
    return self.__get_data('battery')

  def close(self):
    """Closes the connection"""
    logger.debug('Close sensor type \'%s\' at address %s' % (self.__class__.__name__,self.__address))

  @staticmethod
  def scan():
    SCANTIME = 5
    MIN_DB = -90
    logger.info('Scanning %s seconds for MiFlora bluetooth devices' % SCANTIME)

    try:
      for device in Scanner().scan(SCANTIME):
        if device.rssi > MIN_DB and device.getValueText(9).lower() in ['flower mate','flower care']:
          address = device.addr
          device = None
          logger.info('Found MiFlora bluetooth device at address %s' % address)
          yield (address,'temperature')
          yield (address,'moisture')
          yield (address,'light')
          yield (address,'fertility')
    except Exception as ex:
      logger.warning('Bluetooth scanning is not enabled for normal users or there are 0 Bluetooth LE device available.... bluetooth is disabled!')
