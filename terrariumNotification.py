# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import gettext
gettext.install('terrariumpi', 'locales/', unicode=True)

import re
import ConfigParser
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from terrariumUtils import terrariumUtils


class terrariumNotificationMessage(object):

  def __init__(self,message_id, title, message, enabled = False):
    self.enabled = enabled
    self.id = message_id
    self.title = title
    self.message = message


  def get_id(self):
    return self.id

  def get_title(self):
    return self.title

  def get_message(self):
    return self.message

  def is_enabled(self):
    return self.enabled == True

  def get_data(self):
    return {'id':self.get_id(),
            'title':self.get_title(),
            'message':self.get_message(),
            'enabled':self.is_enabled(),
            }

class terrariumNotification(object):
  __regex_parse = re.compile(r"%(?P<index>[^%]+)%")

  __default_notifications = {
    'environment_light_alarm_low_on' : terrariumNotificationMessage('environment_light_alarm_low_on',_('Environment light day on'),'Lights when on at %config_timer_start%\n\n%raw_data%.'),
    'environment_light_alarm_low_off' : terrariumNotificationMessage('environment_light_alarm_low_off',_('Environment light day off'),'Lights when off at %off_time%'),
    'environment_light_alarm_high_on' : terrariumNotificationMessage('environment_light_alarm_high_on',_('Environment light night on'),'Lights when on at %on_time%'),
    'environment_light_alarm_high_off' : terrariumNotificationMessage('environment_light_alarm_high_off',_('Environment light night off'),'Lights when off at %off_time%'),

    'environment_temperature_alarm_low_on' : terrariumNotificationMessage('environment_temperature_alarm_low_on',_('Environment temperature alarm_low on'),'Lights when on at %on_time%'),
    'environment_temperature_alarm_low_off' : terrariumNotificationMessage('environment_temperature_alarm_low_off',_('Environment temperature alarm_low off'),'Lights when off at %off_time%'),
    'environment_temperature_alarm_high_on' : terrariumNotificationMessage('environment_temperature_alarm_high_on',_('Environment temperature alarm_high on'),'Lights when on at %on_time%'),
    'environment_temperature_alarm_high_off' : terrariumNotificationMessage('environment_temperature_alarm_high_off',_('Environment temperature alarm_high off'),'Lights when off at %off_time%')

  }

  def __init__(self):
    self.__data = ConfigParser.SafeConfigParser()
    self.__data.read('notifications.cfg')

    self.email = None

    self.set_email('test@theyosh.nl','mail.theyosh.nl')
    self.__load_messages()

    #self.message('environment_light_night_on')

  def __load_messages(self,data = None):
    self.messages = {}
    for message_id in self.__default_notifications:
      if self.__data.has_section('message_' + message_id):
        self.messages[message_id] = terrariumNotificationMessage(message_id,
                                                                 self.__data.get('message_' + message_id,'title'),
                                                                 self.__data.get('message_' + message_id,'message'),
                                                                 self.__data.getboolean('message_' + message_id,'enabled'))
      else:
        self.messages[message_id] = self.__default_notifications[message_id]

  def set_email(self,receiver,server,serverport = 25,username = None,password = None):
    self.email = {'receiver'   : receiver,
                  'server'     : server,
                  'serverport' : serverport,
                  'username'   : username,
                  'password'   : password}

  def send_email(self,subject,message):
    msg = MIMEMultipart()
    msg['From'] = 'terrariumpi+' + self.email['receiver']
    msg['To'] = self.email['receiver']
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP(self.email['server'],self.email['serverport'])
    mailserver.ehlo()
    try:
      mailserver.starttls()
      mailserver.ehlo()
    except:
      pass

    if self.email['username'] is not None and self.email['password'] is not None:
      mailserver.login(self.email['username'], self.email['password'])

    mailserver.sendmail('terrariumpi+' + self.email['receiver'],self.email['receiver'],msg.as_string())
    mailserver.quit()

  def message(self,message_id,data = None):
    if message_id not in self.messages:
      return

    message = self.messages[message_id].get_message()
    if data is not None:
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
      for item in terrariumNotification.__regex_parse.findall(self.messages[message_id].get_message()):
        if 'raw_data' == item:
          message = message.replace('%' + item + '%',str(data).replace(',',"\n").replace('{',' ').replace('}',''))
        elif item in data:
          message = message.replace('%' + item + '%',data[item])

    if self.email is not None:
      self.send_email(self.messages[message_id].get_title(),message)

  def get_messages(self):
    data = []
    for message_id in self.messages:
      data.append(self.messages[message_id].get_data())

    return data





























