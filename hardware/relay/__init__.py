# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

import threading
import inspect
from importlib import import_module
import sys

from pathlib import Path
from hashlib import md5
from operator import itemgetter
from func_timeout import func_timeout, FunctionTimedOut

# pip install retry
from retry import retry

from terrariumUtils import terrariumUtils, terrariumCache, classproperty


class terrariumRelayException(TypeError):
    """There is a problem with loading a hardware switch. Invalid power switch action."""

    def __init__(self, message, *args):
        self.message = message
        super().__init__(message, *args)


class terrariumRelayLoadingException(terrariumRelayException):
    pass


class terrariumRelayUpdateException(terrariumRelayException):
    pass


class terrariumRelayActionException(terrariumRelayException):
    pass


# Factory class
class terrariumRelay(object):
    HARDWARE = None
    NAME = None

    OFF = 0.0
    ON = 100.0

    _CACHE_TIMEOUT = 30
    _UPDATE_TIME_OUT = 10

    @classproperty
    def available_hardware(__cls__):
        __CACHE_KEY = "known_relays"
        cache = terrariumCache()

        data = cache.get_data(__CACHE_KEY)
        if data is None:
            data = {}
            # Start dynamically loading sensors (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
            for file in sorted(Path(__file__).parent.glob("*_relay.py")):
                imported_module = import_module("." + file.stem, package="{}".format(__name__))

                for i in dir(imported_module):
                    attribute = getattr(imported_module, i)

                    if inspect.isclass(attribute) and attribute != __cls__ and issubclass(attribute, __cls__):
                        setattr(sys.modules[__name__], file.stem, attribute)
                        data[attribute.HARDWARE] = attribute

            cache.set_data(__CACHE_KEY, data, -1)

        return data

    @classproperty
    def available_relays(__cls__):
        data = []
        for hardware_type, relay in __cls__.available_hardware.items():
            if relay.NAME is not None:
                data.append({"hardware": hardware_type, "name": relay.NAME})

        return sorted(data, key=itemgetter("name"))

    # Return polymorph relay....
    def __new__(cls, _, hardware_type, address, name="", prev_state=None, callback=None):
        known_relays = terrariumRelay.available_hardware

        if hardware_type not in known_relays:
            raise terrariumRelayException(f"Relay of hardware type {hardware_type} is unknown.")

        return super(terrariumRelay, cls).__new__(known_relays[hardware_type])

    def __init__(self, device_id, _, address, name="", prev_state=None, callback=None):
        self._device = {
            "device": None,
            "address": None,
            "name": None,
            "switch": None,
            "type": None,
            "id": None,
            "wattage": 0.0,
            "flow": 0.0,
            "last_update": 0,
            "value": self.OFF,
        }

        self.__relay_cache = terrariumCache()

        self._timer = None

        self.id = device_id
        self.name = name
        self.address = address
        self.callback = callback

        self.load_hardware()

    def __repr__(self):
        return f"{self.NAME} {self.type} named '{self.name}' at address '{self.address}'"

    @retry(terrariumRelayLoadingException, tries=3, delay=0.5, max_delay=2, logger=logger)
    def load_hardware(self):
        hardware_cache_key = md5(f"HW-{self.HARDWARE}-{self.address}".encode()).hexdigest()
        hardware = self.__relay_cache.get_data(hardware_cache_key)
        if hardware is None:
            try:
                hardware = func_timeout(self._UPDATE_TIME_OUT, self._load_hardware)

                if hardware is None:
                    raise terrariumRelayLoadingException(f"Could not load hardware for relay {self}: Unknown error")

                self.__relay_cache.set_data(hardware_cache_key, hardware, -1)
            except FunctionTimedOut:
                raise terrariumRelayLoadingException(
                    f"Could not load hardware for relay {self}: Timed out after {self._UPDATE_TIME_OUT} seconds."
                )
            except Exception as ex:
                raise terrariumRelayLoadingException(f"Could not load hardware for relay {self}: {ex}")

        self._device["device"] = hardware

    @retry(terrariumRelayActionException, tries=3, delay=0.5, max_delay=2, logger=logger)
    def __set_hardware_value(self, state):
        try:
            action_ok = func_timeout(self._UPDATE_TIME_OUT, self._set_hardware_value, (state,))
            if action_ok:
                # Update ok, store the new state
                self._device["value"] = state
            else:
                raise terrariumRelayActionException(f"Error changing relay {self} to state {state}. Error: unknown")

        except FunctionTimedOut:
            raise terrariumRelayLoadingException(
                f"Error changing relay {self} to state {state}: Timed out after {self._UPDATE_TIME_OUT} seconds."
            )
        except Exception as ex:
            raise terrariumRelayActionException(f"Error changing relay {self} to state {state}. Error: {ex}")

    @retry(terrariumRelayUpdateException, tries=3, delay=0.5, max_delay=2, logger=logger)
    def __get_hardware_value(self):
        data = None
        try:
            data = func_timeout(self._UPDATE_TIME_OUT, self._get_hardware_value)

        except FunctionTimedOut:
            logger.error(f"Error getting new data from relay {self}: Timed out after {self._UPDATE_TIME_OUT} seconds.")
        except Exception as ex:
            logger.error(f"Error getting new data from relay {self}. Error: {ex}")

        if data is None:
            raise terrariumRelayUpdateException(f"Error getting new data from relay {self}. Error: unknown")

        return data

    @property
    def id(self):
        if self._device["id"] is None and self.address is not None:
            self._device["id"] = md5(f"{self.HARDWARE}{self.address}".encode()).hexdigest()

        return self._device["id"]

    @id.setter
    def id(self, value):
        if value is not None and "" != str(value).strip():
            self._device["id"] = str(value).strip()

    @property
    def address(self):
        return self._device["address"]

    @property
    def _address(self):
        return [part.strip() for part in self.address.split(",")]

    @address.setter
    def address(self, value):
        value = terrariumUtils.clean_address(value)
        if value is not None and "" != value:
            self._device["address"] = value

    @property
    def device(self):
        return self._device["device"]

    @property
    def name(self):
        return self._device["name"]

    @name.setter
    def name(self, value):
        if value is not None and "" != str(value).strip():
            self._device["name"] = str(value).strip()

    @property
    def state(self):
        return self._device["value"]

    def set_state(self, new_state, force=False, no_callback=False):
        if new_state is None or not (self.OFF <= new_state <= self.ON):
            logger.error(f"Illegal value for relay {self}: {new_state}")
            return False

        changed = False
        if self.state != new_state or terrariumUtils.is_true(force):
            old_state = self.state

            try:
                self.__set_hardware_value(new_state)
                # logger.info(f'Changed relay {self} from state \'{old_state}\' to state \'{new_state}\'')

            except Exception as ex:
                logger.error(f"Error changing state for relay {self} to {new_state} :{ex}")

            if (old_state is not None) or (old_state is None and new_state == 0):
                # This is due to a bug that will graph 0 watt usage in the graph after rebooting.
                # Fix is to add power and water usage in constructor
                changed = old_state != self.state

        if changed and not no_callback and self.callback is not None:
            self.callback(self.id, new_state)

        return changed

    def update(self, force=False):
        new_data = None
        try:
            new_data = self.__get_hardware_value()
        except Exception as ex:
            logger.error(ex)

        self._device["value"] = new_data
        return self._device["value"]

    def on(self, value=100, delay=0.0):
        if self._timer is not None and self._timer.is_alive():
            return False

        changed = self.state != value
        if delay > 0.0:
            self._timer = threading.Timer(delay, lambda: self.set_state(value))
            self._timer.name = f"Delay_{value}"
            self._timer.start()
        else:
            changed = self.set_state(value)
            self._timer = None

        # Not great, but the set_state has a callback for updates
        return changed

    def off(self, value=0, delay=0.0):
        return self.on(value, delay)

    def is_on(self):
        on = self.state == self.ON
        if self._timer is not None and self._timer.is_alive():
            delay_on = float(self._timer.name.split("_")[1])
            on = delay_on == self.ON

        return on

    def is_off(self):
        off = self.state == self.OFF
        if self._timer is not None and self._timer.is_alive():
            delay_off = float(self._timer.name.split("_")[1])
            off = delay_off == self.OFF

        return off

    @property
    def is_dimmer(self):
        return self.HARDWARE.endswith("-dimmer")

    @property
    def type(self):
        return "dimmer" if self.is_dimmer else "relay"

    def stop(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer.join()

    # Auto discovery of running/connected power switches
    @staticmethod
    def scan_relays(callback=None, **kwargs):
        for hardware_type, relay_device in terrariumRelay.available_hardware.items():
            logger.debug(f"Scanning for {hardware_type} at {relay_device}")
            try:
                for relay in relay_device._scan_relays(callback, **kwargs):
                    yield relay
            except AttributeError as ex:
                # The relay does not support scanning. Just ignore
                logger.debug(f"Relay {relay_device} does not support scanning: {ex}")


class terrariumRelayDimmer(terrariumRelay):
    TYPE = None
    _DIMMER_MAXDIM = None

    def __init__(self, relay_id, _, address, name="", prev_state=None, callback=None):
        self._dimmer_offset = 0
        self._dimmer_state = 0
        self._legacy = False

        self.running = False
        self.__running = threading.Event()
        self.__thread = None
        super().__init__(relay_id, _, address, name, prev_state, callback)

    def __run(self, to, duration):
        self.running = True
        self.__running.clear()

        current_state = self.state
        steps = abs(to - current_state)
        direction = 1 if current_state < to else -1
        pause_time = duration / steps

        for _ in range(int(steps)):
            if not self.running:
                break

            current_state += direction
            self.set_state(current_state)
            self.__running.wait(timeout=pause_time)

        # Somehow the led-warrior18-dimmer does not go fully off when slowly dimming.
        # So ramping it up a bit and then set to 0 hoping this will fully shutdown the dimmer.
        # https://github.com/theyosh/TerrariumPI/issues/798
        # This seems to work, and therefore enable it for all dimmers
        if to < 1.0:
            self.set_state(5, True, True)
        # Force the 'to' value at the end to make sure the dimmer is at the actual value
        self.set_state(to)

        self.__running.set()
        self.running = False
        self.__thread = None

    def calibrate(self, data):
        dimmer_offset = data.get("dimmer_offset", self._dimmer_offset)
        if "" == dimmer_offset:
            dimmer_offset = 0

        self._dimmer_offset = int(dimmer_offset)

        max_power = data.get("dimmer_max_power", -1)
        if "" == max_power:
            max_power = -1

        max_power = int(max_power)
        if 0 <= max_power <= 100:
            self.ON = max_power
            if self.state > self.ON:
                # Current power is higher then the new limit. So lower down the power now!
                self.on(self.ON, 0)

    def on(self, value=100, duration=0.0, delay=0.0):
        if self._timer is not None and self._timer.is_alive():
            return False

        if self.__thread is not None and self.__thread.is_alive():
            return False

        changed = self.state != value
        if delay > 0.0:
            self._timer = threading.Timer(delay, lambda: self.on(value, duration, 0))
            self._timer.name = f"Delay_{value}"
            self._timer.start()
        else:
            # We assume when the to value is >- 0.9, it should off. So we force to zero (0%)
            value = round(value) if value > 1.0 else 0.0
            # Make sure we set the value within the specified limits
            value = max(self.OFF, min(self.ON, value))

            if 0 == duration:
                self._timer = None
                return self.set_state(value)

            # Start the thread for the dimmer to go to the requested value in duration time
            self.__thread = threading.Thread(target=self.__run, args=(value, duration))
            self.__thread.name = f"End_{value}"
            self.__thread.start()

        return changed

    def off(self, value=0, duration=0.0, delay=0.0):
        return self.on(value, duration, delay)

    def is_on(self):
        on = super().is_on()
        if self.__thread is not None and self.__thread.is_alive():
            thread_on = float(self.__thread.name.split("_")[1])
            on = thread_on == self.ON

        return on

    def is_off(self):
        off = super().is_off()
        if self.__thread is not None and self.__thread.is_alive():
            thread_off = float(self.__thread.name.split("_")[1])
            off = thread_off == self.OFF

        return off

    def stop(self):
        self.running = False
        self.__running.set()

        if self.__thread is not None:
            self.__thread.join()

        super().stop()
