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
import thread

from terrariumUtils import terrariumUtils,terrariumSingleton

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

class terrariumLCD():
  __metaclass__ = terrariumSingleton

  def __init__(self,address,resolution = '16x2',title = False):
    self.__address = None
    self.__lcd = None
    self.__title = False

    self.set_address(address)
    self.set_resolution(resolution)
    self.set_title(title)

    self.__text_animation = False
    self.__rotation_timeout = 10
    self.__messages = ['Starting terrariumPI...']
    thread.start_new_thread(self.__rotate_messages, ())

  def __rotate_messages(self):
    max_lines = int(self.__resolution[1])

    while True:
      starttime = time.time()
      messages = [message for message in self.__messages]
      messages.insert(0,datetime.datetime.now().strftime('%c'))

      for messagenr in xrange(0,len(messages)):
        if messagenr >= max_lines:
          timeout = float(self.__rotation_timeout) - (time.time() - starttime)
          if timeout >= 0.0:
            sleep(timeout)
          starttime = time.time()

          for linenr in xrange(max_lines - (1 + (1 if self.__title else 0)),0,-1):
            self.__animate_text(messages[messagenr - linenr], max_lines - linenr)

          self.__animate_text(messages[messagenr],max_lines)

        else:
          self.__animate_text(messages[messagenr],(messagenr % max_lines) + 1)
          starttime = time.time()

      timeout = float(self.__rotation_timeout) - (time.time() - starttime)
      if timeout >= 0.0:
        sleep(timeout)
      starttime = time.time()

  def __animate_text(self,message,linenr):
    max_chars = int(self.__resolution[0])
    if self.__lcd is None:
      return

    self.__lcd.lcd_display_string(message[:max_chars].ljust(max_chars),linenr)

    if len(message) > max_chars and not self.__text_animation:
      self.__text_animation = True
      sleep(0.2)
      for counter in xrange(1,len(message)-max_chars):
        self.__lcd.lcd_display_string(message[counter:max_chars+counter],linenr)
        sleep(0.2)

      for counter in xrange(len(message)-max_chars,0,-1):
        self.__lcd.lcd_display_string(message[counter:max_chars+counter],linenr)
        sleep(0.2)

      self.__lcd.lcd_display_string(message[:max_chars].ljust(max_chars),linenr)
      self.__text_animation = False

  def set_address(self,address):
    self.__address = None
    if address is not None and '' != address:
      self.__address = address
      address = address.split(',')
      bus = 1 if len(address) == 1 else int(address[1])
      address = int('0x' + str(address[0]),16)
      self.__lcd = lcd(address,bus)

  def get_address(self):
    return self.__address

  def set_resolution(self,resolution):
    self.__resolution = None
    if resolution is not None and '' != resolution:
      self.__resolution = resolution.split('x')
      self.__resolution[0] = self.__resolution[0]
      self.__resolution[1] = self.__resolution[1]

  def get_resolution(self):
    if self.__resolution is not None:
      return 'x'.join(self.__resolution)

    return ''

  def set_title(self,value):
    self.__title = terrariumUtils.is_true(value)

  def get_title(self):
    return self.__title == True

  def message(self,message):
    if isinstance(message,basestring):
      self.__messages = [message]
      self.__lcd.lcd_display_string(message)
    else:
      self.__messages = [msg for msg in message]

  def get_config(self):
    data = {'address'    : self.get_address(),
            'resolution' : self.get_resolution(),
            'title'      : self.get_title()}

    return data
