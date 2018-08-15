# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from gpiozero import MCP3008

from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumAnalogSensor(object):

  hardwaretype = None

  def __init__(self, datapin, device = 0):
    self.__datapin = datapin
    self.__device = 0 if device is None else device
    self.__value = None

    logger.debug('Initializing sensor type \'%s\' with Analog address %s,%s' % (self.__class__.__name__,self.__datapin,self.__device))

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def __get_raw_data(self):
    # Read 5 samples of data and get an average of it
    sensor = MCP3008(channel=int(self.__datapin), device=int(self.__device))
    values = []
    for counter in range(5):
      value = sensor.value
      if terrariumUtils.is_float(value):
        values.append(float(value))
      sleep(0.2)

    sensor = None

    # sort values from low to high
    values.sort()
    # Calculate average. Exclude the min and max value. And therefore devide by 3
    self.__value = round((sum(values[1:-1]) / (len(values)-2)),5)

  def get_current(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__value) else float(self.__value)

  def close(self):
    logger.debug('Closed sensor type \'%s\' with address %s,%s' % (self.__class__.__name__,self.__datapin,self.__device))

class terrariumSKUSEN0161Sensor(terrariumAnalogSensor):

  hardwaretype = 'sku-sen0161'

  def get_ph(self):
    value = self.get_current()
    # https://github.com/theyosh/TerrariumPI/issues/108
    # We measure the values in volts already, so no deviding by 1000 as original script does
    return None if not terrariumUtils.is_float(value) else ((float(value) * ( 5000.0 / 1024.0)) * 3.3 + 0.1614)
