# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from struct import unpack
from bluepy.btle import Scanner, Peripheral

from terrariumUtils import terrariumUtils

#from gevent import monkey, sleep
#monkey.patch_all()

class terrariumMiFloraSensor(object):
  hardwaretype = 'miflora'

  def __init__(self,address):
    self.__address = address
    self.__firmware = None
    self.__battery = None

    logger.debug('Initializing sensor type \'%s\' at address %s' % (self.__class__.__name__,self.__address))

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def close(self):
    """Closes the i2c connection"""
    logger.debug('Close sensor type \'%s\' at address %s' % (self.__class__.__name__,self.__address))
    #self.__bus.close()

  def __get_raw_data(self,part):
    value = None

    try:
      miflora_dev = Peripheral(self.__address)
      #Read battery and firmware version attribute
      self.__battery, self.__firmware = unpack('<xB5s',miflora_dev.readCharacteristic(56))

      #Enable real-time data reading
      miflora_dev.writeCharacteristic(51, str(bytearray([0xa0, 0x1f])), True)

      #Read plant data
      temperature, sunlight, moisture, fertility = unpack('<hxIBHxxxxxx',miflora_dev.readCharacteristic(53))

      # Close connection...
      miflora_dev.disconnect()

      if 'temperature' == part:
        value = float(temperature)/10.0
      if 'moisture' == part:
        value = float(moisture)
      if 'light' == part:
        value = float(sunlight)
      if 'fertility' == part:
        value = float(fertility)
    except Exception, ex:
      print ex

    return value

  def get_temperature(self):
    logger.debug('Read temperature value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    temperature = self.__get_raw_data('temperature')
    logger.debug('Got data from temperature sensor type \'%s\' with address %s: temperature: %s' % (self.__class__.__name__,self.__address,temperature))
    return None if not terrariumUtils.is_float(temperature) else float(temperature)

  def get_moisture(self):
    logger.debug('Read moisture value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    moisture = self.__get_raw_data('moisture')
    logger.debug('Got data from moisture sensor type \'%s\' with address %s: moisture: %s' % (self.__class__.__name__,self.__address,moisture))
    return None if not terrariumUtils.is_float(moisture) else float(moisture)

  def get_light(self):
    logger.debug('Read brightness value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    light = self.__get_raw_data('light')
    logger.debug('Got data from brightness sensor type \'%s\' with address %s: brightness: %s' % (self.__class__.__name__,self.__address,light))
    return None if not terrariumUtils.is_float(light) else float(light)

  def get_fertility(self):
    logger.debug('Read fertility value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__address))
    fertility = self.__get_raw_data('fertility')
    logger.debug('Got data from fertility sensor type \'%s\' with address %s: fertility: %s' % (self.__class__.__name__,self.__address,fertility))
    return None if not terrariumUtils.is_float(fertility) else float(fertility)

  def get_firmware(self):
    if self.__firmware is None:
      self.__get_raw_data('temperature')
    return self.__firmware

  def get_battery(self):
    if self.__battery is None:
      self.__get_raw_data('temperature')
    return self.__battery

  @staticmethod
  def scan():
    SCANTIME = 5
    logger.info('Scanning %s seconds for MiFlora bluetooth devices' % SCANTIME)

    for device in Scanner().scan(SCANTIME):
      if device.getValueText(9).lower() in ['flower mate','flower care']:
        address = device.addr
        device = None
        logger.info('Found MiFlora bluetooth device at address %s' % address)
        yield (address,'temperature')
        yield (address,'moisture')
        yield (address,'fertility')
