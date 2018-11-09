# -*- coding: utf-8 -*-
# Source: https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

# -*- coding: utf-8 -*-
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
try:
  import thread as _thread
except ImportError as ex:
  import _thread
import serial

import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

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

  __MAX_SHOW_LINE_TIMEOUT = 7
  __MAX_SHOW_CHAR_TIMEOUT = 0.01

  def __init__(self,id,address,name,resolution = '16x2',title = False):
    self.id = id
    self.font_size = 1
    self.animating = False

    self.set_name(name)
    self.set_resolution(resolution)
    self.set_title(title)
    self.set_address(address)

    self.loading()

  def loading(self):
    self.message('Starting TerrariumPI')

  def clear(self):
    pass

  def write_image(self,imagefile):
    pass

  def get_max_chars(self):
    return int(float(self.resolution[0]) / float(self.font_size))

  def get_max_lines(self):
    return int(float(self.resolution[1]) / float(self.font_size))

  def get_id(self):
    return self.id

  def set_address(self,address):
    self.address = None
    self.bus = None
    if address is not None and '' != address:
      address = address.split(',')
      self.address = address[0]
      self.bus = 1 if len(address) == 1 else address[1]

  def get_address(self):
    data = str(self.address)
    if self.bus is not None:
      data = data + ',' + str(self.bus)
    return data

  def set_name(self,value):
    self.name = None
    if value is not None and '' != value:
      self.name = value

  def get_name(self):
    return self.name

  def set_resolution(self,resolution):
    self.resolution = None
    if resolution is not None and '' != resolution:
      self.resolution = resolution.split('x')

  def get_resolution(self):
    if self.resolution is not None:
      return 'x'.join(self.resolution)

    return ''

  def set_title(self,value):
    self.title = terrariumUtils.is_true(value)

  def get_title(self):
    return self.title == True

  def get_config(self):
    data = {'id'         : self.get_id(),
            'address'    : self.get_address(),
            'name'       : self.get_name(),
            'resolution' : self.get_resolution(),
            'title'      : self.get_title()}

    return data

  def message(self,messages):
    if self.animating:
      return

    if isinstance(messages,str):
      if len(messages) > 2 * self.get_max_chars():
        # Split long messages on a 'dot', creating multiple lines
        messages = messages.split('. ')
        if len(messages) == 1:
          # When it is one long sentence, split it in have on a space
          splitpos = messages[0].find(' ',len(messages[0])/2)
          messages = [messages[0][:splitpos].strip(),messages[0][splitpos:].strip()]

      else:
        messages = [messages.strip()]

    # Set 'now' timestamp
    self.messages = [datetime.datetime.now().strftime('%c')]
    # Add messages to queue
    for message in messages:
      # If there are new lines in a message, split it up to multiple lines
      message = message.split("\n")
      for submessage in message:
        if '' != submessage.strip():
          self.messages.append(submessage.strip())

    _thread.start_new_thread(self.display_messages, ())

  def display_messages(self):
    if self.animating:
      return

    self.animating = True

    max_chars = self.get_max_chars()
    max_lines = self.get_max_lines()

    line_counter = 0
    animate_lines = []

    starttime = time.time()
    empty_lines = []
    if max_lines > 0 and len(self.messages) > 0:
      empty_lines = [''] * int((max_lines - (len(self.messages) % max_lines)) - (0 if not self.get_title() else len(self.messages) / max_lines))

    for message in self.messages + empty_lines:
      self.write_line((line_counter % max_lines)+1,message)
      if len(message) > max_chars:
        animate_lines.append({'linenr' : (line_counter % max_lines)+1,'message' : message})

      line_counter += 1

      if line_counter > 0 and line_counter % max_lines == 0:
        if len(animate_lines) > 0:
          self.animate_lines(animate_lines)

        timeout = float(terrariumScreen.__MAX_SHOW_LINE_TIMEOUT) - (time.time() - starttime)
        if timeout >= 0.0:
          sleep(timeout)

        if self.get_title():
          line_counter += 1

        animate_lines = []
        starttime = time.time()

    if len(animate_lines) > 0:
      self.animate_lines(animate_lines)

    self.animating = False

  def animate_lines(self,lines):
    max_chars = self.get_max_chars()

    for line in lines:
      for counter in range(1,len(line['message'])-max_chars):
        self.write_line(line['linenr'],line['message'][counter:max_chars+counter])
        sleep(terrariumScreen.__MAX_SHOW_CHAR_TIMEOUT)

      for counter in range(len(line['message'])-max_chars,0,-1):
        self.write_line(line['linenr'],line['message'][counter:max_chars+counter])
        sleep(terrariumScreen.__MAX_SHOW_CHAR_TIMEOUT)

      self.write_line(line['linenr'],line['message'][:max_chars])

