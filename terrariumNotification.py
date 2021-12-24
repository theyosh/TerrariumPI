# -*- coding: utf-8 -*-
import os
import terrariumLogging
logger = terrariumLogging.logging.getLogger(None)

import re
import datetime
import requests
import copy

# Traffic light Support
import RPi.GPIO as GPIO

# Email support
import emails

# MQTT Support
import paho.mqtt.client as mqtt
import json

from pony import orm
from string import Template
from gevent import sleep
from operator import itemgetter
from threading import Timer
from base64 import b64encode

from terrariumDatabase import NotificationMessage, NotificationService
from terrariumUtils import terrariumUtils, terrariumSingleton, classproperty

# Display support
from hardware.display import terrariumDisplay, terrariumDisplayLoadingException


class terrariumNotification(terrariumSingleton):
  __DEFAULT_PLACEHOLDERS = {
    'date' : _('Local date'),
    'time' : _('Local time'),
    'now'  : _('Local date and time'),
  }

  __MAX_MESSAGES_TOTAL_PER_MINUTE = 60

  __MESSAGES = {

    'authentication_error' : {
      'name':_('Authentication login error'),
      'placeholders' : {
        'ip'       : _('IP of the wrong login attempt'),
        'username' : _('Used username'),
        'password' : _('Used password'),
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'system_warning' : {
      'name':_('System warning'),
      'placeholders' : {
        'message' : _('Warning message'),
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'system_error' : {
      'name':_('System error'),
      'placeholders' : {
        'message' : _('Error message'),
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'system_summary' : {
      'name':_('System summary'),
      'placeholders' : {
        'uptime' : _('System uptime in humand readable format'),
        'system_load' : _('System load last minute'),
        'system_load_alarm' : _('True if there is an alarm'),
        'cpu_temperature' : _('System CPU temperature'),
        'cpu_temperature_alarm' : _('True if there is an alarm'),
        'storage' : _('Storage usage'),
        'memory' : _('Memory usage'),
        'average_[sensor_type]' : _('Average of [sensor type] (ex. temperature)'),
        'average_[sensor_type]_unit' : _('Sensor type unit value'),
        'average_[sensor_type]_alarm' : _('True if there is an alarm'),
        'current_watt' : _('Current power usage'),
        'max_watt' : _('Max power usage'),
        'current_flow' : _('Current water flow'),
        'max_flow' : _('Max water flow'),
        'relays_active' : _('Number of relays active'),
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'sensor_update' : {
      'name':_('Sensor update (every 30 seconds)'),
      'placeholders' : {
        'id': _('ID'),
        'hardware': _('Hardware type'),
        'type': _('Sensor type'),
        'name': _('Name'),
        'address': _('Address'),
        'limit_min': _('Limit min'),
        'limit_max': _('Limit max'),
        'alarm_min': _('Alarm min'),
        'alarm_max': _('Alarm max'),
        'max_diff': _('Max difference'),
        'exclude_avg': _('Exclude from average'),
        'alarm': _('True if there is an alarm'),
        'value': _('Current value'),
        'error': _('True if there is an error'),
        'unit' : _('Sensor type unit value'),
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'sensor_change' : {
      'name':_('Sensor change (only when value is changed)'),
      'placeholders' : {
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'sensor_alarm' : {
      'name':_('Sensor alarm'),
      'placeholders' : {
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'relay_update' : {
      'name':_('Relay update (every 30 seconds)'),
      'placeholders' : {
        'id': _('ID'),
        'hardware': _('Hardware type'),
        'name': _('Name'),
        'address': _('Address'),
        'wattage': _('Max wattage'),
        'flow': _('Max water flow'),
        'manual_mode': _('True if in manual mode'),
        'dimmer': _('True if it is a dimmer'),
        'value': _('Current state'),
        'error': _('True if there is an error'),
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'relay_change' : {
      'name':_('Relay change (only when value is changed)'),
      'placeholders' : {
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'relay_toggle' : {
      'name':_('Relay toggle'),
      'placeholders' : {
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'button_update' : {
      'name':_('Button update (every 30 seconds)'),
      'placeholders' : {
        'id': _('ID'),
        'hardware': _('Hardware type'),
        'name': _('Name'),
        'address': _('Address'),
        'value': _('Current state'),
        'error': _('True if there is an error'),
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'button_change' : {
      'name':_('Button change (only when value is changed)'),
      'placeholders' : {
        **__DEFAULT_PLACEHOLDERS
      }
    },

    'button_action' : {
      'name':_('Button action'),
      'placeholders' : {
        **__DEFAULT_PLACEHOLDERS
      }
    },


    'webcam_archive' : {
      'name':_('Webcam archive'),
      'placeholders' : {
        **__DEFAULT_PLACEHOLDERS
      }
    },
  }

  __MESSAGES['sensor_change']['placeholders'] = __MESSAGES['sensor_update']['placeholders']
  __MESSAGES['sensor_alarm']['placeholders']  = __MESSAGES['sensor_update']['placeholders']

  __MESSAGES['relay_change']['placeholders']  = __MESSAGES['relay_update']['placeholders']
  __MESSAGES['relay_toggle']['placeholders']  = __MESSAGES['relay_update']['placeholders']

  __MESSAGES['button_change']['placeholders'] = __MESSAGES['button_update']['placeholders']
  __MESSAGES['button_action']['placeholders'] = __MESSAGES['button_update']['placeholders']


  @classproperty
  def available_messages(__cls__):
    data = []
    for (type, msgdata) in terrariumNotification.__MESSAGES.items():
      data.append({'type' : type, 'name' : msgdata['name'], 'placeholders' : msgdata['placeholders']})

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
        service = service.to_dict()
        if service['id'] not in self.services:
          setup = copy.deepcopy(service['setup'])
          setup['version']       = self.version
          setup['profile_image'] = self.profile_image
          try:
            self.services[service['id']] = terrariumNotificationService(service['id'], service['type'], service['name'], service['enabled'], setup)
          except terrariumDisplayLoadingException as ex:
            self.services[service['id']] = None
            logger.error(f'Error loading display {service["name"]}: {ex}')

  def broadcast(self, subject, message, image):
    for _, service in self.services.items():
      if service is not None and service.enabled:
        service.send_message('system_broadcast', subject, message, None, [image])

  @property
  def version(self):
    return None if self.engine is None else self.engine.version

  @property
  def profile_image(self):
    return None if self.engine is None else self.engine.settings['profile_image']

  def message(self, message_id, data = {}, files = []):
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
      data['date'] = datetime.datetime.now().strftime('%x')
      data['time'] = datetime.datetime.now().strftime('%X')
      data['now'] = data['date'] + ' ' + data['time']
      title = Template(message.title).safe_substitute(**data)
      text  = Template(message.message).safe_substitute(**data)

      if message.rate_limit > 0 and self.__rate_limit(title, message.rate_limit):
        logger.warning(f'Hitting the max rate limit of {self.__rate_limiter_counter[title]["rate"]} messages per minute for message {message.title}. Message will be ignored.')
        return

      for service in message.services:

        if self.services[service.id] is None:
          logger.debug(f'Ignoring service {self} as it did not loaded correctly.')
          continue

        if not service.enabled:
          logger.debug(f'Service {self} is (temporary) disabled.')
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
    for _, service in self.services.items():
      if service is not None:
        service.stop()

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


class terrariumNotificationServiceDisplay(terrariumNotificationService):

  def load_setup(self, setup_data):
    super().load_setup(setup_data)

    # Now load the actual display device
    self.setup['device'] = terrariumDisplay(None, setup_data['hardware'], setup_data['address'], None if not terrariumUtils.is_true(setup_data['show_title']) else f'TerrariumPI {self.setup["version"]}')
    self.show_picture(self.setup['profile_image'])

  def send_message(self, type, subject, message, data = None, attachments = []):
    self.setup['device'].message(message)

  def show_picture(self, picture):
    self.setup['device'].write_image(picture)

  def stop(self):
    self.setup['device'].stop()

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
    # TODO: Flush the queue

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
    data = {
      'token'   : self.setup['api_token'],
      'user'    : self.setup['user_key'],
      'title'   : subject,
      'message' : message
    }

    if 'system_error' == type:
      data['sound'] = 'siren'

    attachment = None
    if len(attachments) > 0:
      attachment = {'attachment' : (os.path.basename(attachments[0]), open(attachments[0],'rb'), 'image/jpeg')}

    r = requests.post(self.setup['address'],
      data = data,
      files = attachment
    )

    if r.status_code != 200:
      logger.error(f'Error sending Pusover message \'{subject}\' with status code: {r.status_code}')