# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import time
import RPi.GPIO as GPIO
import Adafruit_DHT

from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumGPIOSensor(object):

  hardwaretype = None

  def __init__(self,datapin,powerpin = None):
    self.__datapin = datapin
    self.__powerpin = powerpin
    self.__value = None

    logger.debug('Initializing sensor type \'%s\' with GPIO address %s' % (self.__class__.__name__,self.__datapin))
    #GPIO.setup(terrariumUtils.to_BCM_port_number(self.__datapin), GPIO.IN,pull_up_down=GPIO.PUD_UP)


    #GPIO.add_event_detect(terrariumUtils.to_BCM_port_number(self.__gpionummer), GPIO.BOTH, bouncetime=300)
    #GPIO.add_event_callback(terrariumUtils.to_BCM_port_number(self.__gpionummer), self.__state_change)

  def __enter__(self):
    """used to enable python's with statement support"""
    GPIO.setup(terrariumUtils.to_BCM_port_number(self.__datapin), GPIO.IN)

    if self.__powerpin is not None:
      # Some kind of 'power management' :) https://raspberrypi.stackexchange.com/questions/68123/preventing-corrosion-on-yl-69
      logger.debug('Enabling power control management on sensor type \'%s\' with GPIO power address %s' % (self.__class__.__name__,self.__powerpin))
      GPIO.setup(terrariumUtils.to_BCM_port_number(self.__powerpin), GPIO.OUT)

    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def __get_raw_data(self):
    if self.__powerpin is not None:
      logger.debug('Powering up sensor type \'%s\' with GPIO address %s' % (self.__class__.__name__,self.__powerpin))
      GPIO.output(terrariumUtils.to_BCM_port_number(self.__powerpin),1)
      # Time to get power flowing. Not sure what the right amount time would be....
      sleep(0.5)

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
    # Convert the value
    # Return 0 for dry (value get_current = 1)
    # Return 100 for wet (value get_current = 0)
    return 0.0 if self.get_current() == 1.0 else 100.0

  def get_alarm(self):
    return self.get_moisture() == 0.0

  def get_state(self):
    return (_('Dry') if self.get_alarm() else _('Wet'))

class terrariumDHTSensor(terrariumGPIOSensor):
  __CACHE_TIMEOUT = 29

  hardwaretype = None

  def __init__(self,datapin,dhttype,powerpin = None):
    self.__cached_data = {'temperature' : None,
                          'humidity'    : None,
                          'last_update' : 0}

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

  def __get_raw_data(self,force_update = False):
    # Need some extra timeout to get the chip to relax....:(
    starttime = int(time.time())
    if force_update or starttime - self.__cached_data['last_update'] > terrariumDHTSensor.__CACHE_TIMEOUT:
      self.__cached_data['humidity'], self.__cached_data['temperature'] = Adafruit_DHT.read_retry(self.__dhttype, terrariumUtils.to_BCM_port_number(self.__datapin),5)
      self.__cached_data['last_update'] = starttime

  def get_temperature(self):
    value = None
    logger.debug('Read temperature value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__datapin))
    self.__get_raw_data()
    if terrariumUtils.is_float(self.__cached_data['temperature']):
      value = float(self.__cached_data['temperature'])

    logger.debug('Got data from temperature sensor type \'%s\' with address %s: temperature: %s' % (self.__class__.__name__,self.__datapin,value))
    return value

  def get_humidity(self):
    value = None
    logger.debug('Read humidity value from sensor type \'%s\' with address %s' % (self.__class__.__name__,self.__datapin))
    self.__get_raw_data()
    if terrariumUtils.is_float(self.__cached_data['humidity']):
      value = float(self.__cached_data['humidity'])

    logger.debug('Got data from humidity sensor type \'%s\' with address %s: moisture: %s' % (self.__class__.__name__,self.__datapin,value))
    return value

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

    self.__datapin = echopin
    self.__triggerpin = triggerpin
    self.__value = None

  def __get_raw_data(self):
    #ECHO pin is done at super()
    GPIO.setup(terrariumUtils.to_BCM_port_number(self.__triggerpin),GPIO.OUT)

    GPIO.output(terrariumUtils.to_BCM_port_number(self.__triggerpin), False)
    sleep(2)
    GPIO.output(terrariumUtils.to_BCM_port_number(self.__triggerpin), True)
    sleep(0.00001)
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
