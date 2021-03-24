from . import terrariumRelay, terrariumRelayException
from terrariumUtils import terrariumUtils

from pathlib import Path

# https://github.com/SequentMicrosystems/relay8-rpi
# https://github.com/SequentMicrosystems/8relay-rpi
import sys
# For the old version (V1). New version (V3) will be installed as package
sys.path.insert(0, str((Path(__file__).parent / Path('../../3rdparty/relay8-rpi/python')).resolve()))
sys.path.insert(0, str((Path(__file__).parent / Path('../../3rdparty/4relay-rpi/python/4relay')).resolve()))

from relay8 import set as relay8SetV1
from relay8 import get as relay8GetV1

from lib8relay import set as relay8SetV3
from lib8relay import get as relay8GetV3

from lib4relay import set as relay4Set
from lib4relay import get as relay4Get

class terrariumRelay8Stack(terrariumRelay):
  HARDWARE = '8relay-stack_v1'
  NAME = 'Sequent Microsystems 8 Relay Card Ver. 1 - 2'

  def _load_hardware(self):
    address = self._address
    address[0] = int(address[0])
    if len(address) == 1:
      address.append(0)

    elif len(address) == 2:
      # Board numbers starts at '0' where the user will enter 1 as first
      address[1] = int(address[1]) - 1

    return (address[0],address[1])

  def _set_hardware_value(self, state):
    (device, nr) = self.device
    relay8SetV1(device, nr, 1 if state == self.ON else 0)
    return True

  def _get_hardware_value(self):
    (device, nr) = self.device
    data = relay8GetV1(device, nr)
    if data is None:
      return None

    return self.ON if terrariumUtils.is_true(data) else self.OFF

class terrariumRelay8StackV3(terrariumRelay8Stack):
  HARDWARE = '8relay-stack_v3'
  NAME = 'Sequent Microsystems 8 Relay Card Ver. 3'

  def _set_hardware_value(self, state):
    (device, nr) = self.device
    relay8SetV3(device, nr, 1 if state == self.ON else 0)

  def _get_hardware_value(self):
    (device, nr) = self.device
    data = relay8GetV3(device, nr)
    if data is None:
      return None

    return self.ON if terrariumUtils.is_true(data) else self.OFF

class terrariumRelay4Stack(terrariumRelay8Stack):
  HARDWARE = '4relay-stack'
  NAME = 'Sequent Microsystems 4 Relay Card'

  def _set_hardware_value(self, state):
    (device, nr) = self.device
    relay4Set(device, nr, 1 if state == self.ON else 0)

  def _get_hardware_value(self):
    (device, nr) = self.device
    data = relay4Get(device, nr)
    if data is None:
      return None

    return self.ON if terrariumUtils.is_true(data) else self.OFF