# -*- coding: utf-8 -*-
import terrariumLogging
from terrariumUtils import classproperty

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

    return super(terrariumIOExpander, cls).__new__(known_devices[hardware_type])

  def __init__(self, _, address):
    self.address = address
    self.device = self.load_hardware()

  def __repr__(self):
    return f'IO Expander at address \'{self.address}\''

  @property
  def _address(self):
    address = self.address.split(',')

    if isinstance(address[0], str):
      if not address[0].startswith('0x'):
        address[0] = '0x' + address[0]
      address[0] = int(address[0],16)

    if len(address) == 1:
      address.append(1)

    return address

  def port(self, nr, state = None):
    if state is None:
      return self.device.port(self._PIN_OUT[nr])
    else:
      self.device.set_output(self._PIN_OUT[nr], state)
      return True #?? Needed a return value for changing..


class terrariumPCF8574IOExpander(terrariumIOExpander):
  HARDWARE = 'PCF8574'
  NAME = 'PCF8574 Expander (8 ports)'

  _PIN_OUT = [7,6,5,4,3,2,1,0]

  def load_hardware(self):
    address = self._address
    return PCF8574(address[1], address[0])


class terrariumPCF8575IOExpander(terrariumIOExpander):
  HARDWARE = 'PCF8575'
  NAME = 'PCF8575 Expander (16 ports)'

  _PIN_OUT = [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]

  def load_hardware(self):
    address = self._address
    return PCF8575(address[1], address[0])