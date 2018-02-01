# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import pigpio
import thread
import time
import math
import requests
import datetime

from pylibftdi import Driver, BitBangDevice, SerialDevice, Device
from hashlib import md5
from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumSwitch():
  VALID_HARDWARE_TYPES = ['ftdi','gpio','gpio-inverse','pwm-dimmer','remote','remote-dimmer']

  OFF = False
  ON = True

  # PWM Dimmer settings
  PWM_DIMMER_MAXDIM = 880 # http://www.esp8266-projects.com/2017/04/raspberry-pi-domoticz-ac-dimmer-part-1/
  PWM_DIMMER_MIN_TIMEOUT=0.2
  PWM_DIMMER_MIN_STEP=1

  BITBANG_ADDRESSES = {
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

  def __init__(self, id, hardware_type, address, name = '', power_wattage = 0.0, water_flow = 0.0, callback = None):
    self.id = id
    self.state = None
    self.callback = callback

    self.set_hardware_type(hardware_type)

    if self.get_hardware_type() == 'ftdi':
      self.__load_ftdi_device()
    elif self.get_hardware_type() == 'pwm-dimmer':
      self.__load_pwm_device()
    elif 'remote' in self.get_hardware_type():
      pass
    elif 'gpio' in self.get_hardware_type():
      self.__load_gpio_device()

    self.set_address(address)
    self.set_name(name)
    self.set_power_wattage(power_wattage)
    self.set_water_flow(water_flow)

    # Init system default timer settings
    self.set_timer_enabled(False)
    self.set_timer_start('00:00')
    self.set_timer_stop('00:00')
    self.set_timer_on_duration(0)
    self.set_timer_off_duration(0)

    if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer']:
      # Init system default dimmer settings
      self.set_dimmer_duration(10)
      self.set_dimmer_on_duration(5)
      self.set_dimmer_on_percentage(100)
      self.set_dimmer_off_duration(5)
      self.set_dimmer_off_percentage(0)

    if self.id is None:
      self.id = md5(b'' + self.get_hardware_type() + self.get_address()).hexdigest()

    logger.info('Loaded switch \'%s\' with values: power %.2fW and waterflow %.3fL/s' %
                (self.get_name(),
                 self.get_power_wattage(),
                 self.get_water_flow()))

    # Force to off state!
    self.set_state(terrariumSwitch.OFF,True)

  def __load_ftdi_device(self):
    for device in Driver().list_devices():
      vendor, product, self.device = map(lambda x: x.decode('latin1'), device)
      self.device_type = 'Serial' if product.endswith('UART') else 'BitBang'
      logger.debug('Found switch board %s, %s, %s, of type %s' % (vendor,product,self.device,self.device_type))
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

  def __dim_switch(self,from_value,to_value,duration):
    # When the dimmer is working, ignore new state changes.
    if not self.__dimmer_running:
      self.__pigpio.set_pull_up_down(terrariumUtils.to_BCM_port_number(self.get_address()), pigpio.PUD_OFF)
      self.__dimmer_running = True

      if from_value is None or duration == 0:
        logger.info('Switching dimmer \'%s\' from %s%% to %s%% instantly',
                  self.get_name(),from_value,to_value)
        # Geen animatie, gelijk to_value
        dim_value = terrariumSwitch.PWM_DIMMER_MAXDIM * ((100.0 - float(to_value)) / 100.0)
        self.__pigpio.hardware_PWM(terrariumUtils.to_BCM_port_number(self.get_address()), 5000, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle
      else:
        from_value = float(from_value)
        to_value = float(to_value)
        direction = (1.0 if from_value < to_value else -1.0)

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
          self.__pigpio.hardware_PWM(terrariumUtils.to_BCM_port_number(self.get_address()), 5000, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle
          time.sleep(duration)

        # For impatient people... Put the dimmer at the current state value if it has changed during the animation
        dim_value = terrariumSwitch.PWM_DIMMER_MAXDIM * ((100.0 - self.get_state()) / 100.0)
        self.__pigpio.hardware_PWM(terrariumUtils.to_BCM_port_number(self.get_address()), 5000, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle

      self.__dimmer_running = False
      logger.info('Dimmer \'%s\' is done at value %s%%',self.get_name(),self.get_state())
    else:
      logger.warning('Dimmer %s is already working. Ignoring state change!. Will switch to latest state value when done', self.get_name())

  def __calculate_time_table(self):
    logger.info('Calculating timer -=- Calculating timer -=- Calculating timer -=- Calculating timer');
    self.__timer_time_table = []
    if self.state is None or \
       not self.get_timer_enabled() or \
       (self.get_timer_on_duration() == 0 and self.get_timer_off_duration() == 0):

      return False

    logger.info('Calculating timer \'%s\' with timer data: enabled = %s, start = %s, stop = %s, on duration = %s, off duration = %s',
      self.get_name(),
      self.get_timer_enabled(),
      self.get_timer_start(),
      self.get_timer_stop(),
      self.get_timer_on_duration(),
      self.get_timer_off_duration())

    self.__timer_time_table = terrariumUtils.calculate_time_table(self.get_timer_start(),
                                                                  self.get_timer_stop(),
                                                                  self.get_timer_on_duration(),
                                                                  self.get_timer_off_duration())
    logger.info('Timer time table loaded for switch \'%s\' with %s entries.', self.get_name(),len(self.__timer_time_table))

  def set_state(self, state, force = False):
    if self.get_state() is not state or force:
      if self.get_hardware_type() == 'ftdi':
        try:
          if 'BitBang' == self.device_type:
            with BitBangDevice(self.device) as device:
              device.baudrate = 9600
              if state is terrariumSwitch.ON:
                device.port |= int(terrariumSwitch.BITBANG_ADDRESSES[str(self.get_address())], 16)
              else:
                device.port &= ~int(terrariumSwitch.BITBANG_ADDRESSES[str(self.get_address())], 16)
              device.close()

          elif 'Serial' == self.device_type:
            with SerialDevice(self.device) as device:
              device.baudrate = 9600
              cmd = chr(0xff) + chr(0x0 + int(self.get_address())) + chr(0x0 + (1 if state is terrariumSwitch.ON else 0))
              device.write(cmd)
              device.close()

        except Exception, err:
          # Ignore for now
          pass

      elif self.get_hardware_type() == 'gpio':
        GPIO.output(int(self.get_address()), ( GPIO.HIGH if state is terrariumSwitch.ON else GPIO.LOW ))

      elif self.get_hardware_type() == 'gpio-inverse':
        GPIO.output(int(self.get_address()), ( GPIO.LOW if state is terrariumSwitch.ON else GPIO.HIGH ))

      elif self.get_hardware_type() == 'pwm-dimmer' and self.__pigpio is not False:
        duration = self.get_dimmer_duration()
        # State 100 = full on which means 0 dim.
        # State is inverse of dim
        if state is terrariumSwitch.ON:
          state = self.get_dimmer_on_percentage()
          duration = self.get_dimmer_on_duration()
        elif state is terrariumSwitch.OFF or not (0 <= state <= 100):
          state = self.get_dimmer_off_percentage()
          duration = self.get_dimmer_off_duration()

        thread.start_new_thread(self.__dim_switch, (self.state,state,duration))
      elif 'remote' in self.get_hardware_type():
        # Not yet implemented
        pass

      self.state = state
      if self.get_hardware_type() != 'pwm-dimmer':
        logger.info('Toggle switch \'%s\' from %s',self.get_name(),('off to on' if self.is_on() else 'on to off'))
      if self.callback is not None:
        data = self.get_data()
        self.callback(data)

    return self.get_state() == state

  def timer(self):
    if self.get_timer_enabled():
      logger.info('Checking timer time table for switch %s with %s entries.', self.get_name(),len(self.__timer_time_table))
      switch_state = None
      now = datetime.datetime.today()
      for time_schedule in self.__timer_time_table:
        if now > time_schedule[0] and now < time_schedule[1]:
          switch_state = True
          break

        elif now < time_schedule[0]:
          switch_state = False
          break

      logmessage = 'State not changed.'
      if switch_state is not None and 'dimmer' not in self.get_hardware_type() and self.get_state() != switch_state:
        logmessage = 'Switched to state %s.' % ('on' if switch_state else 'off')

      if switch_state is None:
        self.__calculate_time_table()
        switch_state = False

      if switch_state is True:
        self.on()
      else:
        self.off()

      logger.info('Timer action is done for switch %s. %s', self.get_name(),logmessage)

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
            'timer_enabled': self.get_timer_enabled(),
            'timer_start': self.get_timer_start(),
            'timer_stop' : self.get_timer_stop(),
            'timer_on_duration': self.get_timer_on_duration(),
            'timer_off_duration': self.get_timer_off_duration()
            }

    if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer']:
      data.update({ 'dimmer_duration': self.get_dimmer_duration(),
                    'dimmer_on_duration': self.get_dimmer_on_duration(),
                    'dimmer_on_percentage' : self.get_dimmer_on_percentage(),
                    'dimmer_off_duration': self.get_dimmer_off_duration(),
                    'dimmer_off_percentage': self.get_dimmer_off_percentage()
                  })

    return data

  def update(self):
    if 'remote' in self.get_hardware_type():
      url_data = terrariumUtils.parse_url(self.get_address())
      if url_data is False:
        logger.error('Remote url \'%s\' for switch \'%s\' is not a valid remote source url!' % (self.get_address(),self.get_name()))
      else:
        try:
          data = requests.get(self.get_address(),auth=(url_data['username'],url_data['password']),timeout=3)

          if data.status_code == 200:
            data = data.json()
            json_path = url_data['fragment'].split('/') if 'fragment' in url_data and url_data['fragment'] is not None else []

            for item in json_path:
              # Dirty hack to process array data....
              try:
                item = int(item)
              except Exception, ex:
                item = str(item)

              data = data[item]

            if 'remote' == self.get_hardware_type():
              self.set_state(terrariumUtils.is_true(data))
            elif 'remote-dimmer' == self.get_hardware_type():
              self.set_state(int(data))

          else:
            logger.warning('Remote switch \'%s\' got error from remote source \'%s\':' % (self.get_name(),self.get_address(),data.status_code))
        except Exception:
          logger.exception('Remote switch \'%s\' got error from remote source \'%s\':' % (self.get_name(),self.get_address()))

  def get_id(self):
    return self.id

  def get_hardware_type(self):
    return self.hardwaretype

  def set_hardware_type(self,type):
    if type in terrariumSwitch.VALID_HARDWARE_TYPES:
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
    if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer']:
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
    if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer']:
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
    if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer']:
      return self.get_state() > self.get_dimmer_off_percentage()
    else:
      return self.get_state() is terrariumSwitch.ON

  def is_off(self):
    if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer']:
      return self.get_state() <= self.get_dimmer_off_percentage()
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

  def is_pwm_dimmer(self):
    return self.get_hardware_type() == 'pwm-dimmer'

  def dim(self,value):
    if 0 <= value <= 100:
      self.set_state(100 - value)

  def set_dimmer_duration(self,value):
    value = float(value) if terrariumUtils.is_float(value) else 0.0
    self.__dimmer_duration = value if value >= 0.0 else 0.0

  def get_dimmer_duration(self):
    return (self.__dimmer_duration if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer'] else 0.0)

  def set_dimmer_on_duration(self,value):
    value = float(value) if terrariumUtils.is_float(value) else 0.0
    self.__dimmer_on_duration = value if value >= 0.0 else 0.0

  def get_dimmer_on_duration(self):
    return (self.__dimmer_on_duration if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer'] else 0.0)

  def set_dimmer_off_duration(self,value):
    value = float(value) if terrariumUtils.is_float(value) else 0.0
    self.__dimmer_off_duration = value if value >= 0.0 else 0.0

  def get_dimmer_off_duration(self):
    return (self.__dimmer_off_duration if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer'] else 0.0)

  def set_dimmer_on_percentage(self,value):
    value = float(value) if terrariumUtils.is_float(value) else 0.0
    self.__dimmer_on_percentage = value if (0.0 <= value <= 100.0) else 100.0

  def get_dimmer_on_percentage(self):
    return (self.__dimmer_on_percentage if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer'] else 100.0)

  def set_dimmer_off_percentage(self,value):
    value = float(value) if terrariumUtils.is_float(value) else 0.0
    self.__dimmer_off_percentage = value if (0.0 <= value <= 100.0) else 100.0

  def get_dimmer_off_percentage(self):
    return (self.__dimmer_off_percentage if self.get_hardware_type() in ['pwm-dimmer','remote-dimmer'] else 0.0)

  def set_timer_enabled(self,value):
    self.__timer_enabled = terrariumUtils.is_true(value)
    self.__calculate_time_table()

  def get_timer_enabled(self):
    return (self.__timer_enabled if self.__timer_enabled in [True,False] else False)

  def set_timer_start(self,value):
    self.__timer_start = terrariumUtils.parse_time(value)
    self.__calculate_time_table()

  def get_timer_start(self):
    return self.__timer_start

  def set_timer_stop(self,value):
    self.__timer_stop = terrariumUtils.parse_time(value)
    self.__calculate_time_table()

  def get_timer_stop(self):
    return self.__timer_stop

  def set_timer_on_duration(self,value):
    if terrariumUtils.is_float(value) and int(value) >= 0:
      self.__timer_on_duration = int(value)
      self.__calculate_time_table()

  def get_timer_on_duration(self):
    return self.__timer_on_duration

  def set_timer_off_duration(self,value):
    if terrariumUtils.is_float(value) and int(value) >= 0:
      self.__timer_off_duration = int(value)
      self.__calculate_time_table()

  def get_timer_off_duration(self):
    return self.__timer_off_duration