class terrariumLCD(terrariumScreen):
  def set_address(self,address):
    super(terrariumLCD,self).set_address(address)
    self.__screen = lcd(int('0x' + str(self.address),16),int(self.bus))

  def write_line(self,linenr,text):
    text = text[:int(self.resolution[0])].ljust(int(self.resolution[0]))
    self.__screen.lcd_display_string(text,linenr)

class terrariumLCDSerial(terrariumScreen):
  def set_address(self,address):
    super(terrariumLCDSerial,self).set_address(address)
    if self.bus == 1:
      self.bus = 9600
    self.__screen = serial.Serial(self.address, int(self.bus))

  def clear(self):
    self.__screen.write(str.encode('00clr'))
    sleep(1)

  def write_line(self,linenr,text):
    text = text[:int(self.resolution[0])].ljust(int(self.resolution[0]))
    data = str.encode('0' + str(linenr-1) + str(text))
    self.__screen.write(data)
    # Always sleep 1 sec due to slow serial: https://www.instructables.com/id/Raspberry-Pi-Arduino-LCD-Screen/
    sleep(1)

class terrariumOLED(terrariumScreen):
  def set_address(self,address):
    super(terrariumOLED,self).set_address(address)
    self.__screen = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=int('0x' + str(self.address),16), i2c_bus=int(self.bus))
    self.init()

  def loading(self):
    self.write_image('static/images/profile_image.jpg')

  def get_max_chars(self):
    return int(float(self.resolution[0]) / (self.font_size/2.0))

  def init(self):
    self.font_size = 10
    self.__screen.begin()
    self.__screen.clear()
    self.__screen.display()

    self.__canvas = Image.new('1', (int(self.resolution[0]), int(self.resolution[1])))
    draw = ImageDraw.Draw(self.__canvas)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,int(self.resolution[0])-1,int(self.resolution[1])-1), outline=1, fill=0)
    self.__screen.image(self.__canvas)
    # Load font
    self.__font = ImageFont.truetype('fonts/DejaVuSans.ttf', self.font_size)

  def write_line(self,linenr,text):
    draw = ImageDraw.Draw(self.__canvas)
    # Clean line
    draw.rectangle((1,((linenr-1) * self.font_size)+1,int(self.resolution[0])-2, (((linenr-1) * self.font_size) + self.font_size) ), outline=0, fill=0)
    # Write new line
    if text != '':
      draw.text((1, (linenr-1) * self.font_size), text, font=self.__font, fill=255)

    self.__screen.image(self.__canvas)
    self.__screen.display()

  def write_image(self,imagefile):
    image = Image.open(imagefile)

    scale = max(float(self.resolution[0]) / float(image.size[0]),float(self.resolution[1]) / float(image.size[1]))
    image = image.resize((int(scale * float(image.size[0])),int(scale * float(image.size[1]))),Image.ANTIALIAS)

    top_x = int((image.size[0] - int(self.resolution[0])) / 2)
    top_y = int((image.size[1] - int(self.resolution[1])) / 2)
    image = image.crop((top_x,top_y,top_x + int(self.resolution[0]),top_y + int(self.resolution[1])))

    image = image.convert('1')
    self.__screen.image(image)
    self.__screen.display()

# Factory class
class terrariumDisplay(object):

  def __new__(self,id,address,name,resolution = '16x2',title = False):
    if resolution in ['16x2','20x4']:
      if address.startswith('/dev/'):
        return terrariumLCDSerial(id,address,name,resolution,title)
      else:
        return terrariumLCD(id,address,name,resolution,title)
    elif resolution in ['128x64']:
      return terrariumOLED(id,address,name,resolution,title)

    raise Exception()
