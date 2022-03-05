# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from pathlib import Path
import inspect
from importlib import import_module
import sys
from hashlib import md5
import RPi.GPIO as GPIO
import threading
from gevent import sleep

from terrariumUtils import terrariumUtils, terrariumCache, classproperty

from hardware.io_expander import terrariumIOExpander


class terrariumButtonException(TypeError):
  '''There is a problem with loading a hardware sensor.'''
  pass

class terrariumButtonLoadingException(terrariumButtonException):
  pass

class terrariumButtonUpdateException(terrariumButtonException):
  pass

# Factory class
class terrariumButton(object):
  HARDWARE = None
  NAME = None

  RELEASED = 0
  PRESSED  = 1

  @classproperty
  def available_hardware(__cls__):
    __CACHE_KEY = 'known_buttons'
    cache = terrariumCache()

    data = cache.get_data(__CACHE_KEY)
    if data is None:
      data = {}
      # Start dynamically loading sensors (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
      for file in sorted(Path(__file__).parent.glob('*_button.py')):
        imported_module = import_module( '.' + file.stem, package='{}'.format(__name__))

        for i in dir(imported_module):
          attribute = getattr(imported_module, i)

          if inspect.isclass(attribute) and attribute != terrariumButton and issubclass(attribute, terrariumButton):
            setattr(sys.modules[__name__], file.stem, attribute)
            data[attribute.HARDWARE] = attribute

      cache.set_data(__CACHE_KEY,data,-1)

    return data

  @classproperty
  def available_buttons(__cls__):
    data = []
    for (hardware_type, button) in __cls__.available_hardware.items():
      data.append({'hardware' : hardware_type, 'name' : button.NAME})

    return data

  # Return polymorph relay....
  def __new__(cls, id, hardware_type, address, name = '', callback = None):
    known_buttons = terrariumButton.available_hardware

    if hardware_type not in known_buttons:
      raise terrariumButtonException(f'Button of hardware type {hardware_type} is unknown.')

    return super(terrariumButton, cls).__new__(known_buttons[hardware_type])

  def __init__(self, id, _, address, name = '', callback = None):

    self._device = {'device'      : None,
                    'io_expander' : None,
                    'id'          : None,
                    'address'     : None,
                    'name'        : None,
                    'state'       : None}

    self._checker = {
      'running' : False,
      'thread'  : None
    }

    self.id       = id
    self.name     = name
    self.callback = callback

    # By setting the address, we will load the hardware.
    self.address = address

  def __repr__(self):
    return f'{self.NAME} named \'{self.name}\' at address \'{self.address}\''

  def _run(self):
    self._checker['running'] = True
    while self._checker['running']:
      new_state = self._get_state()
      if new_state != self._device['state']:
        self._device['state'] = new_state
        if self.callback is not None:
          self.callback(self.id, self._device['state'])

      sleep(.1)

  def _get_state(self):
    if self._device['io_expander'] is not None:
      # IO Expander in use
      return self.PRESSED if self._device['io_expander'].port[self._device['device']] else self.RELEASED

    else:
      return self.PRESSED if GPIO.input(self._device['device']) else self.RELEASED

  def load_hardware(self):
    address = self._address

    if len(address) >= 2:
      # IO Expander in use... Only valid for motion and magnetic... LDR seems not suitable at the moment
      if address[0].startswith('PCF8575-'):
        self._device['io_expander'] = terrariumIOExpander('PCF8575',','.join(address[1:]))
      elif address[0].startswith('PCF8574-'):
        self._device['io_expander'] = terrariumIOExpander('PCF8574',','.join(address[1:]))

      address[0] = int(address[0].split('-')[1])
      self._device['device'] =  address[0] if self._PIN_OUT == None else self._PIN_OUT[address[0]]

    else:
      self._device['device'] = terrariumUtils.to_BCM_port_number(address[0])
      GPIO.setup(self._device['device'], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Data in


    self._load_hardware()

    self._checker['thread'] = threading.Thread(target=self._run)
    self._checker['thread'].start()

  @property
  def id(self):
    if self._device['id'] is None and self.address is not None:
      self._device['id'] = md5(f'{self.HARDWARE}{self.address}'.encode()).hexdigest()

    return self._device['id']

  @id.setter
  def id(self, value):
    value = terrariumUtils.clean_address(value)
    if value is not None and '' != value:
      self._device['id'] = value

  @property
  def address(self):
    return self._device['address']

  @property
  def _address(self):
    return [ part.strip() for part in self.address.split(',') ]

  @address.setter
  def address(self, value):
    value = terrariumUtils.clean_address(value)
    if value not in [None, '', self.address]:

      if self.address is not None:
        self.stop()

      self._device['address'] = value
      self.load_hardware()

  @property
  def name(self):
    return self._device['name']

  @name.setter
  def name(self, value):
    value = terrariumUtils.clean_address(value)
    if value not in [None, '', self.name]:
      self._device['name'] = value

  @property
  def state(self):
    return self._device['state']

  @property
  def pressed(self):
    return self._device['state'] == self.PRESSED

  def calibrate(self,calibration_data):
    pass

  def update(self):
    return self.state

  def stop(self):
    self._checker['running'] = False
    self._checker['thread'].join()

    GPIO.cleanup(self._device['device'])
