#import terrariumLogging
#logger = terrariumLogging.logging.getLogger(__name__)

from abc import ABCMeta, abstractmethod
from pathlib import Path
import inspect
import pkgutil
from importlib import import_module
import sys
from hashlib import md5

from time import time, sleep

import textwrap
import queue
import threading

from terrariumUtils import terrariumSingleton, terrariumUtils

class terrariumDisplayException(TypeError):
  '''There is a problem with loading a hardware sensor.'''

  def __init__(self, message, *args):
    self.message = message
    super().__init__(message, *args)

class terrariumDisplayAbstract(metaclass=ABCMeta):
  HARDWARE = None
  NAME = None

  __MODE_TEXT_WRAP = 1
  __MODE_TEXT_H_SCROLL = 2
  __MODE_TEXT_H_SCROLL_ONCE = 3

  def __init__(self, id, address, title = None, width = 16, height = 2):
    self._device = {'device'   : None,
                    'address'  : None,
                    'id'       : None,
                    'title'    : None,
                    'width'    : None,
                    'height'   : None,
                    'mode'     : None,
                    'fontsize' : 1,
                    'fontwidth': 1,
                    'font'     : None}

    self.mode = self.__MODE_TEXT_WRAP

    self.address = address
    self.width = width
    self.height = height

    self.__message_queue = queue.Queue(maxsize = 3 * self.height)
    self.__thread = threading.Thread(target=self.__process, daemon=False).start()

    # Load hardware can update the address value that is used for making a unique ID
    self.load_hardware()

    self.id = id
    self.title = title

    self.clear()
    #self.write_text() # Makes the title shown ....

  def __process(self):
    self.__running = True
    while self.__running or not self.__message_queue.empty():
      try:
        text = self.__message_queue.get(False)
        self.write_text(text)
        self.__message_queue.task_done()
      except queue.Empty:
        sleep(0.1)

  @property
  def id(self):
    if self._device['id'] is None:
      self._device['id'] = md5('{}{}{}'.format(self.HARDWARE, self.address).encode()).hexdigest()
    return self._device['id']

  @id.setter
  def id(self, value):
    if value is not None and '' == value.strip():
      self._device['id'] = value.strip()

  @property
  def name(self):
    return self._device['name']

  @name.setter
  def name(self, value):
    if '' != value.strip():
      self._device['name'] = value.strip()

  @property
  def address(self):
    return self._device['address']

  @property
  def _address(self):
    address = [ part.strip() for part in self.address.split(',') ]
    if type(address[0]) is str:
      if not address[0].startswith('0x'):
        address[0] = '0x' + address[0]
      address[0] = int(address[0],16)

    return address

  @address.setter
  def address(self, value):
    self._device['address'] = str(value).strip().strip(',').strip()

  @property
  def title(self):
    return self._device['title']

  @title.setter
  def title(self, value):
    if value is not None and not '' == value.strip():
      self._device['title'] = value.strip()

  @property
  def width(self):
    return self._device['width']

  @width.setter
  def width(self, value):
    self._device['width'] = value

  @property
  def height(self):
    return self._device['height']

  @height.setter
  def height(self, value):
    self._device['height'] = value

  @property
  def mode(self):
    return self._device['mode']

  @mode.setter
  def mode(self, value):
    if value in [self.__MODE_TEXT_WRAP, self.__MODE_TEXT_H_SCROLL, self.__MODE_TEXT_H_SCROLL_ONCE]:
      self._device['mode'] = value

  @property
  def fontsize(self):
    return self._device['fontsize']

  @property
  def font(self):
    return self._device['font']

  def add_message(self, text):
    if self.__running:
      self.__message_queue.put(text)

  def stop(self, wait = True):
    self.__running = False
    if wait:
      self.__message_queue.join()

  def write_text(self, text = '', line = 1):
    max_screen_lines   = int(self.height / self.fontsize)
    max_chars_per_line = int(float(self.width) / self._device['fontwidth'])

    # print('Font width: {} -> {} / {} = {}'.format(self._device['fontwidth'], self.width, self._device['fontwidth'], self.width / self._device['fontwidth']))
    # print('Max chars on 1 line: {}'.format(max_chars_per_line))
    text = text.split('\n')
    if self.__MODE_TEXT_WRAP == self.mode:
      temp_lines = []
      for line in text:
        temp_lines += textwrap.wrap(line, width=max_chars_per_line)
      text = temp_lines

    self.clear()
    # How many extra lines do we have more then the max height
    # This means that many extra row up animations

    if self.title is not None:
      max_screen_lines -= 1

    line_animations = max(0,len(text) - max_screen_lines)
    for animation_step in range(line_animations+1):

      # Here we select the max amount of text we can display once (max height) starting with the animation step as start.
      # This will make the text shift up with one line each round
      for line_nr, line in enumerate(text[animation_step:(animation_step + max_screen_lines)]):
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
        for char_step in range(extra_chars+1):
          # Show the text line. This is a substring of max width characters, starting at char_step
          self._write_line(line[char_step:(char_step+max_chars_per_line)].ljust(max_chars_per_line),line_nr+screen_line_number_offset)
          if extra_chars > 0:
            # If we have exta chars, we pauze and show the same line again, but then 1 character shifted to the left
            sleep(0.1)

        # If we have normal horizontal scrolling, we will scroll backwards.
        if self.__MODE_TEXT_H_SCROLL == self.mode:
          time.sleep(0.25)
          if extra_chars > 0:
            for char_step in range(extra_chars+1,0,-1):
              self._write_line(line[char_step:(char_step+max_chars_per_line)].ljust(max_chars_per_line),line_nr+screen_line_number_offset)
              sleep(0.1)
        # Else we just revert the text back to show only the first max width characters
        elif self.__MODE_TEXT_H_SCROLL_ONCE == self.mode:
          time.sleep(0.25)
          self._write_line(line[:max_chars_per_line].ljust(max_chars_per_line),line_nr+screen_line_number_offset)

      if line_animations > 0:
        sleep(0.5)

    sleep(1)

  @abstractmethod
  def load_hardware(self):
    pass

  @abstractmethod
  def unload_hardware(self):
    pass

  @abstractmethod
  def clear(self):
    if self.title is not None:
      self._write_line(self.title[:self.width].ljust(self.width),1)

# Factory class
class terrariumDisplay(object):

  DISPLAYS = {}

  # Start dynamically loading switches (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
  for file in sorted(Path(__file__).parent.glob('*_display.py')):
    imported_module = import_module( '.' + file.stem, package='{}'.format(__name__))

    for i in dir(imported_module):
      attribute = getattr(imported_module, i)

      if inspect.isclass(attribute) and attribute != terrariumDisplayAbstract and issubclass(attribute, terrariumDisplayAbstract):
        setattr(sys.modules[__name__], file.stem, attribute)
        DISPLAYS[attribute.HARDWARE] = attribute

  # Return polymorph sensor....
  def __new__(self, id, hardware_type, address, title = None):
    if hardware_type not in terrariumDisplay.DISPLAYS:
      raise terrariumDisplayException('Display type {} is unknown.'.format(hardware_type))

    return terrariumDisplay.DISPLAYS[hardware_type](id, address, title)

  # Return a list with type and names of supported switches
  @staticmethod
  def get_available_types():
    data = []
    all_types = []
    for (hardware_type,display) in terrariumDisplay.DISPLAYS.items():
      if display.NAME is not None:
        data.append({'hardware' : hardware_type, 'name' : display.NAME})

    return data