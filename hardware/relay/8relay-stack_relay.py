from . import terrariumRelay
from terrariumUtils import terrariumUtils

from pathlib import Path

# https://github.com/SequentMicrosystems/relay8-rpi
# https://github.com/SequentMicrosystems/8relay-rpi
# https://github.com/SequentMicrosystems/4relind-rpi
# https://github.com/SequentMicrosystems/8relind-rpi
import sys

# For the old version (V1). New version (V3) will be installed as package
sys.path.insert(0, str((Path(__file__).parent / Path("../../3rdparty/relay8-rpi/python")).resolve()))
sys.path.insert(0, str((Path(__file__).parent / Path("../../3rdparty/4relay-rpi/python/4relay")).resolve()))
# Version 4.X
sys.path.insert(0, str((Path(__file__).parent / Path("../../3rdparty/8relind-rpi/python/8relind")).resolve()))
sys.path.insert(0, str((Path(__file__).parent / Path("../../3rdparty/4relind-rpi/python/4relind")).resolve()))

from relay8 import set as relay8SetV1
from relay8 import get as relay8GetV1

from lib4relay import set as relay4Set
from lib4relay import get as relay4Get

from lib8relay import set as relay8SetV3
from lib8relay import get as relay8GetV3

from lib4relind import set_relay as relay4SetV4
from lib4relind import get_relay as relay4GetV4

from lib8relind import set as relay8SetV4
from lib8relind import get as relay8GetV4


class terrariumRelay8Stack(terrariumRelay):
    HARDWARE = "8relay-stack_v1"
    NAME = "Sequent Microsystems 8 Relay Card Ver. 1 - 2"

    def _device_set(self, device, nr, action):
        return relay8SetV1(device, nr, action)

    def _device_get(self, device, nr):
        return relay8GetV1(device, nr)

    def _load_hardware(self):
        address = self._address
        if len(address) == 1:
            # Add board number explicit
            address.append(0)

        # Return tuple with (stack, relay)
        return (int(address[1]), int(address[0]))

    def _set_hardware_value(self, state):
        (device, nr) = self.device
        self._device_set(device, nr, 1 if state == self.ON else 0)
        return True

    def _get_hardware_value(self):
        (device, nr) = self.device
        data = self._device_get(device, nr)
        if data is None:
            return None

        return self.ON if terrariumUtils.is_true(data) else self.OFF


class terrariumRelay8StackV3(terrariumRelay8Stack):
    HARDWARE = "8relay-stack_v3"
    NAME = "Sequent Microsystems 8 Relay Card Ver. 3"

    def _device_set(self, device, nr, action):
        return relay8SetV3(device, nr, action)

    def _device_get(self, device, nr):
        return relay8GetV3(device, nr)


class terrariumRelay4Stack(terrariumRelay8Stack):
    HARDWARE = "4relay-stack"
    NAME = "Sequent Microsystems 4 Relay Card"

    def _device_set(self, device, nr, action):
        return relay4Set(device, nr, action)

    def _device_get(self, device, nr):
        return relay4Get(device, nr)


class terrariumRelay4StackV4(terrariumRelay8Stack):
    HARDWARE = "4relind-stack"
    NAME = "Sequent Microsystems 4 Relay Card Ver. 4"

    def _device_set(self, device, nr, action):
        return relay4SetV4(device, nr, action)

    def _device_get(self, device, nr):
        return relay4GetV4(device, nr)


class terrariumRelay8StackV4(terrariumRelay8Stack):
    HARDWARE = "8relind-stack"
    NAME = "Sequent Microsystems 8 Relay Card Ver. 4"

    def _device_set(self, device, nr, action):
        return relay8SetV4(device, nr, action)

    def _device_get(self, device, nr):
        return relay8GetV4(device, nr)
