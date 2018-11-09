# -*- coding: utf-8 -*-
import re
import datetime
import RPi.GPIO as GPIO
import time
import os
import os.path
import _thread
import json
import sys
#import requests
#import urllib.parse

try:
  import configparser
except ImportError as ex:
  import ConfigParser as configparser

# Email support
import smtplib

#Python2
if sys.version_info.major == 2:
  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText
  from email.MIMEImage import MIMEImage

#Python3
if sys.version_info.major == 3:
  from email.message import EmailMessage
  from email.headerregistry import Address
  from email.utils import make_msgid

# Twitter support
import twitter

# Pushover support
import pushover

from terrariumUtils import terrariumUtils, terrariumSingleton
from terrariumDisplay import terrariumDisplay

from gevent import monkey, sleep
monkey.patch_all()

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

  def send_message(self,text, chat_id = None):
    if self.__running:
      chat_ids = self.__chat_ids if chat_id is None else [int(chat_id)]
#      text = urllib.parse.quote_plus(text)
      for chat_id in chat_ids:
        url = self.__bot_url + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
        terrariumUtils.get_remote_data(url,proxy=self.__proxy)

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

class terrariumNotification(terrariumSingleton):
  __MAX_MESSAGES_TOTAL_PER_MINUTE = 5
  __MAX_MESSAGES_PER_MINUTE = 2

  __regex_parse = re.compile(r'%(?P<index>[^% ]+)%')

  __default_notifications = {
    'environment_light_alarm_low_on' : terrariumNotificationMessage('environment_light_alarm_low_on','Environment light day on','%raw_data%'),
    'environment_light_alarm_low_off' : terrariumNotificationMessage('environment_light_alarm_low_off','Environment light day off','%raw_data%'),
    'environment_light_alarm_high_on' : terrariumNotificationMessage('environment_light_alarm_high_on','Environment light night on','%raw_data%'),
    'environment_light_alarm_high_off' : terrariumNotificationMessage('environment_light_alarm_high_off','Environment light night off','%raw_data%'),

    'environment_temperature_alarm_low_on' : terrariumNotificationMessage('environment_temperature_alarm_low_on','Environment temperature alarm low on','%raw_data%'),
    'environment_temperature_alarm_low_off' : terrariumNotificationMessage('environment_temperature_alarm_low_off','Environment temperature alarm low off','%raw_data%'),
    'environment_temperature_alarm_high_on' : terrariumNotificationMessage('environment_temperature_alarm_high_on','Environment temperature alarm high on','%raw_data%'),
    'environment_temperature_alarm_high_off' : terrariumNotificationMessage('environment_temperature_alarm_high_off','Environment temperature alarm high off','%raw_data%'),

    'environment_humidity_alarm_low_on' : terrariumNotificationMessage('environment_humidity_alarm_low_on','Environment humidity alarm low on','%raw_data%'),
    'environment_humidity_alarm_low_off' : terrariumNotificationMessage('environment_humidity_alarm_low_off','Environment humidity alarm low off','%raw_data%'),
    'environment_humidity_alarm_high_on' : terrariumNotificationMessage('environment_humidity_alarm_high_on','Environment humidity alarm high on','%raw_data%'),
    'environment_humidity_alarm_high_off' : terrariumNotificationMessage('environment_humidity_alarm_high_off','Environment humidity alarm high off','%raw_data%'),

    'environment_moisture_alarm_low_on' : terrariumNotificationMessage('environment_moisture_alarm_low_on','Environment moisture alarm low on','%raw_data%'),
    'environment_moisture_alarm_low_off' : terrariumNotificationMessage('environment_moisture_alarm_low_off','Environment moisture alarm low off','%raw_data%'),
    'environment_moisture_alarm_high_on' : terrariumNotificationMessage('environment_moisture_alarm_high_on','Environment moisture alarm high on','%raw_data%'),
    'environment_moisture_alarm_high_off' : terrariumNotificationMessage('environment_moisture_alarm_high_off','Environment moisture alarm high off','%raw_data%'),

    'environment_conductivity_alarm_low_on' : terrariumNotificationMessage('environment_conductivity_alarm_low_on','Environment conductivity alarm low on','%raw_data%'),
    'environment_conductivity_alarm_low_off' : terrariumNotificationMessage('environment_conductivity_alarm_low_off','Environment conductivity alarm low off','%raw_data%'),
    'environment_conductivity_alarm_high_on' : terrariumNotificationMessage('environment_conductivity_alarm_high_on','Environment conductivity alarm high on','%raw_data%'),
    'environment_conductivity_alarm_high_off' : terrariumNotificationMessage('environment_conductivity_alarm_high_off','Environment conductivity alarm high off','%raw_data%'),

    'environment_ph_alarm_low_on' : terrariumNotificationMessage('environment_ph_alarm_low_on','Environment pH alarm low on','%raw_data%'),
    'environment_ph_alarm_low_off' : terrariumNotificationMessage('environment_ph_alarm_low_off','Environment pH alarm low off','%raw_data%'),
    'environment_ph_alarm_high_on' : terrariumNotificationMessage('environment_ph_alarm_high_on','Environment pH alarm high on','%raw_data%'),
    'environment_ph_alarm_high_off' : terrariumNotificationMessage('environment_ph_alarm_high_off','Environment pH alarm high off','%raw_data%'),

    'environment_watertank_alarm_low_on' : terrariumNotificationMessage('environment_watertank_alarm_low_on','Environment watertank alarm low on','%raw_data%'),
    'environment_watertank_alarm_low_off' : terrariumNotificationMessage('environment_watertank_alarm_low_off','Environment watertank alarm low off','%raw_data%'),
    'environment_watertank_alarm_high_on' : terrariumNotificationMessage('environment_watertank_alarm_high_on','Environment watertank alarm high on','%raw_data%'),
    'environment_watertank_alarm_high_off' : terrariumNotificationMessage('environment_watertank_alarm_high_off','Environment watertank alarm high off','%raw_data%'),

    'system_warning' : terrariumNotificationMessage('system_warning','System warning message','%message%'),
    'system_error' : terrariumNotificationMessage('system_error','System error message','%message%'),

    'sensor_alarm_low' : terrariumNotificationMessage('sensor_alarm_low','Sensor %name% alarm low','%raw_data%'),
    'sensor_alarm_high' : terrariumNotificationMessage('sensor_alarm_high','Sensor %name% alarm high','%raw_data%'),

    'switch_toggle_on' : terrariumNotificationMessage('switch_toggle_on','Powerswitch %name% toggled on','%raw_data%'),
    'switch_toggle_off' : terrariumNotificationMessage('switch_toggle_off','Powerswitch %name% toggled off','%raw_data%'),

    'door_toggle_open' : terrariumNotificationMessage('door_toggle_open','Door %name% is open','%raw_data%'),
    'door_toggle_closed' : terrariumNotificationMessage('door_toggle_closed','Door %name% is closed','%raw_data%'),

  }

  def __init__(self,trafficlights = [], profile_image = None):
    self.__profile_image = None
    self.__ratelimit_messages = {}
    self.__notification_leds = {'info'      : {'pin' : None, 'state' : False, 'lastaction' : 0},
                                'warning'   : {'pin' : None, 'state' : False, 'lastaction' : 0},
                                'error'     : {'pin' : None, 'state' : False, 'lastaction' : 0},
                                'exception' : {'pin' : None, 'state' : False, 'lastaction' : 0},
                                }

    self.email = None
    self.twitter = None
    self.pushover = None
    self.telegram = None
    self.display = None

    self.set_profile_image(profile_image)
    if trafficlights is not None and len(trafficlights) == 3:
      self.set_notification_leds(trafficlights[0],trafficlights[1],trafficlights[2])

    self.__load_config()
    self.__load_messages()

  def __current_minute(self):
    # Get timestamp of current minute with 00 seconds.
    now = int(datetime.datetime.now().strftime('%s'))
    now -= now % 60
    return now

  def __ratelimit(self):
    now = str(self.__current_minute())
    total = 0
    for messageItem in sorted(self.__ratelimit_messages):
      for timestamp in sorted(self.__ratelimit_messages[messageItem],reverse=True):
        if timestamp == now:
          total += self.__ratelimit_messages[messageItem][timestamp]
        else:
          del(self.__ratelimit_messages[messageItem][timestamp])

    return total

  def __load_config(self):
    self.__data = configparser.ConfigParser()
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
      proxy = None
      if self.__data.has_option('telegram', 'proxy'):
        proxy = self.__data.get('telegram','proxy')

      self.set_telegram(self.__data.get('telegram','bot_token'),
                        self.__data.get('telegram','userid'),
                        proxy)

    if self.__data.has_section('display'):
      self.set_display(self.__data.get('display','address'),
                       self.__data.get('display','resolution'),
                       self.__data.get('display','title'))

  def __load_messages(self,data = None):
    self.messages = {}
    for message_id in self.__default_notifications:
      if self.__data.has_section('message' + message_id):
        self.messages[message_id] = terrariumNotificationMessage(message_id,
                                                                 self.__data.get('message' + message_id,'title').replace('%%','%'),
                                                                 self.__data.get('message' + message_id,'message').replace('%%','%'),
                                                                 self.__data.get('message' + message_id,'services').replace('%%','%'))
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
    data['now'] = datetime.datetime.now().strftime('%c')

    for dateitem in ['timer_min_lastaction','timer_max_lastaction','last_update']:
      if dateitem in data:
        data[dateitem] = datetime.datetime.fromtimestamp(int(data[dateitem])).strftime('%c')

    for item in terrariumNotification.__regex_parse.findall(message):
      if 'raw_data' == item:
        message = message.replace('%' + item + '%',str(data)
                                                    .replace(',',"\n")
                                                    .replace('{',' ')
                                                    .replace('}',''))
      elif item in data:
        message = message.replace('%' + item + '%',str(data[item]))

    return message.encode('utf8')

  def __update_config(self,section,data,exclude = []):
    if not self.__data.has_section(section):
      self.__data.add_section(section)

    keys = list(data.keys())
    keys.sort()
    for setting in keys:
      if setting in exclude:
        continue

      if type(data[setting]) is list:
        data[setting] = ','.join(data[setting])

      if isinstance(data[setting], str):
        try:
          data[setting] = data[setting].encode('utf-8').decode()
        except Exception as ex:
          # 'Not sure what to do... but it seams already utf-8...??'
          pass

      self.__data.set(section, str(setting), str(data[setting].replace('%','%%')))

  def stop(self):
    if self.telegram is not None:
      self.telegram.stop()

  def set_profile_image(self,imagefile):
    self.__profile_image = imagefile
    if self.__profile_image is None:
      return

    if imagefile[0] == '/':
      imagefile = imagefile[1:]

    if os.path.isfile(imagefile):
      self.__profile_image = imagefile
      self.update_twitter_profile_image()

  def set_notification_leds(self,green,orange,red):
    self.__notification_leds['info']['pin'] = terrariumUtils.to_BCM_port_number(green)
    self.__notification_leds['warning']['pin'] = terrariumUtils.to_BCM_port_number(orange)
    self.__notification_leds['error']['pin'] = terrariumUtils.to_BCM_port_number(red)

    # Initialize leds and run them all for 1 second to test
    GPIO.setmode(GPIO.BCM)
    for messagetype in ['info','warning','error']:
      lednr = self.__notification_leds[messagetype]['pin']
      if lednr is not None:
        GPIO.setup(lednr, GPIO.OUT)
        GPIO.output(lednr,1)
        sleep(1)
        GPIO.output(lednr,0)

  def send_notication_led(self,message_id):
    message_type = message_id.replace('system_','')
    now = int(time.time())
    if message_type in ['info','error','warning']:
      if self.__notification_leds[message_type]['pin'] is not None:
        GPIO.output(self.__notification_leds[message_type]['pin'],1)
        self.__notification_leds[message_type]['state'] = True
        self.__notification_leds[message_type]['lastaction'] = now

    for message_type in self.__notification_leds:
      if self.__notification_leds[message_type]['state'] and \
          ( ('warning' == message_type and now - self.__notification_leds[message_type]['lastaction'] > 10 * 60) or \
            ('error'   == message_type and now - self.__notification_leds[message_type]['lastaction'] > 30 * 60) ):

        GPIO.output(self.__notification_leds[message_type]['pin'],0)
        self.__notification_leds[message_type]['state'] = False
        self.__notification_leds[message_type]['lastaction'] = now

  def set_email(self,receiver,server,serverport = 25,username = None,password = None):
    if '' != receiver and '' != server:
      self.email = {'receiver'   : receiver.split(','),
                    'server'     : server,
                    'serverport' : serverport,
                    'username'   : username,
                    'password'   : password}

  def send_email(self,subject,message):
    if self.email is None:
      return

    mailserver = None
    try:
      mailserver = smtplib.SMTP(self.email['server'],self.email['serverport'],timeout=15)
    except Exception as ex:
      print(ex)
      try:
        mailserver = smtplib.SMTP_SSL(self.email['server'],self.email['serverport'],timeout=15)
      except Exception as ex:
        print(ex)
        print('%s - ERROR  - terrariumNotificatio - Mailserver is not reachable!' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23]))
        return

    if mailserver is None:
      print('%s - ERROR  - terrariumNotificatio - Mailserver is not reachable!' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23]))
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
      except Exception as ex:
        print(ex)
        print('%s - ERROR  - terrariumNotificatio - Mailserver login credentials are invalid. Cannot sent mail!' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23]))
        return

    htmlbody = '<html><head><title>%s</title></head><body>%s%s</body></html>'
    htmlimage = ''
    textimage = ''
    profile_image = None
    profile_image_cid = ''

    if self.__profile_image is not None:
      try:
        with open(self.__profile_image, 'rb') as imagefile:
          profile_image = imagefile.read()
          if sys.version_info.major == 2:
            filename, file_extension = os.path.splitext(self.__profile_image)
            profile_image = MIMEImage(profile_image,_subtype=file_extension.replace('.',''))
            profile_image_cid = '<profileimage>'
            profile_image.add_header('Content-ID', profile_image_cid)
            profile_image.add_header('Content-Disposition', 'inline', filename=os.path.basename(self.__profile_image))
          elif sys.version_info.major == 3:
            profile_image_cid = make_msgid()

          htmlimage = '<img src="cid:{profileimage}" alt="Profile image" title="Profile image" align="right" style="max-width:300px;border-radius:25%;">'
          textimage = '[cid:{profileimage}]\n'

      except Exception as ex:
        print('%s - ERROR  - terrariumNotificatio - %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],ex))
        # No images unfortunally...

    textmessage = (textimage + message.decode()).format(profileimage=profile_image_cid[1:-1])
    htmlmessage = (htmlbody % (subject.decode(),htmlimage,message.decode().replace('\n','<br />'))).format(profileimage=profile_image_cid[1:-1])
    for receiver in self.email['receiver']:
      if sys.version_info.major == 2:
        emailmessage = MIMEMultipart('mixed')
        emailmessagerelated = MIMEMultipart('related')
        emailmessagealternative = MIMEMultipart('alternative')

        emailmessage['Subject'] = subject.decode()
        emailmessage['From'] = receiver
        emailmessage['To'] = re.sub(r'(.*)@(.*)', '\\1+terrariumpi@\\2', receiver, 0, re.MULTILINE)

        emailmessagealternative.attach(MIMEText(textmessage, 'plain'))
        emailmessagealternative.attach(MIMEText(htmlmessage, 'html'))

        emailmessagerelated.attach(emailmessagealternative)

        if profile_image is not None:
          emailmessagerelated.attach(profile_image)

        emailmessage.attach(emailmessagerelated)

        try:
          mailserver.sendmail(receiver,re.sub(r'(.*)@(.*)', '\\1+terrariumpi@\\2', receiver, 0, re.MULTILINE),emailmessage.as_string())
        except Exception as ex:
          print(ex)

      elif sys.version_info.major == 3:
        emailmessage = EmailMessage()
        emailmessage['Subject'] = subject.decode()
        emailmessage['From'] = receiver
        emailmessage['To'] = re.sub(r'(.*)@(.*)', '\\1+terrariumpi@\\2', receiver, 0, re.MULTILINE)

        emailmessage.set_content(textmessage, subtype='text')
        emailmessage.add_alternative( htmlmessage, subtype='html')
        if profile_image is not None:
          emailmessage.get_payload()[1].add_related(profile_image, 'image', 'jpeg', cid=profile_image_cid)

        try:
          mailserver.send_message(emailmessage)
        except Exception as ex:
          print(ex)

    try:
      mailserver.quit()
    except Exception as ex:
      pass

  def set_twitter(self,consumer_key,consumer_secret,access_token,access_token_secret):
    if '' != consumer_key and '' != consumer_secret and '' != access_token and '' != access_token_secret:
      self.twitter = {'consumer_key'        : consumer_key,
                      'consumer_secret'     : consumer_secret,
                      'access_token'        : access_token,
                      'access_token_secret' : access_token_secret}

  def update_twitter_profile_image(self):
    if self.__profile_image is not None and self.twitter is not None:
      try:
        api = twitter.Api(consumer_key=self.twitter['consumer_key'],
                          consumer_secret=self.twitter['consumer_secret'],
                          access_token_key=self.twitter['access_token'],
                          access_token_secret=self.twitter['access_token_secret'])

        if api.VerifyCredentials() is not None:
          status = api.UpdateImage(self.__profile_image)

      except Exception as ex:
        print(ex)

  def send_tweet(self,message):
    if self.twitter is None:
      return

    try:
      api = twitter.Api(consumer_key=self.twitter['consumer_key'],
                        consumer_secret=self.twitter['consumer_secret'],
                        access_token_key=self.twitter['access_token'],
                        access_token_secret=self.twitter['access_token_secret'])

      if api.VerifyCredentials() is not None:
        status = api.PostUpdates(message)
        # [Status(ID=1003393079041314816, ScreenName=MadagascarGecko, Created=Sun Jun 03 21:48:46 +0000 2018, Text=u'Environment watertank sensors are not up to date. Check your sensors on the sensor page. So force the power down to be sure!')]
    except Exception as ex:
      print(ex)

  def set_pushover(self,api_token,user_key):
    if '' != api_token and '' != user_key:
      self.pushover = {'api_token' : api_token,
                       'user_key'  : user_key}

  def send_pushover(self,subject,message):
    if self.pushover is None:
      return

    try:
      client = pushover.Client(self.pushover['user_key'], api_token=self.pushover['api_token'])
      if client.verify():
        status = client.send_message(message, title=subject)
    except Exception as ex:
      print(ex)

  def set_telegram(self,bot_token,userid,proxy):
    if '' != bot_token and '' != userid:
      if self.telegram is None:
        self.telegram = terrariumNotificationTelegramBot(bot_token,userid,proxy)
      else:
        self.telegram.set_valid_users(userid)
        self.telegram.set_proxy(proxy)
        self.telegram.start()

  def send_telegram(self,subject,message):
    if self.telegram is None:
      return

    self.telegram.send_message(message)

  def set_display(self,address,resolution,title):
    self.display = None
    if address is not None and '' != address:
      self.display = terrariumDisplay(None,address,'notification',resolution,title)

      if self.__profile_image is not None:
        self.display.write_image(self.__profile_image)

  def send_display(self,messages):
    if self.display is not None:
      self.display.message(messages)

  def message(self,message_id,data = None):
    self.send_notication_led(message_id)

    if message_id not in self.messages or not self.messages[message_id].is_enabled():
      return

    now = str(self.__current_minute())
    title = self.__parse_message(self.messages[message_id].get_title(),data)
    message = self.__parse_message(self.messages[message_id].get_message(),data)

    if title not in self.__ratelimit_messages:
      self.__ratelimit_messages[title] = {}

    if now not in self.__ratelimit_messages[title]:
      self.__ratelimit_messages[title][now] = 0

    if self.__ratelimit_messages[title][now] > terrariumNotification.__MAX_MESSAGES_PER_MINUTE:
      print('%s - WARNING - terrariumNotificatio - Max messages per minute %s reached for \'%s\'' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],
                                                                                                 terrariumNotification.__MAX_MESSAGES_PER_MINUTE, title))
      return

    if self.__ratelimit() > terrariumNotification.__MAX_MESSAGES_TOTAL_PER_MINUTE:
      print('%s - WARNING - terrariumNotificatio - Max total messages per minute %s reached' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],
                                                                                                terrariumNotification.__MAX_MESSAGES_TOTAL_PER_MINUTE))
      return

    self.__ratelimit_messages[title][now] += 1

    if self.messages[message_id].is_email_enabled():
      self.send_email(title,message)

    if self.messages[message_id].is_twitter_enabled():
      self.send_tweet(message)

    if self.messages[message_id].is_pushover_enabled():
      self.send_pushover(title,message)

    if self.messages[message_id].is_telegram_enabled():
      self.send_telegram(title,message)

    if self.messages[message_id].is_display_enabled():
      self.send_display(message)

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
                                       'userid'    : data['telegram_userid'],
                                       'proxy'     : data['telegram_proxy']})

      self.__update_config('display',{'address'    : data['display_address'],
                                      'resolution' : data['display_resolution'],
                                      'title'      : data['display_title']})

    except Exception as ex:
      print(ex)

    for message_id in data:
      message_id = message_id[:-8]
      if message_id in self.messages:
        self.messages[message_id] = terrariumNotificationMessage(message_id,
                                                                 data[message_id + '_title'],
                                                                 data[message_id + '_message'],
                                                                 data[message_id + '_services'])

        self.__data.remove_section('message' + message_id)
        self.__update_config('message' + message_id,{'id'       : message_id,
                                                     'title'    : data[message_id + '_title'],
                                                     'message'  : data[message_id + '_message'],
                                                     'services' : data[message_id + '_services']})

    with open('notifications.cfg', 'w') as configfile:
      self.__data.write(configfile)

    self.__load_config()
    self.__load_messages()
    return True

  def get_config(self):
    data = {
      'email'    : dict(self.email) if self.email is not None else {},
      'display'  : self.display.get_config() if self.display is not None else {},
      'twitter'  : dict(self.twitter) if self.twitter is not None else {},
      'pushover' : dict(self.pushover) if self.pushover is not None else {},
      'telegram' : self.telegram.get_config() if self.telegram is not None else {},
      'messages' : self.get_messages() }

    if self.email is not None:
      data['email']['receiver'] = ','.join(data['email']['receiver'])

    return data
