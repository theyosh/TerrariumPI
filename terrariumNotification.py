# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(None)

import re

from string import Template
from gevent import sleep
import datetime
from operator import itemgetter

from threading import Timer
from hashlib import md5

from terrariumDatabase import NotificationMessage, NotificationService
from terrariumUtils import terrariumUtils, terrariumSingleton, classproperty

# Display support
#from terrariumDisplay import terrariumDisplay, terrariumDisplaySourceException

# Traffic light Support
import RPi.GPIO as GPIO

# Email support
import emails

# MQTT Support
import paho.mqtt.client as mqtt
import json

import requests
import copy
from pony import orm

class terrariumNotification(terrariumSingleton):
  __MAX_MESSAGES_TOTAL_PER_MINUTE = 60

  __MESSAGES = {
    'authentication_error' : _('Authentication login error'),
    'system_warning'       : _('System warning'),
    'system_error'         : _('System error'),

    'sensor_update'        : _('Sensor update'),
    'sensor_alarm'         : _('Sensor alarm'),

    'relay_change'         : _('Relay change'),

    'button_change'        : _('Button change'),

    'webcam_archive'       : _('Webcam archive')
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

        self.services[service.id].send_message(message_id, title, text, data)

  def stop(self):
    for serviceid in self.services:
      self.services[serviceid].stop()


class terrariumNotificationServiceException(TypeError):
  '''There is a problem with loading a hardware switch. Invalid power switch action.'''

  def __init__(self, message, *args):
    self.message = message
    super().__init__(message, *args)

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

#     'telegram' : {
#       'name'    : _('Telegram'),
# #      'class' : lambda: terrariumAreaHumidity
#     },

    'traffic' : {
      'name'    : _('Traffic light'),
      'class' : lambda: terrariumNotificationServiceTrafficLight
    },
    'webhook' : {
      'name'    : _('Web-hook'),
      'class' : lambda: terrariumNotificationServiceWebhook
    },
    'mqtt' : {
      'name'    : _('MQTT'),
      'class' : lambda: terrariumNotificationServiceMQTT
    },
    'pushover' : {
      'name': _('Pushover'),
      'class': lambda: terrariumNotificationServicePushover
    }
  }

  @classproperty
  def available_services(__cls__):
    data = []
    for (type, area) in terrariumNotificationService.__TYPES.items():
      data.append({'type' : type, 'name' : area['name']})

    return sorted(data, key=itemgetter('name'))

  # Return polymorph service....
  def __new__(cls, id, type, name = '', enabled = True, setup = None):
    if type not in [service['type'] for service in terrariumNotificationService.available_services]:
      raise terrariumNotificationServiceException(f'Service of type {type} is unknown.')

    return super(terrariumNotificationService, cls).__new__(terrariumNotificationService.__TYPES[type]['class']())

  def __init__(self, id, type, name, enabled, setup):
    # Hacky to fix the logging in these classes...
    global logger
    logger = terrariumLogging.logging.getLogger(__name__)

    if id is None:
      id = terrariumUtils.generate_uuid()

    self.id   = id
    self.type = type
    self.name = name
    self.enabled = enabled

    self.setup = {}
    self.load_setup(setup)

  def __repr__(self):
    return f'{terrariumNotificationService.__TYPES[self.type]["name"]} service {self.name}'

  def load_setup(self, setup_data):
    self.setup['version']       = setup_data.get('version')
    self.setup['profile_image'] = setup_data.get('profile_image')

  def stop(self):
    pass

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

  def send_message(self, type, subject, message, data = None, attachments = []):
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

  def send_message(self, type, subject, message, data = None, attachments = []):
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

  def send_message(self, type, subject, message, data = None, attachments = []):
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
      logger.error(f'Error sending webhook to url \'{self.setup["address"]}\' with status code: {r.status_code}')

class terrariumNotificationServiceTrafficLight(terrariumNotificationService):
  __YELLOW_TIMEOUT = 5 * 60
  __RED_TIMEOUT = 15 * 60

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

  def send_message(self, type, subject, message, data = None, attachments = []):
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
  # The callback for when the client receives a CONNACK response from the server.
  def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
      logger.info(f'Logged in to MQTT Broker at address: {self.setup["address"]}:{self.setup["port"]}.')

    else:
      self.connection = None
      logger.error(f'Error! Login to MQTT Broker at address: {self.setup["address"]}:{self.setup["port"]} failed! Error code: {rc}')

  def load_setup(self, setup_data):
    self.setup = {
      'address'   : setup_data.get('address'),
      'port'      : int(setup_data.get('port')),
      'username'  : setup_data.get('username'),
      'password'  : setup_data.get('password')
    }

    super().load_setup(setup_data)

    self.connection = None

    try:
      self.connection = mqtt.Client()
      self.connection.on_connect = self.on_connect
      self.connection.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
      self.connection.username_pw_set(terrariumUtils.decrypt(self.setup['username']), terrariumUtils.decrypt(self.setup['password']))
      self.connection.connect(self.setup['address'], self.setup['port'], 30)
      self.connection.loop_start()
      logger.info(f'Connected to MQTT Broker at address: {self.setup["address"]}:{self.setup["port"]}')

    except Exception as ex:
      logger.exception(f'Failed connecting to MQTT Broker at address: {self.setup["address"]}:{self.setup["port"]}: {ex}')

  def stop(self):
    # TODO: Flush the queueu

    if self.connection is not None:
      try:
        self.connection.loop_stop()
      except Exception as ex:
        # Ignore
        pass

      self.connection.disconnect()

    logger.info(f'Disconnected from the MQTT Broker at address: {self.setup["address"]}:{self.setup["port"]}')

  def send_message(self, type, subject, message, data = None, attachments = []):
    if self.connection is not None:
      topic = type.replace('_','/')
      topic = f'terrariumpi/{topic}'

      if data is None:
        data = {}

      # Add a unique ID to make clients able to filter duplicate messages
      data['uuid']    = terrariumUtils.generate_uuid()
      # Add the 'direct' topic to subscribe to
      data['topic']   = topic
      # Add the subject
      data['subject'] = subject
      # Add the message
      data['message'] = message

      self.connection.publish(f'terrariumpi/{type}', payload=json.dumps(data), qos=1)
    else:
      logger.error(f'Could not send message {data["subject"]} to topic {data["topic"]} as we are not connected to the MQTT broker at address: {self.setup["address"]}:{self.setup["port"]}')


class terrariumNotificationServicePushover(terrariumNotificationService):
  def load_setup(self, setup_data):
    self.setup = {
      'api_token' : setup_data.get('api_token'),
      'user_key'  : setup_data.get('user_key'),

      'address'   : 'https://api.pushover.net/1/messages.json' # https://support.pushover.net/i44-example-code-and-pushover-libraries#python-image
    }

    super().load_setup(setup_data)

  def send_message(self, type, subject, message, data = None, attachments = []):
    attachment = None
    if len(attachments) > 0:
      attachment = {'attachment' : (os.path.basename(attachments[0]), open(attachments[0],'rb'), 'image/jpeg')}

    r = requests.post(self.setup['address'],
      data = {
        'token'    : self.setup['api_token'],
        'user_key' : self.setup['user_key'],
        'message'  : f'{subject}\n{message}'
      },
      files = attachment
    )

    if r.status_code != 200:
      logger.error(f'Error sending Pusover message \'{subject}\' with status code: {r.status_code}')