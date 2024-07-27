# -*- coding: utf-8 -*-
import terrariumLogging
from terrariumUtils import classproperty, terrariumCache, terrariumUtils

logger = terrariumLogging.logging.getLogger(__name__)

# pip install i2crelay (git)
from i2crelay import I2CRelayBoard


class terrariumIOExpanderException(TypeError):
    """There is a problem with loading a hardware IO expander."""


class terrariumIOExpander(object):
    HARDWARE = None
    NAME = None

    @classproperty
    def available_hardware(__cls__):
        return {"PCF8574": lambda: terrariumPCF8574IOExpander}

    # Return polymorph IO expander....
    def __new__(cls, hardware_type, address):
        known_devices = terrariumIOExpander.available_hardware
        try:
            return super(terrariumIOExpander, cls).__new__(known_devices[hardware_type]())
        except:
            raise terrariumIOExpanderException(f"IO Expander of hardware type {hardware_type} is unknown.")

    def __init__(self, _, address):
        self.port = None
        self.address = address
        self.__hardware_cache = terrariumCache()
        self.__device = self.load_hardware()

    def __repr__(self):
        return f"IO Expander at address '{self.address}' using port {self.port}"

    def set_port(self, nr):
        self.port = int(nr)

    @property
    def _address(self):
        return terrariumUtils.getI2CAddress(self.address)

    def load_hardware(self):
        hardware_key = f"IO_{self.HARDWARE}_{self.address}"
        loaded_hardware = self.__hardware_cache.get_data(hardware_key, None)

        if loaded_hardware is None:
            address = self._address
            loaded_hardware = self._load_device(address)
            if loaded_hardware is not None:
                self.__hardware_cache.set_data(hardware_key, loaded_hardware, -1)

        return loaded_hardware

    def close(self):
        pass

    @property
    def state(self):
        return self.__device.is_on(self.port)

    @state.setter
    def state(self, state):
        state = terrariumUtils.is_true(state)
        try:
            if state:
                self.__device.switch_on(self.port)
            else:
                self.__device.switch_off(self.port)

            return True
        except Exception as ex:
            logger.error(f"Got an error setting {self} to state {state}: {ex}")

        return None


class terrariumPCF8574IOExpander(terrariumIOExpander):
    HARDWARE = "PCF8574"
    NAME = "PCF8574 Expander (8 ports)"

    def _load_device(self, address):
        return I2CRelayBoard(address[1], address[0])
