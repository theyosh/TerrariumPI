# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import gettext
gettext.install('terrariumpi', 'locales/', unicode=True)

import re
import ConfigParser

# Email support
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Twitter support
import twitter

# Pushover support
import pushover

# Telegram support
from telegram.ext import Updater

from terrariumUtils import terrariumUtils

class terrariumNotificationMessage(object):

  def __init__(self,message_id, title, message, enabled = False):
    self.enabled = terrariumUtils.is_true(enabled)
    self.id = message_id
    self.title = title.strip()
    self.message = message.strip()

  def get_id(self):
    return self.id

  def get_title(self):
    return self.title

  def get_message(self):
    return self.message

  def is_enabled(self):
    return self.message != '' and self.enabled == True

  def get_data(self):
    return {'id':self.get_id(),
            'title':self.get_title(),
            'message':self.get_message(),
            'enabled':self.is_enabled(),
            }

class terrariumNotification(object):
  __regex_parse = re.compile(r"%(?P<index>[^% ]+)%")

  __default_notifications = {
    'environment_light_alarm_low_on' : terrariumNotificationMessage('environment_light_alarm_low_on',_('Environment light day on'),'%raw_data%'),
    'environment_light_alarm_low_off' : terrariumNotificationMessage('environment_light_alarm_low_off',_('Environment light day off'),'%raw_data%'),
    'environment_light_alarm_high_on' : terrariumNotificationMessage('environment_light_alarm_high_on',_('Environment light night on'),'%raw_data%'),
    'environment_light_alarm_high_off' : terrariumNotificationMessage('environment_light_alarm_high_off',_('Environment light night off'),'%raw_data%'),

    'environment_temperature_alarm_low_on' : terrariumNotificationMessage('environment_temperature_alarm_low_on',_('Environment temperature alarm low on'),'%raw_data%'),
    'environment_temperature_alarm_low_off' : terrariumNotificationMessage('environment_temperature_alarm_low_off',_('Environment temperature alarm low off'),'%raw_data%'),
    'environment_temperature_alarm_high_on' : terrariumNotificationMessage('environment_temperature_alarm_high_on',_('Environment temperature alarm high on'),'%raw_data%'),
    'environment_temperature_alarm_high_off' : terrariumNotificationMessage('environment_temperature_alarm_high_off',_('Environment temperature alarm high off'),'%raw_data%'),

    'environment_humidity_alarm_low_on' : terrariumNotificationMessage('environment_humidity_alarm_low_on',_('Environment humidity alarm low on'),'%raw_data%'),
    'environment_humidity_alarm_low_off' : terrariumNotificationMessage('environment_humidity_alarm_low_off',_('Environment humidity alarm low off'),'%raw_data%'),
    'environment_humidity_alarm_high_on' : terrariumNotificationMessage('environment_humidity_alarm_high_on',_('Environment humidity alarm high on'),'%raw_data%'),
    'environment_humidity_alarm_high_off' : terrariumNotificationMessage('environment_humidity_alarm_high_off',_('Environment humidity alarm high off'),'%raw_data%'),

    'environment_moisture_alarm_low_on' : terrariumNotificationMessage('environment_moisture_alarm_low_on',_('Environment moisture alarm low on'),'%raw_data%'),
    'environment_moisture_alarm_low_off' : terrariumNotificationMessage('environment_moisture_alarm_low_off',_('Environment moisture alarm low off'),'%raw_data%'),
    'environment_moisture_alarm_high_on' : terrariumNotificationMessage('environment_moisture_alarm_high_on',_('Environment moisture alarm high on'),'%raw_data%'),
    'environment_moisture_alarm_high_off' : terrariumNotificationMessage('environment_moisture_alarm_high_off',_('Environment moisture alarm high off'),'%raw_data%'),

    'environment_conductivity_alarm_low_on' : terrariumNotificationMessage('environment_conductivity_alarm_low_on',_('Environment conductivity alarm low on'),'%raw_data%'),
    'environment_conductivity_alarm_low_off' : terrariumNotificationMessage('environment_conductivity_alarm_low_off',_('Environment conductivity alarm low off'),'%raw_data%'),
    'environment_conductivity_alarm_high_on' : terrariumNotificationMessage('environment_conductivity_alarm_high_on',_('Environment conductivity alarm high on'),'%raw_data%'),
    'environment_conductivity_alarm_high_off' : terrariumNotificationMessage('environment_conductivity_alarm_high_off',_('Environment conductivity alarm high off'),'%raw_data%'),

    'environment_ph_alarm_low_on' : terrariumNotificationMessage('environment_ph_alarm_low_on',_('Environment pH alarm low on'),'%raw_data%'),
    'environment_ph_alarm_low_off' : terrariumNotificationMessage('environment_ph_alarm_low_off',_('Environment pH alarm low off'),'%raw_data%'),
    'environment_ph_alarm_high_on' : terrariumNotificationMessage('environment_ph_alarm_high_on',_('Environment pH alarm high on'),'%raw_data%'),
    'environment_ph_alarm_high_off' : terrariumNotificationMessage('environment_ph_alarm_high_off',_('Environment pH alarm high off'),'%raw_data%'),

    'environment_watertank_alarm_low_on' : terrariumNotificationMessage('environment_watertank_alarm_low_on',_('Environment watertank alarm low on'),'%raw_data%'),
    'environment_watertank_alarm_low_off' : terrariumNotificationMessage('environment_watertank_alarm_low_off',_('Environment watertank alarm low off'),'%raw_data%'),
    'environment_watertank_alarm_high_on' : terrariumNotificationMessage('environment_watertank_alarm_high_on',_('Environment watertank alarm high on'),'%raw_data%'),
    'environment_watertank_alarm_high_off' : terrariumNotificationMessage('environment_watertank_alarm_high_off',_('Environment watertank alarm high off'),'%raw_data%'),

    'system_warning' : terrariumNotificationMessage('system_warning',_('System warning messages'),'%message%'),
    'system_error' : terrariumNotificationMessage('system_error',_('System error messages'),'%message%'),

    'sensor_alarm_low_on' : terrariumNotificationMessage('sensor_alarm_low_on',_('Sensor alarm low on'),'%raw_data%'),
    'sensor_alarm_low_off' : terrariumNotificationMessage('sensor_alarm_low_off',_('Sensor alarm low off'),'%raw_data%'),
    'sensor_alarm_high_on' : terrariumNotificationMessage('sensor_alarm_high_on',_('Sensor alarm high on'),'%raw_data%'),
    'sensor_alarm_high_off' : terrariumNotificationMessage('sensor_alarm_high_off',_('Sensor alarm high off'),'%raw_data%'),

    'switch_toggle_on' : terrariumNotificationMessage('switch_toggle_on',_('Powerswitch toggle on'),'%raw_data%'),
    'switch_toggle_off' : terrariumNotificationMessage('switch_toggle_off',_('Powerswitch toggle off'),'%raw_data%'),

    'door_toggle_open' : terrariumNotificationMessage('door_toggle_open',_('Door open'),'%raw_data%'),
    'door_toggle_closed' : terrariumNotificationMessage('door_toggle_closed',_('Door closed'),'%raw_data%'),

    'webcam_archive' : terrariumNotificationMessage('webcam_archive',_('Webcam archive'),'%raw_data%'),

  }

  def __init__(self):
    self.email = None
    self.twitter = None
    self.pushover = None
    self.telegram = None

    self.__load_config()
    self.__load_messages()

  def __load_config(self):
    self.__data = ConfigParser.SafeConfigParser()
    self.__data.read('notifications.cfg')

    if self.__data.has_section('email'):
      self.set_email(self.__data.get('email','receiver'),
                     self.__data.get('email','server'),
                     self.__data.get('email','serverport'),
                     self.__data.get('email','username'),
                     self.__data.get('email','password'))

    if self.__data.has_section('twitter'):
      self.set_twitter(self.__data.get('twitter','consumer_key'),
                     self.__data.get('twitter','consumer_secret'),
                     self.__data.get('twitter','access_token'),
                     self.__data.get('twitter','access_token_secret'))

    if self.__data.has_section('pushover'):
      self.set_pushover(self.__data.get('pushover','api_token'),
                        self.__data.get('pushover','user_key'))

    if self.__data.has_section('telegram'):
      self.set_telegram(self.__data.get('telegram','bot_token'),
                        self.__data.get('telegram','userid'))

  def __load_messages(self,data = None):
    self.messages = {}
    for message_id in self.__default_notifications:
      if self.__data.has_section('message' + message_id):
        self.messages[message_id] = terrariumNotificationMessage(message_id,
                                                                 self.__data.get('message' + message_id,'title'),
                                                                 self.__data.get('message' + message_id,'message'),
                                                                 self.__data.get('message' + message_id,'enabled'))
      else:
        self.messages[message_id] = self.__default_notifications[message_id]

  def __parse_message(self,message,data):
    if data is None:
      return message

    # Some dirty cleanup... :(
    try:
      del(data['timer_min']['time_table'])
    except:
      pass

    try:
      del(data['timer_max']['time_table'])
    except:
      pass

    data = terrariumUtils.flatten_dict(data)
    for item in terrariumNotification.__regex_parse.findall(message):
      if 'raw_data' == item:
        message = message.replace('%' + item + '%',str(data)
                                                    .replace(',',"\n")
                                                    .replace('{',' ')
                                                    .replace('}',''))
      elif item in data:
        message = message.replace('%' + item + '%',str(data[item]))

    return message

  def __update_config(self,section,data,exclude = []):
    '''Update terrariumPI config with new values

    Keyword arguments:
    section -- section in configuration. If not exists it will be created
    data -- data to save in dict form'''

    if not self.__data.has_section(section):
      self.__data.add_section(section)

    keys = data.keys()
    keys.sort()
    for setting in keys:
      if setting in exclude:
        continue

      if type(data[setting]) is list:
        data[setting] = ','.join(data[setting])

      if isinstance(data[setting], basestring):
        try:
          data[setting] = data[setting].encode('utf-8').replace('%','%%')
        except Exception, ex:
          'Not sure what to do... but it seams already utf-8...??'
          pass

      self.__data.set(section, str(setting), str(data[setting]))

  def set_email(self,receiver,server,serverport = 25,username = None,password = None):
    self.email = {'receiver'   : receiver.split(','),
                  'server'     : server,
                  'serverport' : serverport,
                  'username'   : username,
                  'password'   : password}

  def send_email(self,subject,message):
    mailserver = None
    try:
      mailserver = smtplib.SMTP(self.email['server'],self.email['serverport'],timeout=15)
    except Exception, ex:
      print ex
      try:
        mailserver = smtplib.SMTP_SSL(self.email['server'],self.email['serverport'],timeout=15)
      except Exception, ex:
        print ex
        print 'ERROR Mailserver is not reachable!'
        return

    if mailserver is None:
      print 'ERROR Mailserver is not reachable!'
      return

    mailserver.ehlo()
    try:
      mailserver.starttls()
      mailserver.ehlo()
    except:
      pass

    if self.email['username'] is not None and self.email['password'] is not None and '' != self.email['username'] and '' != self.email['password']:
      try:
        mailserver.login(self.email['username'], self.email['password'])
      except Exception, ex:
        print ex
        print 'ERROR Mailserver login credentials are invalid. Cannot sent mail!'
        return

    for receiver in self.email['receiver']:
      msg = MIMEMultipart()
      msg['From'] = receiver
      msg['To'] = re.sub(r"(.*)@(.*)", "\\1+terrariumpi@\\2", receiver, 0, re.MULTILINE)
      msg['Subject'] = subject
      msg.attach(MIMEText(message))

      try:
        mailserver.sendmail(receiver,re.sub(r"(.*)@(.*)", "\\1+terrariumpi@\\2", receiver, 0, re.MULTILINE),msg.as_string())
      except Exception, ex:
        print ex

    mailserver.quit()

  def set_twitter(self,consumer_key,consumer_secret,access_token,access_token_secret):
    self.twitter = {'consumer_key'        : consumer_key,
                    'consumer_secret'     : consumer_secret,
                    'access_token'        : access_token,
                    'access_token_secret' : access_token_secret}

  def send_tweet(self,message):
    # For now, disable during development
    return

    try:
      api = twitter.Api(consumer_key=self.twitter['consumer_key'],
                        consumer_secret=self.twitter['consumer_secret'],
                        access_token_key=self.twitter['access_token'],
                        access_token_secret=self.twitter['access_token_secret'])

      if api.VerifyCredentials() is not None:
        status = api.PostUpdates(message)
        # [Status(ID=1003393079041314816, ScreenName=MadagascarGecko, Created=Sun Jun 03 21:48:46 +0000 2018, Text=u'Environment watertank sensors are not up to date. Check your sensors on the sensor page. So force the power down to be sure!')]
    except Exception, ex:
      print ex
      logger.exception(ex)



  def set_pushover(self,api_token,user_key):
    self.pushover = {'api_token' : api_token,
                     'user_key'  : user_key}

  def send_pushover(self,subject,message):
    # For now, disable during development
    return

    try:
      client = pushover.Client(self.pushover['user_key'], api_token=self.pushover['api_token'])
      if client.verify():
        status = client.send_message(message, title=subject)
        # {u'status': 1, u'request': u'daad6828-3efe-44d9-89eb-9922fa8e0dda'}
    except Exception, ex:
      print ex
      logger.exception(ex)

  def set_telegram(self,bot_token,userid):
    self.telegram = {'bot_token' : bot_token,
                     'userid'  : userid}

  def send_telegram(self,subject,message):
    # For now, disable during development
    return

    try:
      updater = Updater(self.telegram['bot_token'])
      status = updater.bot.send_message(chat_id=self.telegram['userid'], text=message)
      # {'delete_chat_photo': False, 'new_chat_photo': [], 'from': {'username': u'terrariumpi_bot', 'first_name': u'TerrariumPI', 'is_bot': True, 'id': 519390339}, 'text': u'Dimmer PWM Dimmer is already working. Ignoring state change!. Will switch to latest state value when done', 'caption_entities': [], 'entities': [], 'channel_chat_created': False, 'new_chat_members': [], 'supergroup_chat_created': False, 'chat': {'first_name': u'Yoshie', 'last_name': u'Online', 'type': u'private', 'id': 508490874}, 'photo': [], 'date': 1528062541, 'group_chat_created': False, 'message_id': 14}
    except Exception, ex:
      print ex
      logger.exception(ex)

  def message(self,message_id,data = None):
    if message_id not in self.messages or not self.messages[message_id].is_enabled():
      return

    title = self.__parse_message(self.messages[message_id].get_title(),data)
    message = self.__parse_message(self.messages[message_id].get_message(),data)

    if self.email is not None:
      self.send_email(title,message)

    if self.twitter is not None:
      self.send_tweet(message)

    if self.pushover is not None:
      self.send_pushover(title,message)

    if self.telegram is not None:
      self.send_telegram(title,message)

  def get_messages(self):
    data = []
    for message_id in sorted(self.messages.keys()):
      data.append(self.messages[message_id].get_data())

    return data

  def set_config(self,data):
    try:
      self.__update_config('email',{'receiver'   : data['email_receiver'],
                                    'server'     : data['email_server'],
                                    'serverport' : data['email_serverport'],
                                    'username'   : data['email_username'],
                                    'password'   : data['email_password']})

      self.__update_config('twitter',{'consumer_key'        : data['twitter_consumer_key'],
                                      'consumer_secret'     : data['twitter_consumer_secret'],
                                      'access_token'        : data['twitter_access_token'],
                                      'access_token_secret' : data['twitter_access_token_secret']})

      self.__update_config('pushover',{'api_token' : data['pushover_api_token'],
                                       'user_key'  : data['pushover_user_key']})

      self.__update_config('telegram',{'bot_token' : data['telegram_bot_token'],
                                       'userid'  : data['telegram_userid']})

    except Exception, ex:
      print ex

    for message_id in data:
      if message_id[-8:] == '_enabled':
        message_id = message_id[:-8]
        if message_id in self.messages:
          self.messages[message_id] = terrariumNotificationMessage(message_id,
                                                                   data[message_id + '_title'],
                                                                   data[message_id + '_message'],
                                                                   terrariumUtils.is_true(data[message_id + '_enabled']))

          self.__data.remove_section('message' + message_id)
          self.__update_config('message' + message_id,{'id'      : message_id,
                                                       'title'   : data[message_id + '_title'],
                                                       'message' : data[message_id + '_message'],
                                                       'enabled' : data[message_id + '_enabled']})

    with open('notifications.cfg', 'wb') as configfile:
      self.__data.write(configfile)

    self.__load_config()
    return True

  def get_config(self):
    data = {
      'email' : dict(self.email) if self.email is not None else {},
      'twitter' : dict(self.twitter) if self.twitter is not None else {},
      'pushover' : dict(self.pushover) if self.pushover is not None else {},
      'telegram' : dict(self.telegram) if self.telegram is not None else {},
      'messages' : self.get_messages() }

    data['email']['receiver'] = ','.join(data['email']['receiver'])
    return data
