# -*- coding: utf-8 -*-
import terrariumLogging
from terrariumUtils import classproperty, terrariumCache

logger = terrariumLogging.logging.getLogger(__name__)

# pip install pcf8574 (pcf8574-0.1.3)
from pcf8574 import PCF8574
# pip install pcf8575
from pcf8575 import PCF8575


class terrariumIOExpanderException(TypeError):
  '''There is a problem with loading a hardware IO expander.'''
  pass

class terrariumIOExpander(object):
  HARDWARE = None
  NAME = None

  @classproperty
  def available_hardware(__cls__):
    return {'PCF8574' : lambda: terrariumPCF8574IOExpander,
            'PCF8575' : lambda: terrariumPCF8575IOExpander}

  # Return polymorph IO expander....
  def __new__(cls, hardware_type, address):
    known_devices = terrariumIOExpander.available_hardware

    if hardware_type not in known_devices:
      raise terrariumIOExpanderException(f'IO Expander of hardware type {hardware_type} is unknown.')

    return super(terrariumIOExpander, cls).__new__(known_devices[hardware_type]())

  def __init__(self, _, address):
    self.pin = None
    self.address = address
    self.__hardware_cache = terrariumCache()
    self.device = self.load_hardware()

  def __repr__(self):
    return f'IO Expander at address \'{self.address}\''

  def set_pin(self, nr):
    self.pin = nr

  @property
  def _address(self):
    address = self.address.split(',')

    if isinstance(address[0], str):
      if not address[0].startswith('0x'):
        address[0] = '0x' + address[0]
      address[0] = int(address[0],16)

    if len(address) == 1:
      address.append(1)
    else:
      address[1] = int(address[1])

    return address

  def load_hardware(self):
    address = self._address
    hardware_key = f'{self.HARDWARE}_{self.address}'
    loaded_hardware = self.__hardware_cache.get_data(hardware_key,None)

    if loaded_hardware is None:
      loaded_hardware = self._load_device(address)
      self.__hardware_cache.set_data(hardware_key, loaded_hardware, -1)

    return loaded_hardware

  @property
  def state(self):
    try:
      return True if self.device.get_pin_state(self.pin) else False
    except Exception as ex:
      logger.error(f'Got an error reading {self}: {ex}')
      return None

  @state.setter
  def state(self, state):
    try:
      return self.device.set_output(self.pin, state)
    except Exception as ex:
      logger.error(f'Got an error reading {self}: {ex}')
      return None


class terrariumPCF8574IOExpander(terrariumIOExpander):
  HARDWARE = 'PCF8574'
  NAME = 'PCF8574 Expander (8 ports)'

  def _load_device(self, address):
    return PCF8574(address[1], address[0])

class terrariumPCF8575IOExpander(terrariumIOExpander):
  HARDWARE = 'PCF8575'
  NAME = 'PCF8575 Expander (16 ports)'

  def _load_device(self, address):
    return PCF8575(address[1], address[0])