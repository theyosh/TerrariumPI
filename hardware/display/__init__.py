# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from pathlib import Path
import inspect
from importlib import import_module
import sys
from hashlib import md5
import threading
from gevent import sleep
import queue
import textwrap
from retry import retry

from terrariumUtils import terrariumUtils, terrariumCache, classproperty


class terrariumDisplayLoadingException(TypeError):
    """There is a problem with loading a hardware display."""


class terrariumDisplayException(TypeError):
    """There is a general problem with the display."""


# Factory class
class terrariumDisplay(object):
    HARDWARE = None
    NAME = None

    __MODE_TEXT_WRAP = 1
    __MODE_TEXT_H_SCROLL = 2
    __MODE_TEXT_H_SCROLL_ONCE = 3

    @classproperty
    def available_hardware(__cls__):
        __CACHE_KEY = "known_displays"
        cache = terrariumCache()

        data = cache.get_data(__CACHE_KEY)
        if data is None:
            data = {}
            # Start dynamically loading sensors (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
            for file in sorted(Path(__file__).parent.glob("*_display.py")):
                imported_module = import_module("." + file.stem, package="{}".format(__name__))

                for i in dir(imported_module):
                    attribute = getattr(imported_module, i)

                    if (
                        inspect.isclass(attribute)
                        and attribute != terrariumDisplay
                        and issubclass(attribute, terrariumDisplay)
                    ):
                        setattr(sys.modules[__name__], file.stem, attribute)
                        data[attribute.HARDWARE] = attribute

            cache.set_data(__CACHE_KEY, data, -1)

        return data

    @classproperty
    def available_displays(__cls__):
        data = []
        for hardware_type, button in __cls__.available_hardware.items():
            data.append({"hardware": hardware_type, "name": button.NAME})

        return data

    # Return polymorph relay....
    def __new__(cls, device_id, hardware_type, address, title=None, width=16, height=2):
        known_displays = terrariumDisplay.available_hardware

        if hardware_type not in known_displays:
            raise terrariumDisplayException(f"Dislay of hardware type {hardware_type} is unknown.")

        return super(terrariumDisplay, cls).__new__(known_displays[hardware_type])

    def __init__(self, device_id, _, address, title=None, width=16, height=2):
        self._device = {
            "device": None,
            "address": None,
            "id": None,
            "title": None,
            "width": None,
            "height": None,
            "mode": None,
            "fontsize": 1,
            "fontwidth": 1,
            "font": None,
            "queue": None,
            "thread": None,
            "running": False,
        }

        self.id = device_id
        self.title = title
        self.width = width
        self.height = height

        self.mode = self.__MODE_TEXT_WRAP

        # By setting the address, we will load the hardware.
        self.address = address

        self._device["queue"] = queue.Queue(maxsize=3 * self.height)
        self._device["thread"] = threading.Thread(target=self.__run)
        self._device["thread"].start()

        self.clear()

    def __repr__(self):
        return f"{self.NAME} at address '{self.address}' ({self.width}x{self.height})"

    def __run(self):
        if self._device["device"] is None:
            return

        self._device["running"] = True
        while self._device["running"] or not self._device["queue"].empty():
            try:
                text = self._device["queue"].get(False)
                self.write_text(text)
                self._device["queue"].task_done()
            except queue.Empty:
                sleep(0.1)

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
        address = [part.strip() for part in self.address.split(",")]
        if isinstance(address[0], str):
            if not address[0].startswith("0x"):
                address[0] = "0x" + address[0]
            address[0] = int(address[0], 16)

        return address

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
        if value is not None and not "" == value.strip():
            self._device["title"] = value.strip()

    @property
    def width(self):
        return self._device["width"]

    @width.setter
    def width(self, value):
        self._device["width"] = value

    @property
    def height(self):
        return self._device["height"]

    @height.setter
    def height(self, value):
        self._device["height"] = value

    @property
    def mode(self):
        return self._device["mode"]

    @mode.setter
    def mode(self, value):
        if value in [self.__MODE_TEXT_WRAP, self.__MODE_TEXT_H_SCROLL, self.__MODE_TEXT_H_SCROLL_ONCE]:
            self._device["mode"] = value

    @property
    def fontsize(self):
        return self._device["fontsize"]

    @property
    def font(self):
        return self._device["font"]

    def message(self, text):
        if self._device["running"]:
            self._device["queue"].put(text)

    def stop(self, wait=True):
        self._device["running"] = False
        if wait:
            self._device["queue"].join()

    def write_text(self, text="", line=1):
        if self._device["device"] is None:
            return

        max_screen_lines = int(self.height / self.fontsize)
        max_chars_per_line = int(float(self.width) / self._device["fontwidth"])

        # print(f'Max chars: {max_chars_per_line} -> Width: {self.width} , font size: {self._device["fontwidth"]}')

        # print('Font width: {} -> {} / {} = {}'.format(self._device['fontwidth'], self.width, self._device['fontwidth'], self.width / self._device['fontwidth']))
        # print('Max chars on 1 line: {}'.format(max_chars_per_line))
        text = text.split("\n")
        if self.__MODE_TEXT_WRAP == self.mode:
            temp_lines = []
            for line in text:
                temp_lines += textwrap.wrap(line, width=max_chars_per_line)
            text = temp_lines

        self.clear()

        #    print(text)
        # How many extra lines do we have more then the max height
        # This means that many extra row up animations

        if self.title is not None:
            max_screen_lines -= 1

        line_animations = max(0, len(text) - max_screen_lines)

        #   print(f'Line animation: {line_animations}, max lines: {max_screen_lines}')

        for animation_step in range(line_animations + 1):
            # Here we select the max amount of text we can display once (max height) starting with the animation step as start.
            # This will make the text shift up with one line each round
            for line_nr, line in enumerate(text[animation_step : (animation_step + max_screen_lines)]):
                screen_line_number_offset = 1
                if self.title is not None:
                    screen_line_number_offset += 1
                # Here we check if there what the max length of the line is. If it is more then the max width, we need to animate horizontal
                # But we only animate horizontal the first time we show the line. Not when it shifts up... (takes so much more time)
                # That means after animation step, only the last line will scroll
                extra_chars = 0
                if 0 == animation_step or max_screen_lines - screen_line_number_offset == line_nr:
                    extra_chars = max(0, len(line) - max_chars_per_line)

                # Here we animate horizontal one single line. Only when extra_chars is higher then 0
                for char_step in range(extra_chars + 1):
                    # Show the text line. This is a substring of max width characters, starting at char_step
                    self._write_line(
                        line[char_step : (char_step + max_chars_per_line)].ljust(max_chars_per_line),
                        line_nr + screen_line_number_offset,
                    )
                    if extra_chars > 0:
                        # If we have extra chars, we pause and show the same line again, but then 1 character shifted to the left
                        sleep(0.1)

                # If we have normal horizontal scrolling, we will scroll backwards.
                if self.__MODE_TEXT_H_SCROLL == self.mode:
                    sleep(0.25)
                    if extra_chars > 0:
                        for char_step in range(extra_chars + 1, 0, -1):
                            self._write_line(
                                line[char_step : (char_step + max_chars_per_line)].ljust(max_chars_per_line),
                                line_nr + screen_line_number_offset,
                            )
                            sleep(0.1)
                # Else we just revert the text back to show only the first max width characters
                elif self.__MODE_TEXT_H_SCROLL_ONCE == self.mode:
                    sleep(0.25)
                    self._write_line(
                        line[:max_chars_per_line].ljust(max_chars_per_line), line_nr + screen_line_number_offset
                    )

            if line_animations > 0:
                sleep(0.75)

        sleep(1)

    @retry(terrariumDisplayLoadingException, tries=3, delay=0.5, max_delay=2, logger=logger)
    def load_hardware(self, reload=False):
        try:
            self._load_hardware()
        except Exception as ex:
            raise terrariumDisplayLoadingException(f"Unable to load display {self}: {ex}")

    def unload_hardware(self):
        if self._device["device"] is not None:
            try:
                self._unload_hardware()
                del self._device["device"]
            except Exception as ex:
                logger.warning(f"Unable to unload hardware: {ex}")

    def clear(self):
        if self.title is not None:
            self._write_title()
