# -*- coding: utf-8 -*-
import re

from string import Template
from gevent import sleep
import datetime
from operator import itemgetter

from threading import Timer

from terrariumDatabase import NotificationMessage, NotificationService
from terrariumUtils import terrariumUtils, terrariumSingleton, classproperty

# Display support
#from terrariumDisplay import terrariumDisplay, terrariumDisplaySourceException

# Traffic light Support
import RPi.GPIO as GPIO

# Email support
import emails

# Twitter support
#import twitter

# Pushover support
#import pushover

# Telegram Bot
import paho.mqtt.client as mqtt
import json

#import requests
#from base64 import b64encode

import copy
from pony import orm

class terrariumNotification(terrariumSingleton):
  __MAX_MESSAGES_TOTAL_PER_MINUTE = 60

  __MESSAGES = {
    'authentication_error' : _('Authentication login error'),
    'system_warning'       : _('System warning'),
    'system_error'         : _('System error'),
  }

  @classproperty
  def available_messages(__cls__):
    data = []
    for (type, name) in terrariumNotification.__MESSAGES.items():
      data.append({'type' : type, 'name' : name})

    return sorted(data, key=itemgetter('name'))

  def __init__(self):

    self.__rate_limiter_counter = {
      'total' :
        {
          'rate'       : terrariumNotification.__MAX_MESSAGES_TOTAL_PER_MINUTE,
          'allowance'  : terrariumNotification.__MAX_MESSAGES_TOTAL_PER_MINUTE,
          'last_check' : datetime.datetime.now()
        }
    }

    self.services = {}

    self.engine = None

  def __rate_limit(self, title, rate = None):
    # https://en.wikipedia.org/wiki/Token_bucket / https://stackoverflow.com/a/668327
    # First the overall max rate limit

    if title not in self.__rate_limiter_counter:
      self.__rate_limiter_counter[title] = {'rate' : rate, 'allowance' : rate, 'last_check' : datetime.datetime.now()}

    current = datetime.datetime.now()
    time_passed = (current - self.__rate_limiter_counter[title]['last_check']).total_seconds()
    self.__rate_limiter_counter[title]['last_check'] = current

    self.__rate_limiter_counter[title]['allowance'] += time_passed * (self.__rate_limiter_counter[title]['rate'] / 60.0)

    if (self.__rate_limiter_counter[title]['allowance'] > self.__rate_limiter_counter[title]['rate']):
      self.__rate_limiter_counter[title]['allowance'] = self.__rate_limiter_counter[title]['rate'] # throttle

    if (self.__rate_limiter_counter[title]['allowance'] < 1.0):
      return True
    else:
      self.__rate_limiter_counter[title]['allowance'] -= 1.0
      return False

  def load_services(self):
    with orm.db_session():
      for service in NotificationService.select():
        if service.id not in self.services:
          setup = copy.deepcopy(service.setup)
          setup['version']       = self.version
          setup['profile_image'] = self.profile_image
          self.services[service.id] = terrariumNotificationService(service.id, service.type, service.name, service.enabled, setup)

  @property
  def version(self):
    return None if self.engine is None else self.engine.version

  @property
  def profile_image(self):
    return None if self.engine is None else self.engine.settings['profile_image']

  def message(self, message_id, data = None, files = []):
    if message_id not in self.__MESSAGES:
      return

    with orm.db_session():
      try:
        message = NotificationMessage[message_id]
      except orm.core.ObjectNotFound as ex:
        return

      # print('Notification message')
      # print(message)

      if not message.enabled:
        logger.debug(f'Notification message {message} is (temporary) disabled.')
        return

      if self.__rate_limit('total'):
        logger.warning(f'Hitting the total max rate limit of {self.__rate_limiter_counter["total"]["rate"]} messages per minute. Message will be ignored.')
        return

      # Translate message variables
      title = Template(message.title).safe_substitute(**data)
      text  = Template(message.message).safe_substitute(**data)

      if message.rate_limit > 0 and self.__rate_limit(title, message.rate_limit):
        logger.warning(f'Hitting the max rate limit of {self.__rate_limiter_counter[title]["rate"]} messages per minute for message {message.title}. Message will be ignored.')
        return

      for service in message.services:
        if not service.enabled:
          logger.info(f'Service {self} is (temporary) disabled.')
          continue

        if service.rate_limit > 0 and self.__rate_limit(service.type, service.rate_limit):
          logger.warning(f'Hitting the max rate limit of {self.__rate_limiter_counter[service.type]["rate"]} messages per minute for service {service.type}. Message will be ignored.')
          continue

        if service.id not in self.services:
          setup = copy.copy(service.setup)
          setup['version']       = self.version
          setup['profile_image'] = self.profile_image
          self.services[service.id] = terrariumNotificationService(service.id, service.type, service.name, service.enabled, setup)

        self.services[service.id].send_message(message_id, title, text)

  def stop(self):
    for serviceid in self.services:
      self.services[serviceid].stop()

