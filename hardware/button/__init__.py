"""
Button package which produces different buttons to use in TerrariumPI

Raises:
    terrariumButtonException: There is a general problem with a hardware button

Returns:
    terrariumButton: A working button of specified type
"""
# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from pathlib import Path
import inspect
from importlib import import_module
import sys
from hashlib import md5
import RPi.GPIO as GPIO
import threading
from gevent import sleep

from terrariumUtils import terrariumUtils, terrariumCache, classproperty

from hardware.io_expander import terrariumIOExpander


class terrariumButtonException(TypeError):
    "There is a general problem with a hardware button."


class terrariumButtonLoadingException(terrariumButtonException):
    "There is a problem with loading a hardware button."


class terrariumButtonUpdateException(terrariumButtonException):
    "There is a problem with updating a hardware button."


# Factory class
class terrariumButton(object):
    HARDWARE = None
    NAME = None

    RELEASED = 0
    PRESSED = 1

    @classproperty
    def available_hardware(__cls__):
        __CACHE_KEY = "known_buttons"
        cache = terrariumCache()

        data = cache.get_data(__CACHE_KEY)
        if data is None:
            data = {}
            # Start dynamically loading sensors (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
            for file in sorted(Path(__file__).parent.glob("*_button.py")):
                imported_module = import_module("." + file.stem, package="{}".format(__name__))

                for i in dir(imported_module):
                    attribute = getattr(imported_module, i)

                    if (
                        inspect.isclass(attribute)
                        and attribute != terrariumButton
                        and issubclass(attribute, terrariumButton)
                    ):
                        setattr(sys.modules[__name__], file.stem, attribute)
                        data[attribute.HARDWARE] = attribute

            cache.set_data(__CACHE_KEY, data, -1)

        return data

    @classproperty
    def available_buttons(__cls__):
        data = []
        for hardware_type, button in __cls__.available_hardware.items():
            data.append({"hardware": hardware_type, "name": button.NAME})

        return data

    # Return polymorph relay....
    def __new__(cls, _, hardware_type, address, name="", callback=None):
        known_buttons = terrariumButton.available_hardware

        if hardware_type not in known_buttons:
            raise terrariumButtonException(f"Button of hardware type {hardware_type} is unknown.")

        return super(terrariumButton, cls).__new__(known_buttons[hardware_type])

    def __init__(self, button_id, _, address, name="", callback=None):
        "Create a new button based on type"

        self._device = {"device": None, "id": None, "address": None, "name": None, "state": None}

        self._checker = {"running": False, "thread": None}

        self._inverse = False

        self.id = button_id
        self.name = name
        self.callback = callback

        # By setting the address, we will load the hardware.
        self.address = address

    def __repr__(self):
        """
        Returns readable button name

        Returns:
            string: Button type and name with address
        """
        return f"{self.NAME} named '{self.name}' at address '{self.address}'"

    def _run(self):
        self._checker["running"] = True
        while self._checker["running"]:
            new_state = self._get_state()
            if new_state != self._device["state"]:
                self._device["state"] = new_state
                if self.callback is not None:
                    self.callback(self.id, self.state)

            sleep(0.1)

    def _get_state(self):
        if isinstance(self._device["device"], terrariumIOExpander):
            # IO Expander in use
            state = self._device["device"].state
            if state is None:
                # Device in error...
                return None
            else:
                return self.PRESSED if state else self.RELEASED

        else:
            return self.PRESSED if GPIO.input(self._device["device"]) else self.RELEASED

    def load_hardware(self):
        address = self._address

        if terrariumUtils.is_valid_url(self.address):
            # Remote button
            self._device["device"] = self.address

        elif len(address) >= 2:
            # IO Expander in use... Only valid for motion and magnetic... LDR seems not suitable at the moment
            if address[0].lower().startswith("pcf8575-"):
                self._device["device"] = terrariumIOExpander("PCF8575", ",".join(address[1:]))
            elif address[0].lower().startswith("pcf8574-"):
                self._device["device"] = terrariumIOExpander("PCF8574", ",".join(address[1:]))

            self._device["device"].set_port(int(address[0].split("-")[1]))

        else:
            self._device["device"] = terrariumUtils.to_BCM_port_number(address[0])
            GPIO.setup(self._device["device"], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Data in

        self._load_hardware()

        self._checker["thread"] = threading.Thread(target=self._run)
        self._checker["thread"].start()

    @property
    def id(self):
        if self._device["id"] is None and self.address is not None:
            self._device["id"] = md5(f"{self.HARDWARE}{self.address}".encode()).hexdigest()

        return self._device["id"]

    @id.setter
    def id(self, value):
        value = terrariumUtils.clean_address(value)
        if value is not None and "" != value:
            self._device["id"] = value

    @property
    def address(self):
        return self._device["address"]

    @property
    def _address(self):
        return [part.strip() for part in self.address.split(",")]

    @address.setter
    def address(self, value):
        value = terrariumUtils.clean_address(value)
        if value not in [None, "", self.address]:
            if self.address is not None:
                self.stop()

            self._device["address"] = value
            self.load_hardware()

    @property
    def name(self):
        return self._device["name"]

    @name.setter
    def name(self, value):
        value = terrariumUtils.clean_address(value)
        if value not in [None, "", self.name]:
            self._device["name"] = value

    @property
    def state(self):
        return self._device["state"] if not self._inverse else 1 - self._device["state"]

    @property
    def pressed(self):
        return self.state == self.PRESSED

    def calibrate(self, calibration_data):
        self._inverse = calibration_data.get("inverse", "off") == "on"

    def update(self):
        return self.state

    def stop(self):
        self._checker["running"] = False
        self._checker["thread"].join()

        if not isinstance(self._device["device"], terrariumIOExpander):
            try:
                GPIO.cleanup(self._device["device"])
            except Exception:
                logger.debug(f"Button {self} is already stopped.")
