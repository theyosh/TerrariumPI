# -*- coding: utf-8 -*-

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
