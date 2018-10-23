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
    except Exception, ex:
      logger.exception('Error checking online state sensor at address: \'%s\'. Error: %s' % (self.__address,ex))

    return False

  def __get_raw_data(self,force_update = False):
    if self.__address is None:
      return

    starttime = int(time.time())

    if force_update or starttime - self.__cached_data['last_update'] > terrariumMiFloraSensor.__CACHE_TIMEOUT:
      try:
        miflora_dev = Peripheral(self.__address)
        #Read battery and firmware version attribute
        self.__cached_data['battery'], self.__cached_data['firmware'] = unpack('<xB5s',miflora_dev.readCharacteristic(terrariumMiFloraSensor.__MIFLORA_FIRMWARE_AND_BATTERY))

        #Enable real-time data reading
        miflora_dev.writeCharacteristic(terrariumMiFloraSensor.__MIFLORA_REALTIME_DATA_TRIGGER, str(bytearray([0xa0, 0x1f])), True)

        #Read plant data
        self.__cached_data['temperature'], self.__cached_data['light'], self.__cached_data['moisture'], self.__cached_data['fertility'] = unpack('<hxIBHxxxxxx',miflora_dev.readCharacteristic(terrariumMiFloraSensor.__MIFLORA_GET_DATA))

        # Close connection...
        miflora_dev.disconnect()

        self.__cached_data['last_update'] = starttime

      except Exception, ex:
        logger.exception('Error getting new data from sensor at address: \'%s\'. Error: %s' % (self.__address,ex))

  def get_temperature(self):
    value = None
    logger.debug('Read temperature value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    self.__get_raw_data()
    if terrariumUtils.is_float(self.__cached_data['temperature']):
      value = float(self.__cached_data['temperature']) / 10.0

    logger.debug('Got data from temperature sensor type \'%s\' with address %s: temperature: %s' % (self.__class__.__name__,self.__address,value))
    return value

  def get_moisture(self):
    value = None
    logger.debug('Read moisture value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    self.__get_raw_data()
    if terrariumUtils.is_float(self.__cached_data['moisture']):
      value = float(self.__cached_data['moisture'])

    logger.debug('Got data from moisture sensor type \'%s\' with address %s: moisture: %s' % (self.__class__.__name__,self.__address,value))
    return value

  def get_light(self):
    value = None
    logger.debug('Read brightness value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    self.__get_raw_data()
    if terrariumUtils.is_float(self.__cached_data['light']):
      value = float(self.__cached_data['light'])

    logger.debug('Got data from brightness sensor type \'%s\' with address %s: brightness: %s' % (self.__class__.__name__,self.__address,value))
    return value

  def get_fertility(self):
    value = None
    logger.debug('Read fertility value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    self.__get_raw_data()
    if terrariumUtils.is_float(self.__cached_data['fertility']):
      value = float(self.__cached_data['fertility'])

    logger.debug('Got data from fertility sensor type \'%s\' with address %s: fertility: %s' % (self.__class__.__name__,self.__address,value))
    return value

  def get_firmware(self):
    value = None
    logger.debug('Read firmware value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    self.__get_raw_data()
    if self.__cached_data['firmware'] is not None:
      value = self.__cached_data['firmware']

    logger.debug('Got data from firmware sensor type \'%s\' with address %s: fertility: %s' % (self.__class__.__name__,self.__address,value))
    return value

  def get_battery(self):
    value = None
    logger.debug('Read firmware value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    self.__get_raw_data()
    if terrariumUtils.is_float(self.__cached_data['battery']):
      value = float(self.__cached_data['battery'])

    logger.debug('Got data from firmware sensor type \'%s\' with address %s: fertility: %s' % (self.__class__.__name__,self.__address,value))
    return value

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
    except Exception, ex:
      logger.warning('Bluetooth scanning is not enabled for normal users or there are 0 Bluetooth LE device available.... bluetooth is disabled!')
