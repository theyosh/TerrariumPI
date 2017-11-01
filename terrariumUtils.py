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
