# -*- coding: utf-8 -*-
# Source: https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

"""
Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
Made available under GNU GENERAL PUBLIC LICENSE

# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources
# By DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1

"""
import smbus
import time
import datetime
import math
import textwrap
try:
  import thread as _thread
except ImportError as ex:
  import _thread
import serial

from gevent import sleep
from hashlib import md5
from PIL import Image, ImageFont
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.core.error import DeviceNotFoundError
from luma.oled.device import ssd1306, ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1351, sh1106

from terrariumUtils import terrariumUtils

class i2c_device:
  def __init__(self, addr, port=1):
    self.addr = addr
    self.bus = smbus.SMBus(port)

# Write a single command
  def write_cmd(self, cmd):
    self.bus.write_byte(self.addr, cmd)
    sleep(0.0001)

# Write a command and argument
  def write_cmd_arg(self, cmd, data):
    self.bus.write_byte_data(self.addr, cmd, data)
    sleep(0.0001)

# Write a block of data
  def write_block_data(self, cmd, data):
    self.bus.write_block_data(self.addr, cmd, data)
    sleep(0.0001)

# Read a single byte
  def read(self):
    return self.bus.read_byte(self.addr)

# Read
  def read_data(self, cmd):
    return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
  def read_block_data(self, cmd):
    return self.bus.read_block_data(self.addr, cmd)

class lcd:
  # commands
  LCD_CLEARDISPLAY = 0x01
  LCD_RETURNHOME = 0x02
  LCD_ENTRYMODESET = 0x04
  LCD_DISPLAYCONTROL = 0x08
  LCD_CURSORSHIFT = 0x10
  LCD_FUNCTIONSET = 0x20
  LCD_SETCGRAMADDR = 0x40
  LCD_SETDDRAMADDR = 0x80

  # flags for display entry mode
  LCD_ENTRYRIGHT = 0x00
  LCD_ENTRYLEFT = 0x02
  LCD_ENTRYSHIFTINCREMENT = 0x01
  LCD_ENTRYSHIFTDECREMENT = 0x00

  # flags for display on/off control
  LCD_DISPLAYON = 0x04
  LCD_DISPLAYOFF = 0x00
  LCD_CURSORON = 0x02
  LCD_CURSOROFF = 0x00
  LCD_BLINKON = 0x01
  LCD_BLINKOFF = 0x00

  # flags for display/cursor shift
  LCD_DISPLAYMOVE = 0x08
  LCD_CURSORMOVE = 0x00
  LCD_MOVERIGHT = 0x04
  LCD_MOVELEFT = 0x00

  # flags for function set
  LCD_8BITMODE = 0x10
  LCD_4BITMODE = 0x00
  LCD_2LINE = 0x08
  LCD_1LINE = 0x00
  LCD_5x10DOTS = 0x04
  LCD_5x8DOTS = 0x00

  # flags for backlight control
  LCD_BACKLIGHT = 0x08
  LCD_NOBACKLIGHT = 0x00

  En = 0b00000100 # Enable bit
  Rw = 0b00000010 # Read/Write bit
  Rs = 0b00000001 # Register select bit

  #initializes objects and lcd
  def __init__(self,address,device=1):
    self.lcd_device = i2c_device(address,device)

    self.lcd_write(0x03)
    self.lcd_write(0x03)
    self.lcd_write(0x03)
    self.lcd_write(0x02)

    self.lcd_write(lcd.LCD_FUNCTIONSET | lcd.LCD_2LINE | lcd.LCD_5x8DOTS | lcd.LCD_4BITMODE)
    self.lcd_write(lcd.LCD_DISPLAYCONTROL | lcd.LCD_DISPLAYON)
    self.lcd_write(lcd.LCD_CLEARDISPLAY)
    self.lcd_write(lcd.LCD_ENTRYMODESET | lcd.LCD_ENTRYLEFT)
    sleep(0.2)

  # clocks EN to latch command
  def lcd_strobe(self, data):
    self.lcd_device.write_cmd(data | lcd.En | lcd.LCD_BACKLIGHT)
    sleep(.0005)
    self.lcd_device.write_cmd(((data & ~lcd.En) | lcd.LCD_BACKLIGHT))
    sleep(.0001)

  def lcd_write_four_bits(self, data):
    self.lcd_device.write_cmd(data | lcd.LCD_BACKLIGHT)
    self.lcd_strobe(data)

  # write a command to lcd
  def lcd_write(self, cmd, mode=0):
    self.lcd_write_four_bits(mode | (cmd & 0xF0))
    self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

  # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
  # works!
  def lcd_write_char(self, charvalue, mode=1):
    self.lcd_write_four_bits(mode | (charvalue & 0xF0))
    self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

  # put string function with optional char positioning
  def lcd_display_string(self, string, line=1, pos=0):
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
    elif line == 3:
      pos_new = 0x14 + pos
    elif line == 4:
      pos_new = 0x54 + pos

    self.lcd_write(0x80 + pos_new)

    for char in string:
      self.lcd_write(ord(char), lcd.Rs)

  # clear lcd and set to home
  def lcd_clear(self):
    self.lcd_write(lcd.LCD_CLEARDISPLAY)
    self.lcd_write(lcd.LCD_RETURNHOME)

  # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
  def backlight(self, state): # for state, 1 = on, 0 = off
    if state == 1:
      self.lcd_device.write_cmd(lcd.LCD_BACKLIGHT)
    elif state == 0:
      self.lcd_device.write_cmd(lcd.LCD_NOBACKLIGHT)

  # add custom characters (0 - 7)
  def lcd_load_custom_chars(self, fontdata):
    self.lcd_write(0x40);
    for char in fontdata:
      for line in char:
        self.lcd_write_char(line)

