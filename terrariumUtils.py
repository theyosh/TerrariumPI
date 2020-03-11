# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import re
import datetime
import requests
import subprocess

from math import log
from time import time

# works in Python 2 & 3
class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}
    def __call__(cls, *args, **kwargs):
      if cls not in cls._instances:
        cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
      return cls._instances[cls]

class terrariumSingleton(_Singleton('terrariumSingletonMeta', (object,), {})): pass

class terrariumTimer(object):
  def __init__(self,start,stop,on_duration,off_duration,enabled):
    self.__start = start
    self.__stop = stop
    self.__on_duration = on_duration
    self.__off_duration = off_duration

    self.__enabled = terrariumUtils.is_true(enabled)

    self.__timer_table = []
    self.__calculate_time_table()

  def __calculate_time_table(self):
    starttime = self.__start.split(':')
    stoptime = self.__stop.split(':')
    on_duration = float(self.__on_duration) * 60.0
    off_duration = float(self.__off_duration) * 60.0

    self.__timer_table = []
    now = datetime.datetime.now()
    starttime = now.replace(hour=int(starttime[0]), minute=int(starttime[1]), second=0)
    stoptime = now.replace(hour=int(stoptime[0]), minute=int(stoptime[1]),second=0)

    if starttime == stoptime:
      stoptime += datetime.timedelta(hours=24)

    elif starttime > stoptime:
      if now > stoptime:
        stoptime += datetime.timedelta(hours=24)
      else:
        starttime -= datetime.timedelta(hours=24)

    # Calculate next day when current day is done...
    if now > stoptime:
      starttime += datetime.timedelta(hours=24)
      stoptime += datetime.timedelta(hours=24)

    if (on_duration is None and off_duration is None) or (0 == on_duration and 0 == off_duration):
      # Only start and stop time. No periods
      self.__timer_table.append((int(starttime.strftime('%s')),int(stoptime.strftime('%s'))))
    elif on_duration is not None and off_duration is None:

      if (starttime + datetime.timedelta(seconds=on_duration)) > stoptime:
        on_duration = (stoptime - starttime).total_seconds()
      self.__timer_table.append((int(starttime.strftime('%s')),int((starttime + datetime.timedelta(seconds=on_duration)).strftime('%s'))))
    else:
      # Create time periods based on both duration between start and stop time
      while starttime < stoptime:
        if (starttime + datetime.timedelta(seconds=on_duration)) > stoptime:
          on_duration = (stoptime - starttime).total_seconds()

        self.__timer_table.append((int(starttime.strftime('%s')),int((starttime + datetime.timedelta(seconds=on_duration)).strftime('%s'))))
        starttime += datetime.timedelta(seconds=on_duration + off_duration)

  def is_enabled(self):
    return terrariumUtils.is_true(self.__enabled)

  def is_time(self):
    now = int(datetime.datetime.now().strftime('%s'))
    for time_schedule in self.__timer_table:
      if time_schedule[0] <= now < time_schedule[1]:
        return True

      elif now < time_schedule[0]:
        return False

    #End of time_table. No data to decide for today
    self.__calculate_time_table()
    return None

  def duration(time_table):
    duration = 0
    for time_schedule in self.__timer_table:
      duration += time_schedule[1] - time_schedule[0]

    return duration

  def get_data(self):
    return {'timer_enabled': self.is_enabled(),
            'timer_start': self.__start,
            'timer_stop' : self.__stop,
            'timer_on_duration': self.__on_duration,
            'timer_off_duration': self.__off_duration}

class terrariumCache(terrariumSingleton):
  def __init__(self):
    self.__cache = {}
    self.__running = {}
    logger.debug('Initialized cache')

  def set_data(self,hash_key,data,cache_timeout = 30):
    self.__cache[hash_key] = { 'data' : data, 'expire' : int(time()) + cache_timeout}
    logger.debug('Added new cache data with hash: {}. Total in cache: {}'.format(hash_key,len(self.__cache)))

  def get_data(self,hash_key):
    if hash in self.__cache and self.__cache[hash_key]['expire'] > int(time()):
      return self.__cache[hash_key]['data']

  def clear_data(self,hash_key):
    if hash_key in self.__cache:
      del(self.__cache[hash_key])

  def is_running(self,hash_key):
    if hash_key in self.__running:
      return True

    return False

  def set_running(self,hash_key):
    self.__running[hash_key] = True

  def clear_running(self,hash_key):
    del(self.__running[hash_key])

