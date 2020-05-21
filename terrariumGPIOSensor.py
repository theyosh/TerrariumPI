# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import RPi.GPIO as GPIO
import Adafruit_DHT

from gevent import sleep
from time import time

from terrariumSensor import terrariumSensorSource
from terrariumUtils import terrariumUtils

class terrariumGPIOSensor(terrariumSensorSource):
  TYPE = None
  VALID_SENSOR_TYPES = []

  def __init__(self, sensor_id, sensor_type, address, name = '', callback_indicator = None):
    super(terrariumGPIOSensor,self).__init__(sensor_id, sensor_type, address, name, callback_indicator)
    gpio_pins = self.get_address().split(',')
    logger.debug('Initializing sensor type \'%s\' with GPIO address %s'.format(self.get_type(),gpio_pins))
    GPIO.setup(terrariumUtils.to_BCM_port_number(gpio_pins[0]), GPIO.IN,pull_up_down=GPIO.PUD_UP)

  def load_data(self):
    data = None
    if self.open():
      data = self.load_raw_data()
      self.close()

    return data

  def load_raw_data(self):
    try:
      gpio_pins = self.get_address().split(',')
      data = GPIO.input(terrariumUtils.to_BCM_port_number(gpio_pins[0]))
      logger.debug('Read state sensor type \'{}\' with GPIO address {} with current alarm: {}'.format(self.get_type(),gpio_pins[0],data))

    except Exception as ex:
      logger.warning('Error reading new data from {} sensor \'{}\'. Error message: {}'.format(self.get_type(),self.get_name(),ex))
      return False

    return data

  def open(self):
    try:
      gpio_pins = self.get_address().split(',')
      logger.debug('Open sensor type \'{}\' with address {}'.format(self.get_type(),gpio_pins))

      if len(gpio_pins) > 1 and terrariumUtils.to_BCM_port_number(gpio_pins[-1]):
        # Some kind of 'power management' with the last gpio pin number :) https://raspberrypi.stackexchange.com/questions/68123/preventing-corrosion-on-yl-69
        logger.debug('Enabling power control management on sensor type \'{}\' with GPIO power pin {}'.format(self.get_type(),gpio_pins[-1]))
        GPIO.setup(terrariumUtils.to_BCM_port_number(gpio_pins[-1]), GPIO.OUT)
        sleep(0.5)

      GPIO.setup(terrariumUtils.to_BCM_port_number(gpio_pins[0]), GPIO.IN)

    except Exception as ex:
      logger.warning('Error opening {} sensor \'{}\'. Error message: {}'.format(self.get_type(),self.get_name(),ex))
      return False

    return True

  def close(self):
    try:
      gpio_pins = self.get_address().split(',')
      logger.debug('Closing sensor type \'{}\' with address {}'.format(self.get_type(),gpio_pins))
      GPIO.cleanup(terrariumUtils.to_BCM_port_number(gpio_pins[0]))

      if len(gpio_pins) > 1 and terrariumUtils.to_BCM_port_number(gpio_pins[-1]):
        logger.debug('Closeing power control pin of sensor type \'{}\' at GPIO power pin {}'.format(self.get_type(),gpio_pins[-1]))
        GPIO.cleanup(terrariumUtils.to_BCM_port_number(gpio_pins[-1]))

    except Exception as ex:
      logger.warning('Error closing {} sensor \'{}\'. Error message: {}'.format(self.get_type(),self.get_name(),ex))

class terrariumYTXXSensorDigital(terrariumGPIOSensor):
  TYPE = 'ytxx-digital'
  VALID_SENSOR_TYPES = ['moisture']

  def load_raw_data(self):
    data = super(terrariumYTXXSensorDigital,self).load_raw_data()
    return { self.get_sensor_type() : 0.0 if data == 1.0 else 100.0}

class terrariumDHTSensor(terrariumGPIOSensor):
  TYPE = None
  VALID_SENSOR_TYPES = ['temperature','humidity']

  def load_raw_data(self):
    data = None
    try:
      gpio_pins = self.get_address().split(',')
      data = {}

      sensor_device = Adafruit_DHT.DHT11
      if terrariumDHT22Sensor.TYPE == self.get_type():
        sensor_device = Adafruit_DHT.DHT22
      elif terrariumAM2302Sensor.TYPE == self.get_type():
        sensor_device = Adafruit_DHT.AM2302

      data['humidity'], data['temperature'] = Adafruit_DHT.read_retry(sensor_device, terrariumUtils.to_BCM_port_number(gpio_pins[0]),4)

    except Exception as ex:
      logger.warning('Error getting new data from {} sensor \'{}\'. Error message: {}'.format(self.get_type(),self.get_name(),ex))

    return data