class terrariumNotificationService(object):

  __TYPES = {

    'display' : {
      'name'  : _('Display'),
      'class' : lambda: terrariumNotificationServiceDisplay
    },

    'email' : {
      'name'  : _('Email'),
      'class' : lambda: terrariumNotificationServiceEmail
    },

#     'pushover' : {
#       'name'  : _('Pushover'),
#       'class' : lambda: terrariumNotificationServicePushover
#     },

#     'telegram' : {
#       'name'    : _('Telegram'),
# #      'class' : lambda: terrariumAreaHumidity
#     },

    'traffic' : {
      'name'    : _('Traffic light'),
      'class' : lambda: terrariumNotificationServiceTrafficLight
    },

#     'twitter' : {
#       'name'    : _('Twitter'),
# #      'class' : lambda: terrariumAreaWatertank
#     },

    'webhook' : {
      'name'    : _('Web-hook'),
      'class' : lambda: terrariumNotificationServiceWebhook
    },

    'mqtt' : {
      'name'    : _('MQTT '),
      'class' : lambda: terrariumNotificationServiceMQTT
    },
  }

  @classproperty
  def available_services(__cls__):
    data = []
    for (type, area) in terrariumNotificationService.__TYPES.items():
      data.append({'type' : type, 'name' : area['name']})

    return sorted(data, key=itemgetter('name'))

  # Return polymorph area....
  def __new__(cls, id, type, name = '', enabled = True, setup = None):
    if type not in [service['type'] for service in terrariumNotificationService.available_services]:
      raise terrariumAreaException(f'Service of type {type} is unknown.')

    return super(terrariumNotificationService, cls).__new__(terrariumNotificationService.__TYPES[type]['class']())

  def __init__(self, id, type, name, enabled, setup):
    if id is None:
      id = str(uuid.uuid4())

    self.id   = id
    self.type = type
    self.name = name
    self.enabled = enabled

    self.setup = {}
    self.load_setup(setup)

  def __repr__(self):
    return f'{terrariumNotificationService.__TYPES[self.type]["name"]} service {self.name}'

  def load_setup(self, setup_data):
    # print(f'Notification service: {self}')
    # print(setup_data)

    self.setup['version']       = setup_data.get('version')
    self.setup['profile_image'] = setup_data.get('profile_image')

  def stop(self):
    pass




######

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











class terrariumNotificationServiceDisplay(terrariumNotificationService):


  def load_setup(self, setup_data):


    # print('Load Oled Display data')
    # print(setup_data)


    self.setup = {
      'address'  : setup_data.get('address'),
      'port'     : int(setup_data.get('port',25)),
      'receiver' : setup_data.get('receiver','').split(','),
      'username' : setup_data.get('username'),
      'password' : setup_data.get('password'),
    }
    super().load_setup(setup_data)

  def send_message(self, type, subject, message, attachments = []):
    #print(f'Send {type} type message to display')
    # print(subject)
    # print(message)
    # print(attachments)

    pass


  def show_picture(self, picture):
    pass

class terrariumNotificationServiceEmail(terrariumNotificationService):
  def load_setup(self, setup_data):
    self.setup = {
      'address'  : setup_data.get('address'),
      'port'     : int(setup_data.get('port',25)),
      'receiver' : setup_data.get('receiver','').split(','),
      'username' : setup_data.get('username'),
      'password' : setup_data.get('password'),
    }
    super().load_setup(setup_data)

  def send_message(self, type, subject, message, attachments = []):
    if self.setup is None or len(self.setup.get('receiver',[])) == 0:
      # Configuration is not loaded, or no receivers, ignore sending emails
      return

    htmlbody = '<html><head><title>{}</title></head><body><img src="cid:{}" alt="Profile image" title="Profile image" align="right" style="max-width:300px;border-radius:25%;">{}</body></html>'

    for receiver in self.setup['receiver']:
      mail_tls_ssl = ['tls','ssl',None]
      while not len(mail_tls_ssl) == 0:
        email_message = emails.Message(
                        headers   = {'X-Mailer' : 'TerrariumPI version {}'.format(self.setup['version'])},
                        html      = htmlbody.format(subject,os.path.basename(self.setup['profile_image']),message.replace('\n','<br />')),
                        text      = message,
                        subject   = subject,
                        mail_from = ('TerrariumPI', re.sub(r'(.*)@(.*)', '\\1+terrariumpi@\\2', receiver, 0, re.MULTILINE)))

        with open(self.setup['profile_image'],'rb') as fp:
          profile_image = fp.read()
          email_message.attach(filename=os.path.basename(self.setup['profile_image']), content_disposition='inline', data=profile_image)

        for attachment in attachments:
          with open(attachment,'rb') as fp:
            attachment_data = fp.read()
            email_message.attach(filename=os.path.basename(attachment), data=attachment_data)

        smtp_settings = {'host': self.setup['address'],
                         'port': self.setup['port']}

        smtp_security = mail_tls_ssl.pop(0)
        if smtp_security is not None:
          smtp_settings[smtp_security] = True

        if '' != self.setup['username']:
          smtp_settings['user']     = terrariumUtils.decrypt(self.setup['username'])
          smtp_settings['password'] = terrariumUtils.decrypt(self.setup['password'])

        response = email_message.send(to=receiver, smtp=smtp_settings)

        if response.status_code == 250:
          # Mail sent, clear remaining connection types
          mail_tls_ssl = []


