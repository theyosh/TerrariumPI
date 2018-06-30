# -*- coding: utf-8 -*-
import re
import datetime
import ConfigParser
import RPi.GPIO as GPIO
import time
import os
import os.path
import thread
import json
import requests
import urllib

# Email support
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

# Twitter support
import twitter

# Pushover support
import pushover

from terrariumUtils import terrariumUtils, terrariumSingleton
from terrariumLCD import terrariumLCD

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

  def is_lcd_enabled(self):
    return self.message != '' and 'lcd' in self.services

  def get_data(self):
    return {'id':self.get_id(),
            'title':self.get_title(),
            'message':self.get_message(),
            'enabled':self.is_enabled(),
            'services' : ','.join(self.services)
            }

class terrariumNotificationTelegramBot(object):
  __metaclass__ = terrariumSingleton

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
      text = urllib.quote_plus(text)
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
      thread.start_new_thread(self.__run, ())

  def stop(self):
    self.__running = False
    print '%s - INFO    - terrariumNotificatio - Stopping TelegramBot. This can take up to %s seconds...' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],(terrariumNotificationTelegramBot.__POLL_TIMEOUT - (int(time.time()) - self.__last_update_check)))

  def __run(self):
    self.__running = True
    last_update_id = None

    error_counter = 0
    while self.__running and error_counter < 2:
      try:
        updates = self.__get_updates(last_update_id)
        if 'result' in updates and len(updates['result']) > 0:
          last_update_id = max([int(update['update_id']) for update in updates['result']]) + 1
          self.__process_messages(updates['result'])
          if error_counter > 0:
            error_counter -= 1

        elif 'description' in updates:
          error_counter += 1
          print '%s - ERROR  - terrariumNotificatio - TelegramBot has issues: %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],updates['description'])
          sleep(5)

        sleep(0.5)
      except Exception, ex:
        error_counter += 1
        print ex
        sleep(5)

    self.__running = False
    print '%s - INFO    - terrariumNotificatio - TelegramBot is stopped' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],)

