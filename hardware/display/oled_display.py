from . import terrariumDisplay
from terrariumUtils import terrariumUtils

from pathlib import Path

# pip install luma.oled
from luma.core.interface.serial import i2c
from luma.core.render import canvas
#from luma.core.error import DeviceNotFoundError
from luma.oled.device import ssd1306, ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1351, sh1106

from PIL import Image, ImageFont
from time import sleep

class terrariumOLEDMixin():

  def _load_hardware(self, oled):
    address = self._address
    self._device['device']    = oled(i2c(port=1 if len(address) == 1 else int(address[1]), address=address[0]))
    self._device['fontsize']  = 10
    self._device['font']      = ImageFont.truetype('fonts/DejaVuSans.ttf', self.fontsize)
    self._device['fontwidth'] = self._device['font'].getsize('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')[0] / (2 * 26)

    # Update the resolutions based on device
    self.width  = self._device['device'].width
    self.height = self._device['device'].height


    self._device['lines_buffer'] = []

    #print(f'Cleared: {self._device["clear"]}')
    #self.clear()

  def unload_hardware(self):
    self._device['device'].lcd_device.bus.close()
    del(self._device['device'])

  def _write_line(self, text, line_nr):
    print(f'OLED: nr {line_nr}, {text}')
    xpos = 1
#    self.__text_lines[line_nr-1] = text
    with canvas(self._device['device']) as draw:
      #if len(self._device['lines_buffer']) == 0:
      draw.rectangle(self._device['device'].bounding_box, outline='white', fill='black')

      if self.title is not None:
        draw.rectangle((0,0,self.width,self.fontsize), fill='white')
        draw.text((1,0), self.title, font=self.font, fill='black')

      self._device['lines_buffer'].append(text)
      #for x in range(line_nr):


      for nr, line in enumerate(self._device['lines_buffer']):
        if line is None:
          continue

        ypos = (nr + 0) * self.fontsize
        draw.text((xpos, ypos), line, font=self.font, fill='white')

  def write_image(self, image):
    if Path(image).exists():
      image = Image.open(image)
      scale = max(float(self.width) / float(image.size[0]),float(self.height) / float(image.size[1]))
      image = image.resize((int(scale * float(image.size[0])),int(scale * float(image.size[1]))),Image.ANTIALIAS)

      top_x = int((image.size[0] - int(self.width)) / 2)
      top_y = int((image.size[1] - int(self.height)) / 2)
      image = image.crop((top_x,top_y,top_x + int(self.width),top_y + int(self.height)))

      self._device['device'].display(image.convert(self._device['device'].mode))
      sleep(1)
    else:
      print('Image {} does not exists'.format(image))

  def clear(self):
    self._device['device'].clear()
    with canvas(self._device['device']) as draw:
      draw.rectangle(self._device['device'].bounding_box, outline='white', fill='black')

    self._device['clear'] = True
    self._device['lines_buffer'] = []
    print(f'Oled clear: True')

    #self.__text_lines = [None] * int(self.height / self.fontsize)
    super().clear()

class terrariumOLEDSSD1306(terrariumDisplay, terrariumOLEDMixin):
  HARDWARE = 'SSD1306'
  NAME = 'OLED SSD1306 (I2C)'

  def load_hardware(self):
    print(f'Load hardware {ssd1306}')
    self._load_hardware(ssd1306)

class terrariumOLEDSSD1309(terrariumDisplay, terrariumOLEDMixin):
  HARDWARE = 'SSD1309'
  NAME = 'OLED SSD1309 (I2C)'

  def load_hardware(self):
    self._load_hardware(ssd1309)

class terrariumOLEDSSD1322(terrariumDisplay, terrariumOLEDMixin):
  HARDWARE = 'SSD1322'
  NAME = 'OLED SSD1322 (I2C)'

  def load_hardware(self):
    self._load_hardware(ssd1322)

class terrariumOLEDSSD1325(terrariumDisplay, terrariumOLEDMixin):
  HARDWARE = 'SSD1325'
  NAME = 'OLED SSD1325 (I2C)'

  def load_hardware(self):
    self._load_hardware(ssd1325)

class terrariumOLEDSSD1327(terrariumDisplay, terrariumOLEDMixin):
  HARDWARE = 'SSD1327'
  NAME = 'OLED SSD1327 (I2C)'

  def load_hardware(self):
    self._load_hardware(ssd1327)

class terrariumOLEDSSD1331(terrariumDisplay, terrariumOLEDMixin):
  HARDWARE = 'SSD1331'
  NAME = 'OLED SSD1331 (I2C)'

  def load_hardware(self):
    self._load_hardware(ssd1331)

class terrariumOLEDSSD1351(terrariumDisplay, terrariumOLEDMixin):
  HARDWARE = 'SSD1351'
  NAME = 'OLED SSD1351 (I2C)'

  def load_hardware(self):
    self._load_hardware(ssd1351)

class terrariumOLEDSH1106(terrariumDisplay, terrariumOLEDMixin):
  HARDWARE = 'SH1106'
  NAME = 'OLED SH1106 (I2C)'

  def load_hardware(self):
    self._load_hardware(sh1106)