class terrariumUtils():

  @staticmethod
  def to_fahrenheit(value):
    return 9.0 / 5.0 * float(value) + 32.0

  @staticmethod
  def to_celsius(value):
    return (float(value) - 32) * 5.0 / 9.0

  @staticmethod
  def to_kelvin(value):
    return float(value) + 273.15

  @staticmethod
  def to_inches(value):
    # https://www.convertunits.com/from/cm/to/inches , http://www.manuelsweb.com/in_cm.htm
    # Input value is in cm
    return (39.370078740157 / 100.0) * float(value)

  @staticmethod
  def to_us_gallons(value):
    # https://www.asknumbers.com/gallons-to-liters.aspx
    return float(value) / 3.7854118

  @staticmethod
  def to_uk_gallons(value):
    # https://www.asknumbers.com/gallons-to-liters.aspx
    return float(value) / 4.54609

  @staticmethod
  def conver_to_value(current,indicator):
    if not terrariumUtils.is_float(current):
      return None

    indicator = indicator.lower()
    if 'f' == indicator:
      current = terrariumUtils.to_fahrenheit(current)
    elif 'k' == indicator:
      current = terrariumUtils.to_kelvin(current)
    elif 'inch' == indicator:
      current = terrariumUtils.to_inches(current)
    elif 'usgall' == indicator:
      current = terrariumUtils.to_us_gallons(current)
    elif 'ukgall' == indicator:
      current = terrariumUtils.to_uk_gallons(current)

    return float(current)

  @staticmethod
  def convert_from_to(current, indicator_from, indicator_to):
    indicator_from = indicator_from.lower()
    indicator_to = indicator_to.lower()

    if 'c' == indicator_from:
      pass # Nothing to do
    elif 'f' == indicator_from:
      current = terrariumUtils.to_celsius(current)

    if 'c' == indicator_to:
      pass # Nothing to do
    if 'f' == indicator_to:
      current = terrariumUtils.to_fahrenheit(current)

    return current

  @staticmethod
  def is_float(value):
    if value is None or '' == value:
      return False

    try:
      float(value)
      return True
    except Exception:
      return False

  @staticmethod
  def is_true(value):
    return value in [True,'True','true','1',1,'ON','On','on','YES','Yes','yes']

  @staticmethod
  def to_BCM_port_number(value):
    pinout = {'gpio3'  : 2,
              'gpio5'  : 3,
              'gpio7'  : 4,
              'gpio8'  : 14,
              'gpio10' : 15,
              'gpio11' : 17,
              'gpio12' : 18,
              'gpio13' : 27,
              'gpio15' : 22,
              'gpio16' : 23,
              'gpio18' : 24,
              'gpio19' : 10,
              'gpio21' : 9,
              'gpio22' : 25,
              'gpio23' : 11,
              'gpio24' : 8,
              'gpio26' : 7,
              'gpio27' : 0,
              'gpio28' : 1,
              'gpio29' : 5,
              'gpio31' : 6,
              'gpio32' : 12,
              'gpio33' : 13,
              'gpio35' : 19,
              'gpio36' : 16,
              'gpio37' : 26,
              'gpio38' : 20,
              'gpio40' : 21
              }

    index = 'gpio' + str(value).strip()
    if index in pinout:
      return pinout[index]

    return False

  @staticmethod
  def to_BOARD_port_number(value):
    pinout = {'BCM2'  : 3,
              'BCM3'  : 5,
              'BCM4'  : 7,
              'BCM14' : 8,
              'BCM15' : 10,
              'BCM17' : 11,
              'BCM18' : 12,
              'BCM27' : 13,
              'BCM22' : 15,
              'BCM23' : 16,
              'BCM24' : 18,
              'BCM10' : 19,
              'BCM9'  : 21,
              'BCM25' : 22,
              'BCM11' : 23,
              'BCM8'  : 24,
              'BCM7'  : 26,
              'BCM0'  : 27,
              'BCM1'  : 28,
              'BCM5'  : 29,
              'BCM6'  : 31,
              'BCM12' : 32,
              'BCM13' : 33,
              'BCM19' : 35,
              'BCM16' : 36,
              'BCM26' : 37,
              'BCM20' : 38,
              'BCM21' : 40
              }

    index = 'BCM' + str(value).strip()
    if index in pinout:
      return pinout[index]

    return False

  @staticmethod
  def parse_url(url):
    if url is None or '' == url.strip():
      return False

    regex = r"^((?P<scheme>https?|ftp):\/)?\/?((?P<username>.*?)(:(?P<password>.*?)|)@)?(?P<hostname>[^:\/\s]+)(:(?P<port>(\d*))?)?(?P<path>(\/\w+)*\/)(?P<filename>[-\w.]+[^#?\s]*)?(?P<query>\?([^#]*))?(#(?P<fragment>(.*))?)?$"
    matches = re.search(regex, url.strip())
    if matches:
      return matches.groupdict()

    return False

  @staticmethod
  def parse_time(value):
    time = None
    if ':' in value:
      try:
        value = value.split(':')
        time = "{:0>2}:{:0>2}".format(int(value[0])%24,int(value[1])%60)
      except Exception as ex:
        logger.exception('Error parsing time value %s. Exception %s' % (value, ex))

    return time

  @staticmethod
  def get_remote_data(url, timeout = 3, proxy = None, json = False):
    data = None
    try:
      url_data = terrariumUtils.parse_url(url)
      proxies = {'http' : proxy, 'https' : proxy}
      headers = {}
      if json:
        headers['Accept'] = 'application/json'

      if url_data['username'] is None:
        response = requests.get(url,headers=headers,timeout=timeout,proxies=proxies,stream=True)
      else:
        response = requests.get(url,auth=(url_data['username'],url_data['password']),headers=headers,timeout=timeout,proxies=proxies,stream=True)

      if response.status_code == 200:
        if 'multipart/x-mixed-replace' in response.headers['content-type']:
          # Motion JPEG stream....
          # https://stackoverflow.com/a/36675148
          frame = bytes()
          for chunk in response.iter_content(chunk_size=1024):
            frame += chunk
            a = frame.find(b'\xff\xd8')
            b = frame.find(b'\xff\xd9')
            if a != -1 and b != -1:
              return frame[a:b+2]

        elif 'application/json' in response.headers['content-type']:
          data = response.json()
          json_path = url_data['fragment'].split('/') if 'fragment' in url_data and url_data['fragment'] is not None else []
          for item in json_path:
            # Dirty hack to process array data....
            try:
              item = int(item)
            except Exception as ex:
              item = str(item)

            data = data[item]
        elif 'text' in response.headers['content-type']:
          data = response.text
        else:
          data = response.content

      else:
        data = None

    except Exception as ex:
      print(ex)
      logger.exception('Error parsing remote data at url %s. Exception %s' % (url, ex))

    return data

  @staticmethod
  def get_script_data(script):
    data = None
    try:
      logger.info('Running script: %s.' % (script))
      data = subprocess.check_output(script, shell=True)
      logger.info('Output was: %s.' % (data))
    except Exception as ex:
      print(ex)
      logger.exception('Error parsing script data for script %s. Exception %s' % (script, ex))

    return data

  @staticmethod
  def calculate_time_table(start, stop, on_duration = None, off_duration = None):
    timer_time_table = []

    now = datetime.datetime.now()
    starttime = start.split(':')
    starttime = now.replace(hour=int(starttime[0]), minute=int(starttime[1]), second=0)

    stoptime = stop.split(':')
    stoptime = now.replace(hour=int(stoptime[0]), minute=int(stoptime[1]),second=0)

    if starttime == stoptime:
      stoptime += datetime.timedelta(hours=24)

    elif starttime > stoptime:
      if now > stoptime:
        stoptime += datetime.timedelta(hours=24)
      else:
        starttime -= datetime.timedelta(hours=24)

    # Calculate next day when current day is done...
    if now > stoptime:
      starttime += datetime.timedelta(hours=24)
      stoptime += datetime.timedelta(hours=24)

    if (on_duration is None and off_duration is None) or (0 == on_duration and 0 == off_duration):
      # Only start and stop time. No periods
      timer_time_table.append((int(starttime.strftime('%s')),int(stoptime.strftime('%s'))))
    elif on_duration is not None and off_duration is None:

      if (starttime + datetime.timedelta(minutes=on_duration)) > stoptime:
        on_duration = (stoptime - starttime).total_seconds() / 60
      timer_time_table.append((int(starttime.strftime('%s')),int((starttime + datetime.timedelta(minutes=on_duration)).strftime('%s'))))
    else:
      # Create time periods based on both duration between start and stop time
      while starttime < stoptime:
        if (starttime + datetime.timedelta(minutes=on_duration)) > stoptime:
          on_duration = (stoptime - starttime).total_seconds() / 60

        timer_time_table.append((int(starttime.strftime('%s')),int((starttime + datetime.timedelta(minutes=on_duration)).strftime('%s'))))
        starttime += datetime.timedelta(minutes=on_duration + off_duration)

    return timer_time_table

  @staticmethod
  def is_time(time_table):
    now = int(datetime.datetime.now().strftime('%s'))
    for time_schedule in time_table:
      if time_schedule[0] <= now < time_schedule[1]:
        return True

      elif now < time_schedule[0]:
        return False

    #End of time_table. No data to decide for today
    return None

  @staticmethod
  def duration(time_table):
    duration = 0
    for time_schedule in time_table:
      duration += time_schedule[1] - time_schedule[0]

    return duration

  @staticmethod
  # https://stackoverflow.com/a/19647596
  def flatten_dict(dd, separator='_', prefix=''):
    return { prefix + separator + k if prefix else k : v
             for kk, vv in list(dd.items())
             for k, v in list(terrariumUtils.flatten_dict(vv, separator, kk).items())
             } if isinstance(dd, dict) else { prefix : dd if not isinstance(dd,list) else ','.join(dd)}

  @staticmethod
  def format_uptime(value):
    return str(datetime.timedelta(seconds=int(value)))

  @staticmethod
  def format_filesize(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)