class terrariumScreen(object):
  TYPE = None

  def __init__(self, display_id, address, name, title = False):
    self.display_id = display_id
    self.resolution = [0,0]
    self.font_size = 1
    self.animating = False

    self.set_name(name)
    self.set_title(title)
    self.set_address(address)

    self.loading()

  def get_type(self):
    return self.TYPE

  def get_id(self):
    if self.display_id in [None,'None','']:
      self.display_id = md5((self.get_type() + self.get_address()).encode('utf-8')).hexdigest()

    return self.display_id

  def set_name(self,value):
    self.name = None
    if value is not None and '' != value:
      self.name = value

  def get_name(self):
    return self.name

  def set_address(self,address):
    self.address = None
    self.bus = None
    if address is not None and '' != address:
      address = address.split(',')
      self.address = address[0]
      self.bus = 1 if len(address) == 1 else address[1]

  def get_address(self):
    data = self.address
    if self.bus is not None:
      data = data + ',' + str(self.bus)
    return data

  def set_title(self,value):
    self.title = terrariumUtils.is_true(value)

  def get_title(self):
    return terrariumUtils.is_true(self.title)

  def get_config(self):
    data = {'id'          : self.get_id(),
            'address'     : self.get_address(),
            'name'        : self.get_name(),
            'title'       : self.get_title(),
            'hardwaretype': self.get_type(),
            'supported'   : terrariumDisplay.valid_hardware_types()}

    return data

  def loading(self):
    self.message('Starting TerrariumPI')

  def clear(self):
    pass

  def write_image(self,imagefile):
    pass

  def get_max_chars(self):
    return int(math.floor(float(self.resolution[0]) / float(self.font_size)))

  def get_max_lines(self):
    return int(math.floor(float(self.resolution[1]) / float(self.font_size)))

  def get_resolution(self):
    return 'x'.join(self.resolution)

  def format_message(self,text):
    lines = []
    try:
      text = text.decode('utf-8')
    except Exception as ex:
      pass

    for line in text.split("\n"):
      if '' == line.strip():
        continue

      for wrapline in textwrap.wrap(line.strip(),self.get_max_chars()):
        if '' == wrapline.strip():
          continue

        lines.append(wrapline.strip())

    return lines

  def message(self,text):
    if self.get_max_chars() == 0:
      return

    text_lines = []
    if self.get_title():
      # Set 'now' timestamp as title
      text_lines = [datetime.datetime.now().strftime('%c')]

    text_lines += self.format_message(text)
    _thread.start_new_thread(self.display_message, (text_lines,))

