# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

# pip install pcf8574 (pcf8574-0.1.3)
from pcf8574 import PCF8574
# pip install pcf8575
from pcf8575 import PCF8575

from . import terrariumButton


class terrariumPCF857XButton(terrariumButton):
  HARDWARE = 'magnetic-PCF857X'
  NAME = None

  _PIN_OUT = None

  def _load_hardware(self):
    # Here we invert the values. Because when PRESSED, triggers will happen. But for a door, this is the normal case.
    self.RELEASED = 1
    self.PRESSED  = 0

    # address is expected as `[In_number],[i2c_address],[i2c_bus]`
    address = self._address
    if not address[1].startswith('0x'):
      address[1] = '0x' + address[1]

    self._device['in_port'] = int(address[0]) if self._PIN_OUT == None else self._PIN_OUT[int(address[0])]
    self._device['device'] = self._load_PCF857X(1 if len(address) != 3 else int(address[2]), int(address[1],16))

  def _get_state(self):
    return self.PRESSED if self._device['device'].port[self._device['in_port']] else self.RELEASED

  @property
  def is_open(self):
    return self.pressed

  @property
  def is_closed(self):
    return not self.is_open

class terrariumPCF8574Button(terrariumPCF857XButton):
  HARDWARE = 'magnetic-PCF8574'
  NAME = 'i2c expander PCF8574'

  _PIN_OUT = [7,6,5,4,3,2,1,0]

  def _load_PCF857X(self, i2c_bus, i2c_address):
    return PCF8574(i2c_bus, i2c_address)

class terrariumPCF8575Button(terrariumPCF857XButton):
  HARDWARE = 'magnetic-PCF8575'
  NAME = 'i2c expander PCF8575'

  _PIN_OUT = [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]

  def _load_PCF857X(self, i2c_bus, i2c_address):
    return PCF8575(i2c_bus, i2c_address)