class terrariumDHT11Sensor(terrariumDHTSensor):
  TYPE = 'dht11'

  hardwaretype = 'dht11'

class terrariumDHT22Sensor(terrariumDHTSensor):
  TYPE = 'dht22'

  hardwaretype = 'dht22'

class terrariumAM2302Sensor(terrariumDHTSensor):
  TYPE = 'am2302'

  hardwaretype = 'am2302'

class terrariumHCSR04Sensor(terrariumGPIOSensor):
  TYPE = 'hc-sr04'
  VALID_SENSOR_TYPES = ['distance']

  def __init__(self, sensor_id, sensor_type, address, name = '', callback_indicator = None):
    self.set_limit_max(1000)
    super(terrariumHCSR04Sensor,self).__init__(sensor_id, sensor_type, address, name, callback_indicator)

  def open(self):
    try:
      gpio_pins = self.get_address().split(',')
      logger.debug('Open sensor type \'{}\' with address {}'.format(self.get_type(),gpio_pins))

      if len(gpio_pins) > 2 and terrariumUtils.to_BCM_port_number(gpio_pins[-1]):
        # Some kind of 'power management' with the last gpio pin number :) https://raspberrypi.stackexchange.com/questions/68123/preventing-corrosion-on-yl-69
        logger.debug('Enabling power control management on sensor type \'{}\' with GPIO power pin {}'.format(self.get_type(),gpio_pins[-1]))
        GPIO.setup(terrariumUtils.to_BCM_port_number(gpio_pins[-1]), GPIO.OUT)
        sleep(0.5)

      GPIO.setup(terrariumUtils.to_BCM_port_number(gpio_pins[0]), GPIO.OUT) # Trigger out
      GPIO.setup(terrariumUtils.to_BCM_port_number(gpio_pins[1]), GPIO.IN)  # Data in

    except Exception as ex:
      logger.warning('Error opening {} sensor \'{}\'. Error message: {}'.format(self.get_type(),self.get_name(),ex))
      return False

    return True

  def load_raw_data(self):
    data = None
    try:
      gpio_pins = self.get_address().split(',')
      data = {}

      GPIO.output(terrariumUtils.to_BCM_port_number(gpio_pins[0]), False)
      sleep(2)
      GPIO.output(terrariumUtils.to_BCM_port_number(gpio_pins[0]), True)
      sleep(0.00001)
      GPIO.output(terrariumUtils.to_BCM_port_number(gpio_pins[0]), False)
      pulse_start = time()
      starttime = pulse_start
      while GPIO.input(terrariumUtils.to_BCM_port_number(gpio_pins[1])) == 0:
        pulse_start = time()
        # Somehow, sometimes this will end in an endless loop. The value will never go to '0' (zero). So wrong measurement and return none...
        if pulse_start - starttime > 2:
          logger.warn('Sensor {} \'{}\' is failing to get in the right state. Abort!'.format(self.get_type(),self.get_name()))
          return data

      pulse_end = time()
      while GPIO.input(terrariumUtils.to_BCM_port_number(gpio_pins[1])) == 1:
        pulse_end = time()

      pulse_duration = pulse_end - pulse_start
      # https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
      # Measure in centimetre
      data = { self.get_sensor_type() : round(pulse_duration * 17150,5)}

    except Exception as ex:
      pass

    return data

  def close(self):
    super(terrariumHCSR04Sensor,self).close()

    try:
      gpio_pins = self.get_address().split(',')

      if len(gpio_pins) > 2 and terrariumUtils.to_BCM_port_number(gpio_pins[1]):
        logger.debug('Closeing trigger control pin of sensor type \'{}\' at GPIO power pin {}'.format(self.get_type(),gpio_pins[1]))
        GPIO.cleanup(terrariumUtils.to_BCM_port_number(gpio_pins[1]))

    except Exception as ex:
      logger.warning('Error closing {} sensor \'{}\'. Error message: {}'.format(self.get_type(),self.get_name(),ex))
