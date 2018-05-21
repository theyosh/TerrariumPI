# -*- coding: utf-8 -*-
import re
import datetime
import requests

class terrariumUtils():

  @staticmethod
  def to_fahrenheit(value):
    return float(9.0 / 5.0 * value + 32.0)

  @staticmethod
  def to_celsius(value):
    return float((value - 32) * 5.0 / 9.0)

  @staticmethod
  def to_inches(value):
    # https://www.convertunits.com/from/cm/to/inches , http://www.manuelsweb.com/in_cm.htm
    # Input value is in cm
    return (39.370078740157 / 100.0) * float(value)

  @staticmethod
  def is_float(value):
    if value is None:
      return False

    try:
      float(value)
      return True
    except ValueError:
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

    index = 'gpio' + str(value)
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

    index = 'BCM' + str(value)
    if index in pinout:
      return pinout[index]

    return False

  @staticmethod
  def parse_url(url):
    url = url.strip()
    if '' == url:
      return False

    regex = ur"^((?P<scheme>https?|ftp):\/)?\/?((?P<username>.*?)(:(?P<password>.*?)|)@)?(?P<hostname>[^:\/\s]+)(:(?P<port>(\d*))?)?(?P<path>(\/\w+)*\/)(?P<filename>[-\w.]+[^#?\s]*)?(?P<query>\?([^#]*))?(#(?P<fragment>(.*))?)?$"
    matches = re.search(regex, url)
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
      except Exception, err:
        print 'Error in terrariumUtils.parse_time'
        print err

    return time

  @staticmethod
  def get_remote_data(url):
    data = None
    try:
      url_data = terrariumUtils.parse_url(url)
      data = requests.get(url,auth=(url_data['username'],url_data['password']),timeout=3)

      if data.status_code == 200:
        data = data.json()
        json_path = url_data['fragment'].split('/') if 'fragment' in url_data and url_data['fragment'] is not None else []

        for item in json_path:
          # Dirty hack to process array data....
          try:
            item = int(item)
          except Exception, ex:
            item = str(item)

          data = data[item]
      else:
        data = None

    except Exception, ex:
      print ex

    return data

  @staticmethod
  def calculate_time_table(start, stop, on_duration = None, off_duration = None):
    timer_time_table = []

    now = datetime.datetime.now()
    starttime = start.split(':')
    starttime = now.replace(hour=int(starttime[0]), minute=int(starttime[1]))

    stoptime = stop.split(':')
    stoptime = now.replace(hour=int(stoptime[0]), minute=int(stoptime[1]))

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

    if on_duration is None and off_duration is None:
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
      if time_schedule[0] < now < time_schedule[1]:
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
             for kk, vv in dd.items()
             for k, v in terrariumUtils.flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd if not isinstance(dd,list) else  ','.join(dd)}
