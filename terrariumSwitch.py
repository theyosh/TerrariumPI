# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from pylibftdi import Driver, BitBangDevice, SerialDevice, Device
import RPi.GPIO as GPIO
from hashlib import md5

class terrariumSwitch():

  valid_hardware_types = ['ftdi','gpio','w1']

  OFF = False
  ON = True

  bitbang_addresses = {
    "1":"2",
    "2":"8",
    "3":"20",
    "4":"80",
    "all":"FF"
  }

  def __init__(self, id, hardware_type, address, name = '', power_wattage = 0, water_flow = 0, callback = None):
    self.id = id
    self.callback = callback

    self.set_hardware_type(hardware_type)

    if self.get_hardware_type() == 'ftdi':
      self.__load_ftdi_device()
    elif self.get_hardware_type() == 'gpio':
      self.__load_gpio_device()

    self.set_address(address)
    self.set_name(name)
    self.set_power_wattage(power_wattage)
    self.set_water_flow(water_flow)

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

      self.state = state
      logger.info('Toggle switch \'%s\' from %s',self.get_name(),('off to on' if self.is_on() else 'on to off'))
      if self.callback is not None:
        self.callback(self.get_data())

    return self.get_state() == state

  def get_state(self):
    return self.state

  def get_data(self):
    data = {'id' : self.get_id(),
            'hardwaretype' : self.get_hardware_type(),
            'address' : self.get_address(),
            'name' : self.get_name(),
            'power_wattage' : self.get_power_wattage(),
            'water_flow' : self.get_water_flow(),
            'state' : self.get_state()
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
    if self.get_hardware_type() == 'gpio':
      try:
        GPIO.setup(int(self.get_address()), GPIO.OUT)
      except Exception, err:
        print err
        pass

  def get_name(self):
    return self.name

  def set_name(self,name):
    self.name = name

  def get_power_wattage(self):
    return self.power_wattage

  def set_power_wattage(self,value):
    try:
      self.power_wattage = float(value)
    except Exception:
      self.power_wattage = 0

  def get_water_flow(self):
    return self.water_flow

  def set_water_flow(self,value):
    try:
      self.water_flow = float(value)
    except Exception:
      self.water_flow = 0

  def toggle(self):
    if self.get_state() is not None:
      old_state = self.get_state()
      self.set_state(not old_state)
      return self.get_state() is not old_state

    return None

  def is_on(self):
    return self.get_state() is terrariumSwitch.ON

  def is_off(self):
    return self.get_state() is terrariumSwitch.OFF

  def on(self):
    if self.get_state() is None or self.is_off():
      self.set_state(terrariumSwitch.ON)
      return self.is_on()

  def off(self):
    if self.get_state() is None or self.is_on():
      self.set_state(terrariumSwitch.OFF)
      return self.is_off()