class terrariumNotification(object):
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
    self.lcd = None

    self.__load_config()
    self.__load_messages()

    if trafficlights is not None and len(trafficlights) == 3:
      self.set_notification_leds(trafficlights[0],trafficlights[1],trafficlights[2])

    self.set_profile_image(profile_image)

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
      proxy = None
      if self.__data.has_option('telegram', 'proxy'):
        proxy = self.__data.get('telegram','proxy')

      self.set_telegram(self.__data.get('telegram','bot_token'),
                        self.__data.get('telegram','userid'),
                        proxy)

    if self.__data.has_section('lcd'):
      self.set_lcd(self.__data.get('lcd','address'),
                   self.__data.get('lcd','resolution'),
                   self.__data.get('lcd','title'))

  def __load_messages(self,data = None):
    self.messages = {}
    for message_id in self.__default_notifications:
      if self.__data.has_section('message' + message_id):
        self.messages[message_id] = terrariumNotificationMessage(message_id,
                                                                 self.__data.get('message' + message_id,'title'),
                                                                 self.__data.get('message' + message_id,'message'),
                                                                 self.__data.get('message' + message_id,'services'))
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
          # 'Not sure what to do... but it seams already utf-8...??'
          pass

      self.__data.set(section, str(setting), str(data[setting]))

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
        time.sleep(1)
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
    except Exception, ex:
      print ex
      try:
        mailserver = smtplib.SMTP_SSL(self.email['server'],self.email['serverport'],timeout=15)
      except Exception, ex:
        print ex
        print '%s - ERROR  - terrariumNotificatio - Mailserver is not reachable!' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23])
        return

    if mailserver is None:
      print '%s - ERROR  - terrariumNotificatio - Mailserver is not reachable!' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23])
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
        print '%s - ERROR  - terrariumNotificatio - Mailserver login credentials are invalid. Cannot sent mail!' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23])
        return

    htmlbody = '<html><head><title>%s</title></head><body>%s%s</body></html>'
    htmlimage = ''
    textimage = ''
    msgImage = None

    if self.__profile_image is not None:
      try:
        with open(self.__profile_image, 'rb') as fp:
          filename, file_extension = os.path.splitext(self.__profile_image)
          msgImage = MIMEImage(fp.read(), filename=os.path.basename(self.__profile_image),_subtype=file_extension.replace('.',''))
          msgImage.add_header('Content-ID', 'profileimage')
          msgImage.add_header('Content-Disposition', 'inline', filename=os.path.basename(self.__profile_image))

          htmlimage = '<img src="cid:profileimage" alt="Profile image" title="Profile image" align="right" style="max-width:300px;border-radius:25%;">'
          textimage = '[cid:profileimage]\n'
      except Exception, ex:
        print '%s - ERROR  - terrariumNotificatio - %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],ex)
        # No images unfortunally...

    for receiver in self.email['receiver']:

      emailMessage = MIMEMultipart('mixed')
      emailMessageRelated = MIMEMultipart('related')
      emailMessageAlternative = MIMEMultipart('alternative')

      emailMessage['From'] = receiver
      emailMessage['To'] = re.sub(r'(.*)@(.*)', '\\1+terrariumpi@\\2', receiver, 0, re.MULTILINE)
      emailMessage['Subject'] = subject

      emailMessageAlternative.attach(MIMEText(textimage.encode('utf8') + message, 'plain'))
      emailMessageAlternative.attach(MIMEText(htmlbody.encode('utf8') % (subject,htmlimage,message.replace('\n','<br />')), 'html'))

      emailMessageRelated.attach(emailMessageAlternative)

      if msgImage is not None:
        emailMessageRelated.attach(msgImage)

      emailMessage.attach(emailMessageRelated)

      try:
        mailserver.sendmail(receiver,re.sub(r'(.*)@(.*)', '\\1+terrariumpi@\\2', receiver, 0, re.MULTILINE),emailMessage.as_string())
      except Exception, ex:
        print ex

    mailserver.quit()

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

      except Exception, ex:
        print ex

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
    except Exception, ex:
      print ex

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
    except Exception, ex:
      print ex

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

  def set_lcd(self,address,resolution,title):
    if address is not None and '' != address:
      if self.lcd is None:
        self.lcd = terrariumLCD(address,resolution,title)
      else:
        self.lcd.set_address(address)
        self.lcd.set_resolution(resolution)
        self.lcd.set_title(title)

  def send_lcd(self,messages):
    if self.lcd is not None:
      self.lcd.message(messages)

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
      print '%s - WARNING - terrariumNotificatio - Max messages per minute %s reached for \'%s\'' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],
                                                                                                 terrariumNotification.__MAX_MESSAGES_PER_MINUTE, title)
      return

    if self.__ratelimit() > terrariumNotification.__MAX_MESSAGES_TOTAL_PER_MINUTE:
      print '%s - WARNING - terrariumNotificatio - Max total messages per minute %s reached' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:23],
                                                                                                terrariumNotification.__MAX_MESSAGES_TOTAL_PER_MINUTE)
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

    if self.messages[message_id].is_lcd_enabled():
      self.send_lcd(message)

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

      self.__update_config('lcd',{'address'    : data['lcd_address'],
                                  'resolution' : data['lcd_resolution'],
                                  'title'      : data['lcd_title']})

    except Exception, ex:
      print ex

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

    with open('notifications.cfg', 'wb') as configfile:
      self.__data.write(configfile)

    self.__load_config()
    self.__load_messages()
    return True

  def get_config(self):
    data = {
      'email'    : dict(self.email) if self.email is not None else {},
      'lcd'      : self.lcd.get_config() if self.lcd is not None else {},
      'twitter'  : dict(self.twitter) if self.twitter is not None else {},
      'pushover' : dict(self.pushover) if self.pushover is not None else {},
      'telegram' : self.telegram.get_config() if self.telegram is not None else {},
      'messages' : self.get_messages() }

    if self.email is not None:
      data['email']['receiver'] = ','.join(data['email']['receiver'])

    return data