class terrariumNotificationServiceWebhook(terrariumNotificationService):
  def load_setup(self, setup_data):
    self.setup = {
      'address'  : setup_data.get('url'),
    }
    super().load_setup(setup_data)

  def send_message(self, type, subject, message, attachments = []):
    data = {}
    try:
      data = json.loads(message.replace('False','false').replace('True','true').replace('None','null').replace('\'','"'))
    except Exception as ex:
      print(ex)
      data['message'] = message

    data['subject'] = subject

    if len(attachments) > 0:
      message['files'] = []

      for attachment in attachments:
        with open(attachment,'rb') as fp:
          attachment_data = fp.read()
          message['files'].append({'name' : os.path.basename(attachment), 'data' : b64encode(attachment_data).decode('utf-8')})

    r = requests.post(self.setup['address'], json=data)
    if r.status_code != 200:
      print('Error sending webhook to url \'{}\' with status code: {}'.format(url,r.status_code))


class terrariumNotificationServiceTrafficLight(terrariumNotificationService):
  __YELLOW_TIMEOUT = 15 * 60
  __RED_TIMEOUT = 60 * 60

  def load_setup(self, setup_data):
    self.setup = {
      'red'    : None if setup_data.get('red')    is None else terrariumUtils.to_BCM_port_number(setup_data.get('red')),
      'yellow' : None if setup_data.get('yellow') is None else terrariumUtils.to_BCM_port_number(setup_data.get('yellow')),
      'green'  : None if setup_data.get('green')  is None else terrariumUtils.to_BCM_port_number(setup_data.get('green')),

      'red_timer'    : None,
      'yellow_timer' : None
    }

    for led in ['red','yellow','green']:
      if self.setup[led]:
        GPIO.setup(self.setup[led], GPIO.OUT)
        GPIO.output(self.setup[led],True)
        if led != 'green':
          sleep(1)
          GPIO.output(self.setup[led],False)

    super().load_setup(setup_data)

  def send_message(self, type, subject, message, attachments = []):
    led   = None
    if 'system_warning' == type:
      led     = 'yellow'
      timeout = self.__YELLOW_TIMEOUT

    elif 'system_error' == type:
      led     = 'yellow'
      timeout = self.__RED_TIMEOUT

    else:
      return

    if led is not None:
      GPIO.output(self.setup[led],True)
      if self.setup[f'{led}_timer'] is not None:
        try:
          self.setup[f'{led}_timer'].cancel()
        except Exception as ex:
          print(f'Traffic {led} exception')
          print(ex)

      self.setup[f'{led}_timer'] = Timer(timeout, lambda: GPIO.output(self.setup[f'{led}'],False))

  def stop(self):
    for led in ['red','yellow','green']:
      if self.setup[led]:
        GPIO.output(self.setup[led],False)
        GPIO.cleanup(self.setup[led])
        if self.setup.get(f'{led}_timer'):
          try:
            self.setup[f'{led}_timer'].cancel()
          except Exception as ex:
            print(f'Traffic STOP {led} exception')
            print(ex)


class terrariumNotificationServiceMQTT(terrariumNotificationService):
  def load_setup(self, setup_data):
    super().load_setup(setup_data)

    self.connection = None

    regex = re.compile(r"(?P<protocol>https?):\/\/(?P<host>[^\/:]+)(:(?P<port>\d+))?")
    data = setup_data.get('url')
    data = regex.search(data)
    if data is not None:
      self.setup = {
        'host'  : data.group('host'),
        'port'  : int(data.group('port')),
        'ssl'  : 'https' == data.group('protocol'),
      }

      self.connection = mqtt.Client(self.setup['host'], port=self.setup['port'])
      self.connection.loop_start()

  def stop(self):
    # TODO: Flush the queueu
    self.connection.disconnect()

  def send_message(self, type, subject, message, attachments = []):
    if self.connection is not None:
      self.connection.publish(subject, payload=json.loads(message), qos=1)



#### OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD ######

class terrariumNotificationMessage(object):

  def __init__(self,message_id, title, message, services = ''):
    self.id = message_id
    self.title = title.strip()
    self.message = message.strip()
    self.services = services.split(',') if '' != services else []
    self.enabled = len(self.services) > 0

  def get_id(self):
    return self.id

  def get_title(self):
    return self.title

  def get_message(self):
    return self.message

  def is_enabled(self):
    return self.message != '' and self.enabled == True

  def is_email_enabled(self):
    return self.message != '' and 'email' in self.services

  def is_twitter_enabled(self):
    return self.message != '' and 'twitter' in self.services

  def is_pushover_enabled(self):
    return self.message != '' and 'pushover' in self.services

  def is_telegram_enabled(self):
    return self.message != '' and 'telegram' in self.services

  def is_display_enabled(self):
    return self.message != '' and 'display' in self.services

  def is_webhook_enabled(self):
    return self.message != '' and 'webhook' in self.services

  def get_data(self):
    return {'id':self.get_id(),
            'title':self.get_title(),
            'message':self.get_message(),
            'enabled':self.is_enabled(),
            'services' : ','.join(self.services)
            }

