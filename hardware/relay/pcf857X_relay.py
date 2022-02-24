# pip install pcf8574
from pcf8574 import PCF8574
# pip install pcf8575
from pcf8575 import PCF8575

from . import terrariumRelay

class terrariumRelayPCF857X(terrariumRelay):
  HARDWARE = 'PCF857X'
  NAME = None

  #invert on/off
  _INTERNAL_ON = False
  _INTERNAL_OFF = True

  _PIN_OUT = None

  def _load_hardware(self):
    # address is expected as `[relay_number],[i2c_address],[i2c_bus]`
    address = self._address
    if not address[1].startswith('0x'):
      address[1] = '0x' + address[1]

    self._device['switch'] = int(address[0])
    self._device['device'] = self._get_hardware(1 if len(address) != 3 else int(address[2]), int(address[1],16))
    return self._device['device']

  def _get_hardware(self, i2c_bus, i2c_address):
      return None

  def _set_hardware_value(self, state):
    # Block Load Init State
    if self._get_hardware_value() == state:
      pass
    else:
      if state == self.ON:
        self._device['device'].set_output(self._device['switch'] if self._PIN_OUT == None else self._PIN_OUT[self._device['switch']], self._INTERNAL_ON)
      else:
        self._device['device'].set_output(self._device['switch'] if self._PIN_OUT == None else self._PIN_OUT[self._device['switch']], self._INTERNAL_OFF)
    return True

  def _get_hardware_value(self):
    return self.ON if self._device['device'].get_pin_state(self._device['switch'] if self._PIN_OUT == None else self._PIN_OUT[self._device['switch']], ) == self._INTERNAL_ON else self.OFF

class terrariumRelayPCF8574(terrariumRelayPCF857X):
  HARDWARE = 'PCF8574'
  NAME = 'i2c I/O PCF8574'

  _PIN_OUT = [7,6,5,4,3,2,1,0]

  def _get_hardware(self, i2c_bus, i2c_address):
      return PCF8574(i2c_bus, i2c_address)

class terrariumRelayPCF8575(terrariumRelayPCF857X):
  HARDWARE = 'PCF8575'
  NAME = 'i2c I/O PCF8575'

  _PIN_OUT = [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]

  # correction library change line
  # new_state = current_state | bit if value else current_state & (~bit & 0xff) ==> new_state = current_state | bit if value else current_state & (~bit & 0xffff)

  def _get_hardware(self, i2c_bus, i2c_address):
      return PCF8575(i2c_bus, i2c_address)
