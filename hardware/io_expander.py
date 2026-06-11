# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from pcf8575 import PCF8575
from smbus2 import SMBus
from terrariumUtils import terrariumCache, terrariumUtils, terrariumSingleton


class terrariumIOExpanderException(TypeError):
    """There is a problem with loading a hardware IO expander."""


class terrariumIOExpander(object):
    HARDWARE = None
    NAME = None
    PORTS = 0

    def __init__(self, address):
        self.address = address

        self._internal_state = []
        self._hardware_cache = terrariumCache()
        self._device = self.load_hardware()

    def __repr__(self):
        return f"IO Expander at address '{self.address}'"

    @property
    def _address(self):
        return terrariumUtils.getI2CAddress(self.address)

    def _load_device(self, address):
        pass

    def _set_hardware(self):
        pass

    def _valid_port(self, port):
        if port < 1 or port > self.PORTS:
            raise terrariumIOExpanderException(f"Invalid port number {port} for {self}")

    def load_hardware(self):
        hardware_key = f"IO_{self.HARDWARE}_{'_'.join(map(str, self._address))}"
        loaded_hardware = self._hardware_cache.get_data(hardware_key, None)

        if loaded_hardware is None:
            loaded_hardware = self._load_device(self._address)
            if loaded_hardware is not None:
                self._hardware_cache.set_data(hardware_key, loaded_hardware, -1)

        return loaded_hardware

    def close(self):
        pass

    def switch_on(self, port):
        self._valid_port(port)
        self._internal_state[port - 1] = True
        self._set_hardware()

    def switch_off(self, port):
        self._valid_port(port)
        self._internal_state[port - 1] = False
        self._set_hardware()

    def is_on(self, port):
        self._valid_port(port)
        return self._internal_state[port - 1] == True

    def is_off(self, port):
        return not self.is_on(port)


class terrariumPCF8574IOExpander(terrariumIOExpander, terrariumSingleton):
    HARDWARE = "PCF8574"
    NAME = "PCF8574 Expander (max 8 ports)"
    PORTS = 8

    def _load_device(self, address):
        self._internal_state = self.PORTS * [False]

        return SMBus(address[1])

    def _set_hardware(self):
        # https://drive.google.com/file/d/1ZMIpPZ9RwgDZvfxSMYa3MM99ZONDWeVe/view
        self._device.write_byte(
            self._address[0], int("0b" + "".join(["0" if state else "1" for state in self._internal_state]), 2)
        )

class terrariumPCF8575IOExpander(terrariumIOExpander, terrariumSingleton):
    HARDWARE = "PCF8575"
    NAME = "PCF8575 Expander (max 16 ports)"
    PORTS = 16

    def _load_device(self, address):
        self._internal_state = self.PORTS * [False]

        return PCF8575(address[1], address[0])

    def _set_hardware(self):
        self._device.port = list(reversed([not state for state in self._internal_state]))