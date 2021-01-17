# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from abc import abstractmethod
from pathlib import Path
import inspect
import pkgutil
from importlib import import_module
import sys
from hashlib import md5
import pigpio

# pip install retry
from retry import retry

from terrariumUtils import terrariumUtils, terrariumCache, classproperty

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
    self._device = {'device'   : None,
                    'button'   : None,
                    'id'       : None,
                    'address'  : None,
                    'name'     : None,
                    'callback' : None,
                    'state'    : None}

    self.id = id
    self.address = address
    self.name = name

    self._device['callback'] = callback

    self.load_hardware()

#    if self._device['callback'] is not None:
#      self._device['callback'](self,int(self._device['state']))

  def _pressed(self):
    self._device['state'] = self.PRESSED
    if self._device['callback'] is not None:
      self._device['callback'](self.id, self.PRESSED)

  def _released(self):
    self._device['state'] = self.RELEASED
    if self._device['callback'] is not None:
      self._device['callback'](self.id, self.RELEASED)

  @property
  def id(self):
    if self._device['id'] is None:
      self._device['id'] = md5('{}{}'.format(self.HARDWARE, self.address).encode()).hexdigest()

    return self._device['id']

  @id.setter
  def id(self, value):
    if value is not None and '' != str(value).strip():
      self._device['id'] = str(value).strip()

  @property
  def address(self):
    return self._device['address']

  @property
  def _address(self):
    return [ part.strip() for part in self.address.split(',') ]

  @address.setter
  def address(self, value):
    value = terrariumUtils.clean_address(value)
    if value is not None and '' != value:
      self._device['address'] = value

  @property
  def name(self):
    return self._device['name']

  @name.setter
  def name(self, value):
    if value is not None and '' != str(value).strip():
      self._device['name'] = str(value).strip()

  @property
  def state(self):
    return self._device['state']

  @property
  def pressed(self):
    return self._device['state'] == self.PRESSED

  @abstractmethod
  def load_hardware(self):
    pass

  def update(self):
    return self.state

  def stop(self):
    self._device['device'].close()

  # # Return a list with type and names of supported buttons
  # @staticmethod
  # def get_available_types():
  #   known_buttons = terrariumButton.__search_buttons()

  #   data = []
  #   all_types = []
  #   for (hardware_type,button) in known_buttons.items():
  #     if button.NAME is not None:
  #       data.append({'hardware' : hardware_type, 'name' : button.NAME})

  #   return data

  # Auto discovery of running/connected buttons
  @staticmethod
  def scan_power_switches(callback=None, **kwargs):
#    logger.debug('Start scanning for power switches. We have {} devices'.format(len(POWER_SWITCHES)))
    known_buttons = terrariumButton.available_hardware
    for (hardware_type,button_device) in known_buttons.items():
      try:
        for button in button_device.scan_buttons(callback, **kwargs):
          yield button
      except AttributeError as ex:
        #print(ex)
        pass
#        logger.debug('Device \'{}\' does not support hardware scanning'.format(power_switch_device.TYPE))