class terrariumNotificationTelegramBot(object):
  __POLL_TIMEOUT = 120

  def __init__(self,bot_token,valid_users = None, proxy = None):
    self.__running = False
    self.__proxy = None

    self.__bot_token = bot_token
    self.__bot_url = 'https://api.telegram.org/bot{}/'.format(self.__bot_token)
    self.__chat_ids = []

    self.__last_update_check = int(time.time())

    self.set_valid_users(valid_users)
    self.set_proxy(proxy)
    self.start()

  def __get_updates(self,offset=None):
    self.__last_update_check = int(time.time())
    url = self.__bot_url + 'getUpdates?timeout={}'.format(terrariumNotificationTelegramBot.__POLL_TIMEOUT)
    if offset:
      url += '&offset={}'.format(offset)

    data = terrariumUtils.get_remote_data(url,terrariumNotificationTelegramBot.__POLL_TIMEOUT + 3,proxy=self.__proxy)
    if data is None:
      data = {'description' : 'Did not receive valid JSON data'}

    return data

  def __process_messages(self,messages):
    for update in messages:
      user = update['message']['from']['username']
      text = update['message']['text']
      chat = int(update['message']['chat']['id'])

      if user not in self.__valid_users:
        self.send_message('Sorry, you are not a valid user for this TerrariumPI.', chat)

      else:
        if chat not in self.__chat_ids:
          self.__chat_ids.append(chat)

        self.send_message(('Hi %s, you are now getting messages from TerrariumPI. I do not accept commands.' % (user,)), chat)

  def get_config(self):
    return {'bot_token' : self.__bot_token,
            'userid': ','.join(self.__valid_users) if self.__valid_users is not None else '',
            'proxy' : self.__proxy if self.__proxy is not None else ''}

  def send_message(self, type, text, chat_id = None):
    if self.__running:
      chat_ids = self.__chat_ids if chat_id is None else [int(chat_id)]
      for chat_id in chat_ids:
        url = self.__bot_url + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
        terrariumUtils.get_remote_data(url,proxy=self.__proxy)

  def send_image(self,text,files = [], chat_id = None):
    if self.__running:
      chat_ids = self.__chat_ids if chat_id is None else [int(chat_id)]
      for image in files:
        with open(image,'rb') as fp:
          photo = fp.read()
          post_file = {'photo': photo}

        for chat_id in chat_ids:
          url = self.__bot_url + 'sendPhoto?caption={}&chat_id={}'.format(text, chat_id)
          try:
            r = requests.post(url, files=post_file)
          except Exception as ex:
            print(ex)

  def set_valid_users(self,users = None):
    self.__valid_users = users.split(',') if users is not None else []

  def set_proxy(self,proxy):
    self.__proxy = None
    if proxy is not None and '' != proxy:
      self.__proxy = proxy

  def start(self):
    if not self.__running:
      _thread.start_new_thread(self.__run, ())

  def stop(self):
    self.__running = False
    print('%s - INFO    - terrariumNotificatio - Stopping TelegramBot. This can take up to %s seconds...' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],(terrariumNotificationTelegramBot.__POLL_TIMEOUT - (int(time.time()) - self.__last_update_check))))

  def __run(self):
    self.__running = True
    last_update_id = None

    error_counter = 0
    while self.__running and error_counter < 5:
      try:
        updates = self.__get_updates(last_update_id)
        if error_counter > 0:
          error_counter -= 1

        if 'result' in updates and len(updates['result']) > 0:
          last_update_id = max([int(update['update_id']) for update in updates['result']]) + 1
          self.__process_messages(updates['result'])

        elif 'description' in updates:
          error_counter += 1
          print('%s - ERROR  - terrariumNotificatio - TelegramBot has issues: %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],updates['description']))
          sleep(5)

        sleep(0.5)
      except Exception as ex:
        error_counter += 1
        print(ex)
        sleep(5)

    self.__running = False
    print('%s - INFO    - terrariumNotificatio - TelegramBot is stopped' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],))



# class terrariumNotification(terrariumSingleton):
#   __MAX_MESSAGES_TOTAL_PER_MINUTE = 12
#   __MAX_MESSAGES_PER_MINUTE = 6

#   __regex_parse = re.compile(r'%(?P<index>[^% ]+)%')

