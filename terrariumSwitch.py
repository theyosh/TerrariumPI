# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from pylibftdi import Driver, BitBangDevice, SerialDevice, Device
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import pigpio
from hashlib import md5
import thread
import time
import math

class terrariumSwitch():

  valid_hardware_types = ['ftdi','gpio','gpio-inverse','pwm-dimmer']

  OFF = False
  ON = True

  # PWM Dimmer settings
  PWM_DIMMER_MAXDIM = 880 # http://www.esp8266-projects.com/2017/04/raspberry-pi-domoticz-ac-dimmer-part-1/
  PWM_DIMMER_MIN_TIMEOUT=0.3
  PWM_DIMMER_MIN_STEP=1.0

  bitbang_addresses = {
    "1":"2",
    "2":"8",
    "3":"20",
    "4":"80",
    "5":"1",
    "6":"4",
    "7":"10",
    "8":"40",
    "all":"FF"
  }

  def __init__(self, id, hardware_type, address, name = '', power_wattage = 0.0, water_flow = 0.0, dimmer_on_duration = 0.0, dimmer_on_percentage = 100.0, dimmer_off_duration = 0.0, dimmer_off_percentage = 0.0, callback = None):
    self.id = id
    self.callback = callback

    self.set_hardware_type(hardware_type)

    if self.get_hardware_type() == 'ftdi':
      self.__load_ftdi_device()
    elif self.get_hardware_type() == 'pwm-dimmer':
      self.__load_pwm_device()
    elif 'gpio' in self.get_hardware_type():
      self.__load_gpio_device()

    self.set_address(address)
    self.set_name(name)
    self.set_power_wattage(power_wattage)
    self.set_water_flow(water_flow)

    self.set_dimmer_on_duration(dimmer_on_duration)
    self.set_dimmer_on_percentage(dimmer_on_percentage)
    self.set_dimmer_off_duration(dimmer_off_duration)
    self.set_dimmer_off_percentage(dimmer_off_percentage)

    if self.id is None:
      self.id = md5(b'' + self.get_hardware_type() + self.get_address()).hexdigest()

    logger.info('Loaded switch \'%s\' with values: power %.2fW and waterflow %.3fL/s' %
                (self.get_name(),
                 self.get_power_wattage(),
                 self.get_water_flow()))

    # Force to off state!
    self.state = None
    self.set_state(terrariumSwitch.OFF,True)

  def __load_ftdi_device(self):
    for device in Driver().list_devices():
      vendor, product, self.device = map(lambda x: x.decode('latin1'), device)
      self.device_type = 'Serial' if product.endswith('UART') else 'BitBang'
      logger.info('Found switch board %s, %s, %s, of type %s' % (vendor,product,self.device,self.device_type))
      break # For now, we only support 1 switch board!

  def __load_gpio_device(self):
    GPIO.setmode(GPIO.BOARD)

  def __load_pwm_device(self):
    self.__dimmer_running = False
    # localhost will not work always due to IPv6. Explicit 127.0.0.1 host
    self.__pigpio = pigpio.pi('127.0.0.1',8888)
    if not self.__pigpio.connected:
      logger.error('PiGPIOd process is not running')
      self.__pigpio = False

  def __dim_switch(self,from_value,to_value):
    # When the dimmer is working, ignore new state changes.
    if not self.__dimmer_running:
      self.__dimmer_running = True

      if from_value is None:
        logger.info('Switching dimmer \'%s\' from %s%% to %s%% instantly',
                  self.get_name(),from_value,to_value)
        # Geen animatie, gelijk to_value
        dim_value = terrariumSwitch.PWM_DIMMER_MAXDIM * ((100.0 - float(to_value)) / 100.0)
        self.__pigpio.hardware_PWM(int(self.get_address()), 5000, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle
      else:
        from_value = float(from_value)
        to_value = float(to_value)
        direction = (1.0 if from_value < to_value else -1.0)
        duration = (self.get_dimmer_on_duration() if direction == 1.0 else self.get_dimmer_off_duration())

        logger.info('Changing dimmer \'%s\' from %s%% to %s%% in %s seconds',self.get_name(),from_value,to_value,duration)

        distance = abs(from_value - to_value)
        if duration == 0.0 or distance == 0.0:
          steps = 1.0
        else:
          steps = math.floor(min( (abs(duration) / terrariumSwitch.PWM_DIMMER_MIN_TIMEOUT),
                                  (distance / terrariumSwitch.PWM_DIMMER_MIN_STEP)))
          distance /= steps
          duration /= steps

        logger.debug('Dimmer settings: Steps: %s, Distance per step: %s%%, Time per step: %s, Direction: %s',steps, distance, duration, direction)

        for counter in range(int(steps)):
          from_value += (direction * distance)
          dim_value = terrariumSwitch.PWM_DIMMER_MAXDIM * ((100.0 - from_value) / 100.0)
          logger.debug('Dimmer animation: Step: %s, value %s%%, Dim value: %s, timeout %s',counter+1, from_value, dim_value, duration)
          self.__pigpio.hardware_PWM(int(self.get_address()), 5000, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle
          time.sleep(duration)

        # For impatient people... Put the dimmer at the current state value if it has changed during the animation
        dim_value = terrariumSwitch.PWM_DIMMER_MAXDIM * ((100.0 - self.get_state()) / 100.0)
        self.__pigpio.hardware_PWM(int(self.get_address()), 5000, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle

      self.__dimmer_running = False
      logger.info('Dimmer \'%s\' is done at value %s%%',self.get_name(),self.get_state())
    else:
      logger.warning('Dimmer %s is already working. Ignoring state change!. Will switch to latest state value when done', self.get_name())

  def set_state(self, state, force = False):
    if self.get_state() is not state or force:
      if self.get_hardware_type() == 'ftdi':
        try:
          if 'BitBang' == self.device_type:
            with BitBangDevice(self.device) as device:
              device.baudrate = 9600
              if state is terrariumSwitch.ON:
                device.port |= int(terrariumSwitch.bitbang_addresses[str(self.get_address())], 16)
              else:
                device.port &= ~int(terrariumSwitch.bitbang_addresses[str(self.get_address())], 16)
              device.close()

          elif 'Serial' == self.device_type:
            with SerialDevice(self.device) as device:
              device.baudrate = 9600
              cmd = chr(0xff) + chr(0x0 + int(self.get_address())) + chr(0x0 + (1 if state is terrariumSwitch.ON else 0))
              device.write(cmd)
              device.close()

        except Exception, err:
          # Ignore for now
          print err
          pass

      elif self.get_hardware_type() == 'gpio':
        GPIO.output(int(self.get_address()), ( GPIO.HIGH if state is terrariumSwitch.ON else GPIO.LOW ))

      elif self.get_hardware_type() == 'gpio-inverse':
        GPIO.output(int(self.get_address()), ( GPIO.LOW if state is terrariumSwitch.ON else GPIO.HIGH ))

      elif self.get_hardware_type() == 'pwm-dimmer' and self.__pigpio is not False:
        # State 100 = full on which means 0 dim.
        # State is inverse of dim
        if state is terrariumSwitch.ON:
          state = self.get_dimmer_on_percentage()
        elif state is terrariumSwitch.OFF or not (0 <= state <= 100):
          state = self.get_dimmer_off_percentage()

        thread.start_new_thread(self.__dim_switch, (self.state,state))

      self.state = state
      if self.get_hardware_type() != 'pwm-dimmer':
        logger.info('Toggle switch \'%s\' from %s',self.get_name(),('off to on' if self.is_on() else 'on to off'))
      if self.callback is not None:
        data = self.get_data()
        self.callback(data)

    return self.get_state() == state

  def get_state(self):
    return self.state

  def get_data(self):
    data = {'id' : self.get_id(),
            'hardwaretype' : self.get_hardware_type(),
            'address' : self.get_address(),
            'name' : self.get_name(),
            'power_wattage' : self.get_power_wattage(),
            'current_power_wattage' : self.get_current_power_wattage(),
            'water_flow' : self.get_water_flow(),
            'current_water_flow' : self.get_current_water_flow(),
            'state' : self.get_state(),
            'dimmer_on_duration': self.get_dimmer_on_duration(),
            'dimmer_on_percentage' : self.get_dimmer_on_percentage(),
            'dimmer_off_duration': self.get_dimmer_off_duration(),
            'dimmer_off_percentage': self.get_dimmer_off_percentage()
            }

    return data

  def get_id(self):
    return self.id

  def get_hardware_type(self):
    return self.hardwaretype

  def set_hardware_type(self,type):
    if type in terrariumSwitch.valid_hardware_types:
      self.hardwaretype = type

  def get_address(self):
    return self.sensor_address

  def set_address(self,address):
    self.sensor_address = address
    if 'gpio' in self.get_hardware_type():
      try:
        GPIO.setup(int(self.get_address()), GPIO.OUT)
      except Exception, err:
        logger.warning(err)
        pass

  def get_name(self):
    return self.name

  def set_name(self,name):
    self.name = name

  def get_power_wattage(self):
    return self.power_wattage

  def get_current_power_wattage(self):
    wattage = 0.0
    if self.get_hardware_type() == 'pwm-dimmer':
      wattage = self.get_power_wattage() * (self.get_state() / 100.0)
    else:
      wattage = self.get_power_wattage()

    return wattage

  def set_power_wattage(self,value):
    try:
      self.power_wattage = float(value)
    except Exception:
      self.power_wattage = 0

  def get_water_flow(self):
    return self.water_flow

  def get_current_water_flow(self):
    waterflow = 0.0
    if self.get_hardware_type() == 'pwm-dimmer':
      waterflow = self.get_water_flow() * (self.get_state() / 100.0)
    else:
      waterflow = self.get_water_flow()

    return waterflow

  def set_water_flow(self,value):
    try:
      self.water_flow = float(value)
    except Exception:
      self.water_flow = 0

  def toggle(self):
    if self.get_state() is not None:
      if self.is_on():
        self.off()
      else:
        self.on()
      return True

    return None

  def is_on(self):
    if self.get_hardware_type() == 'pwm-dimmer':
      return self.get_state() > self.get_dimmer_off_percentage()
    else:
      return self.get_state() is terrariumSwitch.ON

  def is_off(self):
    if self.get_hardware_type() == 'pwm-dimmer':
      return self.get_state() == self.get_dimmer_off_percentage()
    else:
      return self.get_state() is terrariumSwitch.OFF

  def on(self):
    if self.get_state() is None or self.is_off():
      self.set_state(terrariumSwitch.ON)
      return self.is_on()

  def off(self):
    if self.get_state() is None or self.is_on():
      self.set_state(terrariumSwitch.OFF)
      return self.is_off()

  def dim(self,value):
    if 0 <= value <= 100:
      self.set_state(100 - value)

  def set_dimmer_on_duration(self,value):
    self.__dimmer_on_duration = float(value if float(value) >= 0.0 else 0)

  def get_dimmer_on_duration(self):
    return (self.__dimmer_on_duration if self.get_hardware_type() == 'pwm-dimmer' else 0.0)

  def set_dimmer_off_duration(self,value):
    self.__dimmer_off_duration = float(value if float(value) >= 0.0 else 0)

  def get_dimmer_off_duration(self):
    return (self.__dimmer_off_duration if self.get_hardware_type() == 'pwm-dimmer' else 0.0)

  def set_dimmer_on_percentage(self,value):
    self.__dimmer_on_percentage = float(value if (0.0 <= float(value) <= 100.0) else 100)

  def get_dimmer_on_percentage(self):
    return (self.__dimmer_on_percentage if self.get_hardware_type() == 'pwm-dimmer' else 100.0)

  def set_dimmer_off_percentage(self,value):
    self.__dimmer_off_percentage = float(value if (0.0 <= float(value) <= 100.0) else 100)

  def get_dimmer_off_percentage(self):
    return (self.__dimmer_off_percentage if self.get_hardware_type() == 'pwm-dimmer' else 0.0)