class terrariumLCD(terrariumScreen):

  def set_address(self,address):
    super(terrariumLCD,self).set_address(address)
    try:
      self.device = lcd(int('0x' + str(self.address),16),int(self.bus))
    except OSError as ex:
      print('%s - WARNING - terrariumDisplay     - %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],ex))
      self.device = None
    except IOError as ex:
      print('%s - WARNING - terrariumDisplay     - %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],ex))
      self.device = None

  def display_message(self,text_lines):
    if self.device is None or self.animating:
      return

    self.animating = True

    if self.get_title():
      title = text_lines.pop(0).ljust(self.resolution[0])

    if len(text_lines) < self.get_max_lines():
      text_lines += [''] * (self.get_max_lines() - (1 if self.get_title() else 0) - len(text_lines))

    while len(text_lines) >= self.get_max_lines()- (1 if self.get_title() else 0):
      if self.get_title():
        self.device.lcd_display_string(title,1)

      linenr = 0
      while linenr < len(text_lines) and linenr < self.get_max_lines()- (1 if self.get_title() else 0):
        self.device.lcd_display_string(text_lines[linenr].ljust(self.resolution[0]),linenr + (2 if self.get_title() else 1))
        linenr += 1

      text_lines.pop(0)
      sleep(0.5)

    self.animating = False

class terrariumLCD16x2(terrariumLCD):
  TYPE = 'LCD16x2'

  def set_address(self,address):
    super(terrariumLCD16x2,self).set_address(address)
    self.resolution = [16,2]

class terrariumLCD20x4(terrariumLCD):
  TYPE = 'LCD20x4'

  def set_address(self,address):
    super(terrariumLCD20x4,self).set_address(address)
    self.resolution = [20,4]

class terrariumLCDSerial(terrariumScreen):

  def set_address(self,address):
    super(terrariumLCDSerial,self).set_address(address)
    if self.bus == 1:
      self.bus = 9600

    try:
      self.device = serial.Serial(self.address, int(self.bus))
    except serial.serialutil.SerialException as ex:
      print('%s - WARNING - terrariumDisplay     - %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],ex))
      self.device = None

  #def clear(self):
  #  if self.device is None:
  #    return

  #  self.device.write(str.encode('00clr'))
  #  sleep(1)

  def display_message(self,text_lines):
    if self.device is None or self.animating:
      return

    self.animating = True

    if self.get_title():
      title = text_lines.pop(0).ljust(self.resolution[0])

    if len(text_lines) < self.get_max_lines():
      text_lines += [''] * (self.get_max_lines() - (1 if self.get_title() else 0) - len(text_lines))

    while len(text_lines) >= self.get_max_lines()- (1 if self.get_title() else 0):
      if self.get_title():
        self.device.write(str.encode('00' + str(title)))
        sleep(1)

      linenr = 0
      while linenr < len(text_lines) and linenr < self.get_max_lines()- (1 if self.get_title() else 0):
        self.device.write(str.encode('0' + str(linenr + (1 if self.get_title() else 0)) + str(text_lines[linenr].ljust(self.resolution[0]))))
        sleep(1)
        linenr += 1

      text_lines.pop(0)

    self.animating = False

class terrariumLCDSerial16x2(terrariumLCDSerial):
  TYPE = 'LCDSerial16x2'

  def set_address(self,address):
    super(terrariumLCDSerial16x2,self).set_address(address)
    self.resolution = [16,2]

class terrariumLCDSerial20x4(terrariumLCDSerial):
  TYPE = 'LCDSerial20x4'

  def set_address(self,address):
    super(terrariumLCDSerial20x4,self).set_address(address)
    self.resolution = [20,4]

class terrariumOLED(terrariumScreen):
  def set_address(self,address):
    super(terrariumOLED,self).set_address(address)
    try:
      address = i2c(port=int(self.bus), address=int('0x' + str(self.address),16))

      if self.get_type() == terrariumOLEDSSD1306.TYPE:
        self.device = ssd1306(address)
      elif self.get_type() == terrariumOLEDSSD1309.TYPE:
        self.device = ssd1309(address)
      elif self.get_type() == terrariumOLEDSSD1322.TYPE:
        self.device = ssd1322(address)
      elif self.get_type() == terrariumOLEDSSD1325.TYPE:
        self.device = ssd1325(address)
      elif self.get_type() == terrariumOLEDSSD1327.TYPE:
        self.device = ssd1327(address)
      elif self.get_type() == terrariumOLEDSSD1331.TYPE:
        self.device = ssd1331(address)
      elif self.get_type() == terrariumOLEDSSD1351.TYPE:
        self.device = ssd1351(address)
      elif self.get_type() == terrariumOLEDSH1106.TYPE:
        self.device = sh1106(address)

    except DeviceNotFoundError as ex:
      print('%s - WARNING - terrariumDisplay     - %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],ex))
      self.device = None

    self.init()

  def loading(self):
    self.write_image('static/images/profile_image.jpg')

  def get_max_chars(self):
    return int(math.floor(float(self.resolution[0]) / (self.font_size/2.0)))

  def init(self):
    if self.device is None:
      return

    self.font_size = 10
    self.font = ImageFont.truetype('fonts/DejaVuSans.ttf', self.font_size)
    try:
      self.resolution = [self.device.width,self.device.height]
      self.device.clear()
      self.device.show()
    except Exception as ex:
      print('%s - WARNING - terrariumDisplay     - %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],ex))

  def display_message(self,text_lines):
    if self.device is None or self.animating:
      return

    self.animating = True

    if self.get_title():
      title = text_lines.pop(0)

    while len(text_lines) >= self.get_max_lines() - (1 if self.get_title() else 0):
      with canvas(self.device) as draw:
        draw.rectangle(self.device.bounding_box, outline='white', fill='black')

        if self.get_title():
          draw.rectangle((0,0,self.resolution[0],self.font_size), fill='white')
          draw.text((1,0), title, font=self.font, fill='black')
          #print(title)

        linenr = 0
        while linenr < len(text_lines) and linenr < self.get_max_lines()- (1 if self.get_title() else 0):
          draw.text((1, (linenr + (1 if self.get_title() else 0)) * self.font_size), text_lines[linenr], font=self.font, fill='white')
          #print(text_lines[linenr])
          linenr += 1

      #print('')
      text_lines.pop(0)
      sleep(0.75)

    self.animating = False

  def write_image(self,imagefile):
    if self.device is None:
      return

    image = Image.open(imagefile)
    scale = max(float(self.resolution[0]) / float(image.size[0]),float(self.resolution[1]) / float(image.size[1]))
    image = image.resize((int(scale * float(image.size[0])),int(scale * float(image.size[1]))),Image.ANTIALIAS)

    top_x = int((image.size[0] - int(self.resolution[0])) / 2)
    top_y = int((image.size[1] - int(self.resolution[1])) / 2)
    image = image.crop((top_x,top_y,top_x + int(self.resolution[0]),top_y + int(self.resolution[1])))

    self.device.display(image.convert(self.device.mode))

class terrariumOLEDSSD1306(terrariumOLED):
  TYPE = 'SSD1306'

class terrariumOLEDSSD1309(terrariumOLED):
  TYPE = 'SSD1309'

class terrariumOLEDSSD1322(terrariumOLED):
  TYPE = 'SSD1322'

class terrariumOLEDSSD1325(terrariumOLED):
  TYPE = 'SSD1325'

class terrariumOLEDSSD1327(terrariumOLED):
  TYPE = 'SSD1327'

class terrariumOLEDSSD1331(terrariumOLED):
  TYPE = 'SSD1331'

class terrariumOLEDSSD1351(terrariumOLED):
  TYPE = 'SSD1351'

class terrariumOLEDSH1106(terrariumOLED):
  TYPE = 'SH1106'

class terrariumDisplaySourceException(Exception):
  '''The entered display source is not known or invalid'''

# Factory class
class terrariumDisplay(object):
  DISPLAYS = [terrariumLCD16x2,
              terrariumLCD20x4,
              terrariumLCDSerial16x2,
              terrariumLCDSerial20x4,
              terrariumOLEDSSD1306,
              terrariumOLEDSSD1309,
              terrariumOLEDSSD1322,
              terrariumOLEDSSD1325,
              terrariumOLEDSSD1327,
              terrariumOLEDSSD1331,
              terrariumOLEDSSD1351,
              terrariumOLEDSH1106 ]

  def __new__(self, display_id, hardware_type, address, name = '', title = False):
    for display in terrariumDisplay.DISPLAYS:
      if hardware_type == display.TYPE:
        return display(display_id, address, name, title)

    raise terrariumDisplaySourceException('Display of type {} is unknown. We cannot controll this hardware.'.format(hardware_type))

  @staticmethod
  def valid_hardware_types():
    data = {}
    for display in terrariumDisplay.DISPLAYS:
      data[display.TYPE] = display.TYPE

    return data
