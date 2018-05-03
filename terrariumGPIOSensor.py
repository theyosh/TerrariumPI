# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import time
import RPi.GPIO as GPIO
import Adafruit_DHT

from terrariumUtils import terrariumUtils

class terrariumGPIOSensor(object):

  hardwaretype = None

  def __init__(self,datapin,powerpin = None):
    self.__datapin = datapin
    self.__powerpin = powerpin
    self.__value = None

    logger.debug('Initializing sensor type \'%s\' with GPIO address %s' % (self.__class__.__name__,self.__datapin))
    #GPIO.setup(terrariumUtils.to_BCM_port_number(self.__datapin), GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(terrariumUtils.to_BCM_port_number(self.__datapin), GPIO.IN)

    if self.__powerpin is not None:
      # Some kind of 'power management' :) https://raspberrypi.stackexchange.com/questions/68123/preventing-corrosion-on-yl-69
      logger.debug('Enabling power control management on sensor type \'%s\' with GPIO power address %s' % (self.__class__.__name__,self.__powerpin))
      GPIO.setup(terrariumUtils.to_BCM_port_number(self.__powerpin), GPIO.OUT)

    #GPIO.add_event_detect(terrariumUtils.to_BCM_port_number(self.__gpionummer), GPIO.BOTH, bouncetime=300)
    #GPIO.add_event_callback(terrariumUtils.to_BCM_port_number(self.__gpionummer), self.__state_change)

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def __get_raw_data(self):
    if self.__powerpin is not None:
      logger.debug('Powering up sensor type \'%s\' with GPIO address %s' % (self.__class__.__name__,self.__powerpin))
      GPIO.output(terrariumUtils.to_BCM_port_number(self.__powerpin),1)
      # Time to get power flowing. Not sure what the right amount time would be....
      time.sleep(0.5)

    self.__value = GPIO.input(terrariumUtils.to_BCM_port_number(self.__datapin))
    logger.debug('Read state sensor type \'%s\' with GPIO address %s with current alarm: %s' % (self.__class__.__name__,self.__datapin,self.__value))

    if self.__powerpin is not None:
      logger.debug('Powering down sensor type \'%s\' with GPIO address %s' % (self.__class__.__name__,self.__powerpin))
      GPIO.output(terrariumUtils.to_BCM_port_number(self.__powerpin),0)

  def get_current(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__value) else float(self.__value)

  def close(self):
    logger.debug('Close sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__datapin))
    GPIO.cleanup(terrariumUtils.to_BCM_port_number(self.__datapin))
    if self.__powerpin is not None:
      logger.debug('Close power control pin of sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__powerpin))
      GPIO.cleanup(terrariumUtils.to_BCM_port_number(self.__powerpin))

class terrariumYTXXSensorDigital(terrariumGPIOSensor):

  hardwaretype = 'ytxx-digital'

  def get_moisture(self):
    # Invert the value
    # Return 1 for dry
    # Return 0 for wet
    return self.get_current()

  def get_alarm(self):
    return self.get_moisture() == 1.0

  def get_state(self):
    return (_('Dry') if self.get_alarm() else _('Wet'))

class terrariumDHTSensor(terrariumGPIOSensor):

  hardwaretype = None

  def __init__(self,datapin,dhttype,powerpin = None):
    super(terrariumDHTSensor,self).__init__(datapin,powerpin)
    self.__datapin = datapin
    #self.__powerpin = powerpin
    #GPIO.cleanup(terrariumUtils.to_BCM_port_number(self.__datapin))
    self.__temperature = None
    self.__humidity = None

    if 'dht11' == dhttype:
      self.__dhttype = Adafruit_DHT.DHT11
    elif 'dht22' == dhttype:
      self.__dhttype = Adafruit_DHT.DHT22
    elif 'am2302' == dhttype:
      self.__dhttype = Adafruit_DHT.AM2302

  def __get_raw_data(self):
    # Need some extra timeout to get the chip to relax....:(
    time.sleep(2.1)
    self.__humidity, self.__temperature = Adafruit_DHT.read_retry(self.__dhttype, terrariumUtils.to_BCM_port_number(self.__datapin),5)

  def get_temperature(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__temperature) else float(self.__temperature)

  def get_humidity(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__humidity) else float(self.__humidity)

class terrariumDHT11Sensor(terrariumDHTSensor):

  hardwaretype = 'dht11'

  def __init__(self,datapin,powerpin = None):
    super(terrariumDHT11Sensor,self).__init__(datapin,terrariumDHT11Sensor.hardwaretype,powerpin)

class terrariumDHT22Sensor(terrariumDHTSensor):

  hardwaretype = 'dht22'

  def __init__(self,datapin,powerpin = None):
    super(terrariumDHT22Sensor,self).__init__(datapin,terrariumDHT22Sensor.hardwaretype,powerpin)

class terrariumAM2302Sensor(terrariumDHTSensor):

  hardwaretype = 'am2302'

  def __init__(self,datapin,powerpin = None):
    super(terrariumAM2302Sensor,self).__init__(datapin,terrariumAM2302Sensor.hardwaretype,powerpin)

class terrariumHCSR04Sensor(terrariumGPIOSensor):

  hardwaretype = 'hc-sr04'

  def __init__(self,triggerpin,echopin,powerpin = None):
    super(terrariumHCSR04Sensor,self).__init__(echopin,powerpin)
    GPIO.setup(terrariumUtils.to_BCM_port_number(triggerpin),GPIO.OUT)
    #ECHO pin is done at super()
    self.__datapin = echopin
    self.__triggerpin = triggerpin
    self.__value = None

  def __get_raw_data(self):
    GPIO.output(terrariumUtils.to_BCM_port_number(self.__triggerpin), False)
    time.sleep(2)
    GPIO.output(terrariumUtils.to_BCM_port_number(self.__triggerpin), True)
    time.sleep(0.00001)
    GPIO.output(terrariumUtils.to_BCM_port_number(self.__triggerpin), False)
    pulse_start = time.time()
    while GPIO.input(terrariumUtils.to_BCM_port_number(self.__datapin))==0:
      pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(terrariumUtils.to_BCM_port_number(self.__datapin))==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    # https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
    # Measure in centimetre
    self.__value = round(pulse_duration * 17150,5)

  def get_current(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__value) else float(self.__value)

  def close(self):
    super(terrariumHCSR04Sensor,self).close()
    logger.debug('Close sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__triggerpin))
    GPIO.cleanup(terrariumUtils.to_BCM_port_number(self.__triggerpin))

  def get_distance(self):
    return self.get_current()