#   __default_notifications = {
#     'environment_light_alarm_low_on' : terrariumNotificationMessage('environment_light_alarm_low_on','Environment light day on','%raw_data%'),
#     'environment_light_alarm_low_off' : terrariumNotificationMessage('environment_light_alarm_low_off','Environment light day off','%raw_data%'),
#     'environment_light_alarm_high_on' : terrariumNotificationMessage('environment_light_alarm_high_on','Environment light night on','%raw_data%'),
#     'environment_light_alarm_high_off' : terrariumNotificationMessage('environment_light_alarm_high_off','Environment light night off','%raw_data%'),

#     'environment_temperature_alarm_low_on' : terrariumNotificationMessage('environment_temperature_alarm_low_on','Environment temperature alarm low on','%raw_data%'),
#     'environment_temperature_alarm_low_off' : terrariumNotificationMessage('environment_temperature_alarm_low_off','Environment temperature alarm low off','%raw_data%'),
#     'environment_temperature_alarm_high_on' : terrariumNotificationMessage('environment_temperature_alarm_high_on','Environment temperature alarm high on','%raw_data%'),
#     'environment_temperature_alarm_high_off' : terrariumNotificationMessage('environment_temperature_alarm_high_off','Environment temperature alarm high off','%raw_data%'),

#     'environment_humidity_alarm_low_on' : terrariumNotificationMessage('environment_humidity_alarm_low_on','Environment humidity alarm low on','%raw_data%'),
#     'environment_humidity_alarm_low_off' : terrariumNotificationMessage('environment_humidity_alarm_low_off','Environment humidity alarm low off','%raw_data%'),
#     'environment_humidity_alarm_high_on' : terrariumNotificationMessage('environment_humidity_alarm_high_on','Environment humidity alarm high on','%raw_data%'),
#     'environment_humidity_alarm_high_off' : terrariumNotificationMessage('environment_humidity_alarm_high_off','Environment humidity alarm high off','%raw_data%'),

#     'environment_moisture_alarm_low_on' : terrariumNotificationMessage('environment_moisture_alarm_low_on','Environment moisture alarm low on','%raw_data%'),
#     'environment_moisture_alarm_low_off' : terrariumNotificationMessage('environment_moisture_alarm_low_off','Environment moisture alarm low off','%raw_data%'),
#     'environment_moisture_alarm_high_on' : terrariumNotificationMessage('environment_moisture_alarm_high_on','Environment moisture alarm high on','%raw_data%'),
#     'environment_moisture_alarm_high_off' : terrariumNotificationMessage('environment_moisture_alarm_high_off','Environment moisture alarm high off','%raw_data%'),

#     'environment_conductivity_alarm_low_on' : terrariumNotificationMessage('environment_conductivity_alarm_low_on','Environment conductivity alarm low on','%raw_data%'),
#     'environment_conductivity_alarm_low_off' : terrariumNotificationMessage('environment_conductivity_alarm_low_off','Environment conductivity alarm low off','%raw_data%'),
#     'environment_conductivity_alarm_high_on' : terrariumNotificationMessage('environment_conductivity_alarm_high_on','Environment conductivity alarm high on','%raw_data%'),
#     'environment_conductivity_alarm_high_off' : terrariumNotificationMessage('environment_conductivity_alarm_high_off','Environment conductivity alarm high off','%raw_data%'),

#     'environment_ph_alarm_low_on' : terrariumNotificationMessage('environment_ph_alarm_low_on','Environment pH alarm low on','%raw_data%'),
#     'environment_ph_alarm_low_off' : terrariumNotificationMessage('environment_ph_alarm_low_off','Environment pH alarm low off','%raw_data%'),
#     'environment_ph_alarm_high_on' : terrariumNotificationMessage('environment_ph_alarm_high_on','Environment pH alarm high on','%raw_data%'),
#     'environment_ph_alarm_high_off' : terrariumNotificationMessage('environment_ph_alarm_high_off','Environment pH alarm high off','%raw_data%'),

#     'environment_watertank_alarm_low_on' : terrariumNotificationMessage('environment_watertank_alarm_low_on','Environment watertank alarm low on','%raw_data%'),
#     'environment_watertank_alarm_low_off' : terrariumNotificationMessage('environment_watertank_alarm_low_off','Environment watertank alarm low off','%raw_data%'),
#     'environment_watertank_alarm_high_on' : terrariumNotificationMessage('environment_watertank_alarm_high_on','Environment watertank alarm high on','%raw_data%'),
#     'environment_watertank_alarm_high_off' : terrariumNotificationMessage('environment_watertank_alarm_high_off','Environment watertank alarm high off','%raw_data%'),

#     'authentication_warning' : terrariumNotificationMessage('authentication_warning','Authentication warning message','%raw_data%'),

#     'system_warning' : terrariumNotificationMessage('system_warning','System warning message','%message%'),
#     'system_error' : terrariumNotificationMessage('system_error','System error message','%message%'),

#     'sensor_alarm_low' : terrariumNotificationMessage('sensor_alarm_low','Sensor %name% alarm low','%raw_data%'),
#     'sensor_alarm_high' : terrariumNotificationMessage('sensor_alarm_high','Sensor %name% alarm high','%raw_data%'),

