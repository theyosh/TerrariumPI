# -*- coding: utf-8 -*-
import re
import datetime

class terrariumUtils():

  @staticmethod
  def to_fahrenheit(value):
    return float(9.0 / 5.0 * value + 32.0)

  @staticmethod
  def to_celsius(value):
    return float((value - 32) * 5.0 / 9.0)

  @staticmethod
  def is_float(value):
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
  def calculate_time_table(start, stop, on_duration = None, off_duration = None):
    timer_time_table = []

    now = datetime.datetime.today()
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

    if on_duration is None and off_duration is None:
      timer_time_table.append((starttime,stoptime))
    elif on_duration is not None and off_duration is None:
      timer_time_table.append((starttime,starttime + datetime.timedelta(minutes=on_duration)))
    else:
      while starttime <= stoptime:
        timer_time_table.append((starttime,starttime + datetime.timedelta(minutes=on_duration)))
        starttime += datetime.timedelta(minutes=on_duration + off_duration)

    return timer_time_table
