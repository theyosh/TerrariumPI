# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from hashlib import md5
import threading
from gevent import sleep
import queue
import textwrap
from retry import retry
from collections import deque

from terrariumUtils import terrariumUtils, classproperty


class terrariumDisplayException(Exception):
    pass


class terrariumDisplayUnknownHardwareException(terrariumDisplayException):
    pass


class terrariumDisplayInvalidSensorTypeException(terrariumDisplayException):
    pass


class terrariumDisplayLoadingException(terrariumDisplayException):
    pass


class terrariumDisplayUpdateException(terrariumDisplayException):
    pass


# Factory class
class terrariumDisplay(object):
    HARDWARE = None
    NAME = None

    WIDTH = 0
    HEIGHT = 0
    FONT_SIZE = 1
    FONT_WIDTH = 1

    __MODE_TEXT_WRAP = 1
    __MODE_TEXT_H_SCROLL = 2
    __MODE_TEXT_H_SCROLL_ONCE = 3

    # Buffer => True will never clear screen, and always append new lines to the bottom of the display
    BUFFER = True

    @classproperty
    def available_hardware(__cls__):
        return terrariumUtils.loadHardwareDrivers( __cls__,__name__,__file__,"*_display.py")

    @classproperty
    def available_displays(__cls__):
        return [
            {"hardware": hardware_type, "name": display.NAME}
            for hardware_type, display in __cls__.available_hardware.items()
        ]

    # Return polymorph relay....
    def __new__(cls, device_id, hardware_type, address, title=None):
        known_displays = terrariumDisplay.available_hardware
        try:
            return super(terrariumDisplay, cls).__new__(known_displays[hardware_type])
        except Exception as ex:
            raise terrariumDisplayLoadingException(
                f"Error loading display device {hardware_type} at address {address}: {ex}"
            )

    def __init__(self, device_id, _, address, title=None):
        self._device = {
            "device": None,
            "address": None,
            "id": None,
            "title": None,
            "mode": None,
            "message_queue": None,
            "thread": None,
            "running": False,
            "display_buffer": None
        }

        self.id = device_id
        self.title = title

        # By setting the address, we will load the hardware.
        self.address = address
        # Initialize screen buffer lines
        self._device['display_buffer'] = deque(maxlen=int((float(self.HEIGHT) / float(self.FONT_SIZE)) - (0 if title is None else 1)))

        # Best working options: __MODE_TEXT_WRAP or __MODE_TEXT_H_SCROLL
        self.mode = self.__MODE_TEXT_H_SCROLL
        if self._device['display_buffer'].maxlen == 1:
            self.mode = self.__MODE_TEXT_H_SCROLL
            self.BUFFER = False

        self._device["message_queue"] = queue.Queue()
        self._device["thread"] = threading.Thread(target=self.__run)
        self._device["thread"].start()

        self.clear()
        self.write_title()


    def __repr__(self):
        return f"{self.NAME} at address '{self.address}' ({self.width}x{self.height})"

    def __run(self):
        if self._device["device"] is None:
            return

        self._device["running"] = True
        while self._device["running"]: # When stopped,
            try:
                text = self._device["message_queue"].get(False)
                # This is a single new message of X length
                self.write_text(text)
                self._device["message_queue"].task_done()
            except queue.Empty:
                sleep(0.1)

        # Flush the queue if not empty
        while not self._device["message_queue"].empty():
            self._device["message_queue"].get(False)
            self._device["message_queue"].task_done()

    @property
    def id(self):
        if self._device["id"] is None:
            self._device["id"] = md5(f"{self.HARDWARE}{self.address}").hexdigest()
        return self._device["id"]

    @id.setter
    def id(self, value):
        if value is not None and "" == value.strip():
            self._device["id"] = value.strip()

    @property
    def address(self):
        return self._device["address"]

    @property
    def _address(self):
        return terrariumUtils.getI2CAddress(self.address)

    @address.setter
    def address(self, value):
        value = terrariumUtils.clean_address(value)
        if value not in [None, "", self.address]:
            if self.address is not None:
                self.stop()

            self._device["address"] = value
            self.load_hardware()

    @property
    def title(self):
        return self._device["title"]

    @title.setter
    def title(self, value):
        self._device["title"] = None if value is None else value.strip()

    @property
    def width(self):
        return self.WIDTH

    @property
    def height(self):
        return self.HEIGHT

    @property
    def mode(self):
        return self._device["mode"]

    @mode.setter
    def mode(self, value):
        if value in [self.__MODE_TEXT_WRAP, self.__MODE_TEXT_H_SCROLL, self.__MODE_TEXT_H_SCROLL_ONCE]:
            self._device["mode"] = value

    def message(self, text):
        if self._device["running"]:
            self._device["message_queue"].put(text)

    def clear(self):
        title_offset = 0 if self.title is None else 1
        for line_nr in range(title_offset, int(self.HEIGHT/ self.FONT_SIZE)):
            self.write_line("", line_nr)

    def write_title(self):
        if self.title is not None:
            self.write_line(self.title)

    def write_lines(self, lines):
        title_offset = 0 if self.title is None else 1
        max_lines = int((self.HEIGHT / self.FONT_SIZE) - title_offset)
        for line_nr, line in enumerate(lines):
            if not self._device["running"]:
                break

            if line_nr >= max_lines:
                continue

            self.write_line(line, line_nr + title_offset, self.mode != self.__MODE_TEXT_WRAP and line_nr == len(lines)-1)

    def write_line(self, line, line_nr = 0, scroll = False):
        line_nr += 1
        max_chars = int(float(self.WIDTH) / float(self.FONT_WIDTH))

        self._write_line(line, line_nr)

        if scroll and len(line) > max_chars:
            sleep(0.25)
            for i in range(1,len(line) - max_chars):
                if not self._device["running"]:
                    break

                self._write_line(line[i:], line_nr)
                sleep(0.01)

            if self.mode != self.__MODE_TEXT_H_SCROLL_ONCE:
                sleep(0.01)
                for i in range(len(line) - max_chars, 1, -1):
                    if not self._device["running"]:
                        break
                    self._write_line(line[i:], line_nr)
                    sleep(0.01)

            self._write_line(line, line_nr)

        sleep(0.25)


    def write_text(self, text):
        if self._device["device"] is None or "" == text:
            return

        # First make sure new lines are kept.
        text = text.strip().split("\n")
        if self.mode in [self.__MODE_TEXT_WRAP]:
            # Reformat all text lines to max screen width and add more lines when needed
            temp_lines = []
            for line in text:
                temp_lines += textwrap.wrap(line, width=int(float(self.WIDTH) / float(self.FONT_WIDTH)))
            text = temp_lines

        if self.BUFFER:
            for line in text:
                self._device['display_buffer'].append(line)
                self.write_lines(self._device['display_buffer'])
        else:
            self.clear()
            self.write_lines(text)

    def stop(self):
        self._device["running"] = False
        self._device["thread"].join()
        self.unload_hardware()

    @retry(terrariumDisplayLoadingException, tries=3, delay=0.5, max_delay=2, logger=logger)
    def load_hardware(self):
        try:
            self._load_hardware()
        except Exception as ex:
            raise terrariumDisplayLoadingException(f"Unable to load display {self}: {ex}")

    def unload_hardware(self):
        if self._device["device"] is not None:
            # Clear title
            self.title = None
            # Clear screen
            self.clear()
            try:
                self._unload_hardware()
                del self._device["device"]
            except Exception as ex:
                logger.warning(f"Unable to unload hardware: {ex}")