#     'switch_toggle_on' : terrariumNotificationMessage('switch_toggle_on','Powerswitch %name% toggled on','%raw_data%'),
#     'switch_toggle_off' : terrariumNotificationMessage('switch_toggle_off','Powerswitch %name% toggled off','%raw_data%'),

#     'door_toggle_open' : terrariumNotificationMessage('door_toggle_open','Door %name% is open','%raw_data%'),
#     'door_toggle_closed' : terrariumNotificationMessage('door_toggle_closed','Door %name% is closed','%raw_data%'),


#     'webcam_motion' : terrariumNotificationMessage('webcam_motion','Movement at webcam %name%','%raw_data%'),
#   }

#   def __init__(self,trafficlights = [], profile_image = None, version = None):
#     self.__profile_image = None
#     self.__version = version
#     self.__ratelimit_messages = {}
#     self.__notification_leds = {'info'      : {'pin' : None, 'state' : False, 'lastaction' : 0},
#                                 'warning'   : {'pin' : None, 'state' : False, 'lastaction' : 0},
#                                 'error'     : {'pin' : None, 'state' : False, 'lastaction' : 0},
#                                 'exception' : {'pin' : None, 'state' : False, 'lastaction' : 0},
#                                 }

#     self.email = None
#     self.twitter = None
#     self.pushover = None
#     self.telegram = None
#     self.display = None
#     self.webhook = None

#     self.set_profile_image(profile_image)
#     if trafficlights is not None and len(trafficlights) == 3:
#       self.set_notification_leds(trafficlights[0],trafficlights[1],trafficlights[2])

#     self.__load_config()
#     self.__load_messages()

#   def __current_minute(self):
#     # Get timestamp of current minute with 00 seconds.
#     now = int(datetime.datetime.now().strftime('%s'))
#     now -= now % 60
#     return now

#   def __ratelimit(self):
#     now = str(self.__current_minute())
#     total = 0
#     for messageItem in sorted(self.__ratelimit_messages):
#       for timestamp in sorted(self.__ratelimit_messages[messageItem],reverse=True):
#         if timestamp == now:
#           total += self.__ratelimit_messages[messageItem][timestamp]
#         else:
#           del(self.__ratelimit_messages[messageItem][timestamp])

#     return total

#   def __load_config(self):
#     self.__data = configparser.ConfigParser()
#     self.__data.read('notifications.cfg')

#     if self.__data.has_section('email'):
#       self.set_email(self.__data.get('email','receiver'),
#                      self.__data.get('email','server'),
#                      self.__data.get('email','serverport'),
#                      self.__data.get('email','username'),
#                      self.__data.get('email','password'))

#     if self.__data.has_section('twitter'):
#       self.set_twitter(self.__data.get('twitter','consumer_key'),
#                      self.__data.get('twitter','consumer_secret'),
#                      self.__data.get('twitter','access_token'),
#                      self.__data.get('twitter','access_token_secret'))

#     if self.__data.has_section('pushover'):
#       self.set_pushover(self.__data.get('pushover','api_token'),
#                         self.__data.get('pushover','user_key'))

#     if self.__data.has_section('telegram'):
#       proxy = None
#       if self.__data.has_option('telegram', 'proxy'):
#         proxy = self.__data.get('telegram','proxy')

#       self.set_telegram(self.__data.get('telegram','bot_token'),
#                         self.__data.get('telegram','userid'),
#                         proxy)

#     if self.__data.has_section('display'):

#       try:
#         self.__data.get('display','hardwaretype')
#       except Exception as ex:
#         address = self.__data.get('display','address')
#         resolution = self.__data.get('display','resolution')
#         self.__data.remove_option('display','resolution')

#         if '/dev/' in address:
#           self.__data.set('display', 'hardwaretype', 'LCDSerial16x2')
#         elif '128x64' in resolution:
#           self.__data.set('display', 'hardwaretype', 'SSD1306')
#         else:
#           self.__data.set('display', 'hardwaretype', 'LCD16x2')

#       self.set_display(self.__data.get('display','address'),
#                        self.__data.get('display','hardwaretype'),
#                        self.__data.get('display','title'))

#     if self.__data.has_section('webhook'):
#       self.set_webhook(self.__data.get('webhook','address').replace('%%','%'))

#   def __load_messages(self,data = None):
#     self.messages = {}
#     for message_id in self.__default_notifications:
#       if self.__data.has_section('message' + message_id):
#         self.messages[message_id] = terrariumNotificationMessage(message_id,
#                                                                  self.__data.get('message' + message_id,'title').replace('%%','%'),
#                                                                  self.__data.get('message' + message_id,'message').replace('%%','%'),
#                                                                  self.__data.get('message' + message_id,'services').replace('%%','%'))
#       else:
#         self.messages[message_id] = self.__default_notifications[message_id]

#   def __parse_message(self,message,data):
#     if data is None:
#       return message

#     # Some dirty cleanup... :(
#     try:
#       del(data['timer_min']['time_table'])
#     except:
#       pass

