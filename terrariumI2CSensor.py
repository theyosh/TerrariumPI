# -*- coding: utf-8 -*-
# Sources: https://github.com/iotify/custom-lab/blob/master/sht2x.py

import smbus
import time

class terrariumI2CSensor():
  # control constants
  __SOFTRESET = 0xFE
  __SOFTRESET_TIMEOUT = 0.1

  __TRIGGER_TEMPERATURE_NO_HOLD = 0xF3
  __TRIGGER_HUMIDITY_NO_HOLD = 0xF5

  __TEMPERATURE_WAIT_TIME = 0.1
  __HUMIDITY_WAIT_TIME = 0.1

  sensortype = None

  def __init__(self, device_number=1, address=0x40):
    self.__bus = smbus.SMBus(device_number)
    self.__address = address
    #Datasheet recommend do Soft Reset before measurment, ok:
    self.__bus.write_byte(self.__address, self.__SOFTRESET)
    time.sleep(self.__SOFTRESET_TIMEOUT)

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def __get_raw_data(self,trigger,timeout):
    self.__bus.write_byte(self.__address, trigger)
    time.sleep(timeout)
    data1 = self.__bus.read_byte(self.__address)
    try:
      data2 = self.__bus.read_byte(self.__address)
    except Exception, ex:
      print ex
      data2 = data1

    return (data1,data2)

  def close(self):
    """Closes the i2c connection"""
    self.__bus.close()

  def read_temperature(self):
    #From datasheet convert this in human view. Temp C = ((Temp_Code*175.72)/65536)-46.85 / T = -46.82 + (172.72 * (ST/2^16))
    #For convert 2 byte in number need MSB*256+LSB.
    bytedata = self.__get_raw_data(self.__TRIGGER_TEMPERATURE_NO_HOLD,self.__TEMPERATURE_WAIT_TIME)
    return ((bytedata[0]*256.0+bytedata[1])*175.72/65536.0)-46.85

  def read_humidity(self):
    #From datasheet convert this in human view. RH% = ((RH*125)/65536)-6 / RH = -6 + (125 * (SRH / 2 ^16))
    #For convert 2 byte in number need MSB*256+LSB.
    bytedata = self.__get_raw_data(self.__TRIGGER_HUMIDITY_NO_HOLD,self.__HUMIDITY_WAIT_TIME)
    return ((bytedata[0]*256.0+bytedata[1])*125.0/65536.0)-6.0

class terrariumSHT2XSensor(terrariumI2CSensor):
  # SHT2XX - 3.3 Volt VCC
  # 黄 = Yellow = DATA
  # 蓝 = Blue   = CLK
  # 黑 = Black  = GND
  # 棕 = Brown  = VCC

  sensortype = 'sht2x'
  # datasheet (v4), page 9, table 7, thanks to Martin Milata
  # for suggesting the use of these better values
  # code copied from https://github.com/mmilata/growd
  # http://www.farnell.com/datasheets/1780639.pdf
  # https://cdn-shop.adafruit.com/datasheets/Sensirion_Humidity_SHT1x_Datasheet_V5.pdf
  __TEMPERATURE_WAIT_TIME = 0.086  # (datasheet: typ=66, max=85 in ms)
  __HUMIDITY_WAIT_TIME = 0.030     # (datasheet: typ=22, max=29 in ms)

class terrariumHTU21DSensor(terrariumI2CSensor):
  sensortype = 'htu21d'
  # Datasheet - https://datasheet.octopart.com/HPP845E131R5-TE-Connectivity-datasheet-15137552.pdf
  __TEMPERATURE_WAIT_TIME = 0.059  # (datasheet: typ=44, max=58 in ms)
  __HUMIDITY_WAIT_TIME = 0.019     # (datasheet: typ=14, max=18 in ms)

class terrariumSi7021Sensor(terrariumI2CSensor):
  sensortype = 'si7021'
  # Datasheet - https://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf
  __TEMPERATURE_WAIT_TIME = 0.012  # (datasheet: typ=7, max=10.8 in ms)
  __HUMIDITY_WAIT_TIME = 0.013     # (datasheet: typ=10, max=12 in ms)
  __SOFTRESET_TIMEOUT = 0.016      # (datasheet: typ=5, max=15 in ms)