#     try:
#       del(data['timer_max']['time_table'])
#     except:
#       pass

#     data = terrariumUtils.flatten_dict(data)
#     data['now'] = datetime.datetime.now().strftime('%c')

#     for dateitem in ['timer_min_lastaction','timer_max_lastaction','last_update']:
#       if dateitem in data:
#         data[dateitem] = datetime.datetime.fromtimestamp(int(data[dateitem])).strftime('%c')

#     for item in terrariumNotification.__regex_parse.findall(message):
#       if 'raw_data' == item:
#         message = message.replace('%' + item + '%',str(data)
#                                                     .replace(', ',"\n")
#                                                     .replace('\': ','\':')
#                                                     .replace('{','')
#                                                     .replace('}',''))
#       elif item in data:
#         message = message.replace('%' + item + '%',str(data[item]))

#     return message.encode('utf8')

#   def __update_config(self,section,data,exclude = []):
#     if not self.__data.has_section(section):
#       self.__data.add_section(section)

#     keys = list(data.keys())
#     keys.sort()
#     for setting in keys:
#       if setting in exclude:
#         continue

#       if type(data[setting]) is list:
#         data[setting] = ','.join(data[setting])

#       if isinstance(data[setting], str):
#         try:
#           data[setting] = data[setting].encode('utf-8').decode()
#         except Exception as ex:
#           # 'Not sure what to do... but it seams already utf-8...??'
#           pass

#       self.__data.set(section, str(setting), str(data[setting].replace('%','%%')))

#   def stop(self):
#     if self.telegram is not None:
#       self.telegram.stop()

#     for messagetype in self.__notification_leds:
#       if self.__notification_leds[messagetype]['pin'] is not None:
#         GPIO.cleanup(self.__notification_leds[messagetype]['pin'])
#         self.__notification_leds[messagetype]['pin'] = None

#   def set_profile_image(self,imagefile):
#     self.__profile_image = imagefile
#     if self.__profile_image is None:
#       return

#     if imagefile[0] == '/':
#       imagefile = imagefile[1:]

#     if os.path.isfile(imagefile):
#       self.__profile_image = imagefile
#       self.update_twitter_profile_image()

#   def set_notification_leds(self,green,orange,red):
#     self.__notification_leds['info']['pin'] = None if green is None else terrariumUtils.to_BCM_port_number(green)
#     self.__notification_leds['warning']['pin'] = None if orange is None else terrariumUtils.to_BCM_port_number(orange)
#     self.__notification_leds['error']['pin'] = None if red is None else terrariumUtils.to_BCM_port_number(red)

#     # Initialize leds and run them all for 1 second to test
#     GPIO.setmode(GPIO.BCM)
#     for messagetype in ['info','warning','error']:
#       lednr = self.__notification_leds[messagetype]['pin']
#       if lednr is not None:
#         GPIO.setup(lednr, GPIO.OUT)
#         GPIO.output(lednr,1)
#         sleep(1)
#         GPIO.output(lednr,0)

#   def send_notication_led(self,message_id):
#     message_type = message_id.replace('system_','')
#     now = int(time.time())
#     if message_type in ['info','error','warning']:
#       if self.__notification_leds[message_type]['pin'] is not None:
#         GPIO.output(self.__notification_leds[message_type]['pin'],1)
#         self.__notification_leds[message_type]['state'] = True
#         self.__notification_leds[message_type]['lastaction'] = now

#     for message_type in self.__notification_leds:
#       if self.__notification_leds[message_type]['state'] and \
#           ( ('warning' == message_type and now - self.__notification_leds[message_type]['lastaction'] > 10 * 60) or \
#             ('error'   == message_type and now - self.__notification_leds[message_type]['lastaction'] > 30 * 60) ):

#         GPIO.output(self.__notification_leds[message_type]['pin'],0)
#         self.__notification_leds[message_type]['state'] = False
#         self.__notification_leds[message_type]['lastaction'] = now

#   def set_email(self,receiver,server,serverport = 25,username = None,password = None):
#     if '' != receiver and '' != server:
#       self.email = {'receiver'   : receiver.split(','),
#                     'server'     : server,
#                     'serverport' : serverport,
#                     'username'   : username,
#                     'password'   : password}

#   def set_twitter(self,consumer_key,consumer_secret,access_token,access_token_secret):
#     if '' != consumer_key and '' != consumer_secret and '' != access_token and '' != access_token_secret:
#       self.twitter = {'consumer_key'        : consumer_key,
#                       'consumer_secret'     : consumer_secret,
#                       'access_token'        : access_token,
#                       'access_token_secret' : access_token_secret}

#   def update_twitter_profile_image(self):
#     if self.__profile_image is not None and self.twitter is not None:
#       try:
#         api = twitter.Api(consumer_key=self.twitter['consumer_key'],
#                           consumer_secret=self.twitter['consumer_secret'],
#                           access_token_key=self.twitter['access_token'],
#                           access_token_secret=self.twitter['access_token_secret'])

#         if api.VerifyCredentials() is not None:
#           status = api.UpdateImage(self.__profile_image)

#       except Exception as ex:
#         print(ex)

#   def send_tweet(self,title,message,files = []):
#     if self.twitter is None:
#       return

#     try:
#       api = twitter.Api(consumer_key=self.twitter['consumer_key'],
#                         consumer_secret=self.twitter['consumer_secret'],
#                         access_token_key=self.twitter['access_token'],
#                         access_token_secret=self.twitter['access_token_secret'])

#       if api.VerifyCredentials() is not None:
#         if len(files) > 0:
#           status = api.PostUpdate(title[:278 - (title.decode('utf-8').count("\n"))],media=files)
#         else:
#           status = api.PostUpdate(message[:278 - (message.decode('utf-8').count("\n"))])
#     except Exception as ex:
#       print(ex)

#   def set_pushover(self,api_token,user_key):
#     if '' != api_token and '' != user_key:
#       self.pushover = {'api_token' : api_token,
#                        'user_key'  : user_key}

#   def send_pushover(self,subject,message,files = []):
#     if self.pushover is None:
#       return

#     try:
#       client = pushover.Client(self.pushover['user_key'], api_token=self.pushover['api_token'])
#       if client.verify():
#         if files is None or len(files) == 0:
#           status = client.send_message(message, title=subject)
#         elif len(files) > 0:
#           for image in files:
#             with open(image,'rb') as image:
#               status = client.send_message(message, title=subject,attachment=image)

#     except Exception as ex:
#       print(ex)

#   def set_telegram(self,bot_token,userid,proxy):
#     if '' != bot_token and '' != userid:
#       if self.telegram is None:
#         self.telegram = terrariumNotificationTelegramBot(bot_token,userid,proxy)
#       else:
#         self.telegram.set_valid_users(userid)
#         self.telegram.set_proxy(proxy)
#         self.telegram.start()

#   def send_telegram(self,subject,message,files = []):
#     if self.telegram is None:
#       return

#     if (files is None or len(files) == 0):
#       self.telegram.send_message(message.decode('utf-8'))
#     else:
#       self.telegram.send_image(subject.decode('utf-8'),files)

#   def set_display(self,address,hardwaretype,title):
#     self.display = None
#     if address is not None and '' != address:
#       try:
#         self.display = terrariumDisplay(None,hardwaretype,address,'notification',title)
#       except terrariumDisplaySourceException as ex:
#         print(ex)
#         self.display = None

#       if self.__profile_image is not None and self.display is not None:
#         self.display.write_image(self.__profile_image)

#   def send_display(self,message):
#     if self.display is not None:
#       self.display.message(message)


#   def message(self,message_id,data = None,files = []):
#     self.send_notication_led(message_id)

#     if message_id not in self.messages or not self.messages[message_id].is_enabled():
#       return

#     now = str(self.__current_minute())
#     title = self.__parse_message(self.messages[message_id].get_title(),data)
#     message = self.__parse_message(self.messages[message_id].get_message(),data)

#     if '' == title:
#       title = 'no_title'

#     # Do not rate limit webhooks
#     if self.messages[message_id].is_webhook_enabled():
#       # Always use raw_data for webhooks
#       self.send_webhook(self.__parse_message(self.webhook['address'],data),self.__parse_message('%raw_data%',data),files)

#     if title not in self.__ratelimit_messages:
#       self.__ratelimit_messages[title] = {}

#     if now not in self.__ratelimit_messages[title]:
#       self.__ratelimit_messages[title][now] = 0

#     if self.__ratelimit_messages[title][now] > terrariumNotification.__MAX_MESSAGES_PER_MINUTE:
#       print('%s - WARNING - terrariumNotificatio - Max messages per minute %s reached for \'%s\'' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],
#                                                                                                  terrariumNotification.__MAX_MESSAGES_PER_MINUTE, title.decode()))
#       return

#     if self.__ratelimit() > terrariumNotification.__MAX_MESSAGES_TOTAL_PER_MINUTE:
#       print('%s - WARNING - terrariumNotificatio - Max total messages per minute %s reached' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],
#                                                                                                 terrariumNotification.__MAX_MESSAGES_TOTAL_PER_MINUTE))
#       return

#     try:
#       self.__ratelimit_messages[title][now] += 1
#     except KeyError as ex:
#       # Somehow we get a key error while it should be there....
#       self.__ratelimit_messages[title][now] = 1

#     if self.messages[message_id].is_email_enabled():
#       self.send_email(title,message,files)

#     if self.messages[message_id].is_twitter_enabled():
#       self.send_tweet(title,message,files)

#     if self.messages[message_id].is_pushover_enabled():
#       self.send_pushover(title,message,files)

#     if self.messages[message_id].is_telegram_enabled():
#       self.send_telegram(title,message,files)

#     if self.messages[message_id].is_display_enabled():
#       self.send_display(message)

#   def get_messages(self):
#     data = []
#     for message_id in sorted(self.messages.keys()):
#       data.append(self.messages[message_id].get_data())

#     return data
