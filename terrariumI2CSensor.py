# -*- coding: utf-8 -*-
# Sources: https://github.com/iotify/custom-lab/blob/master/sht2x.py
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import smbus
import sys
from terrariumUtils import terrariumUtils

# Dirty hack to include someone his code... to lazy to make it myself :)
# https://github.com/ageir/chirp-rpi
sys.path.insert(0, './chirp-rpi')
import chirp

from gevent import monkey, sleep
monkey.patch_all()

class terrariumI2CSensor(object):
  # control constants
  __SOFTRESET = 0xFE
  __SOFTRESET_TIMEOUT = 0.1

  __TRIGGER_TEMPERATURE_NO_HOLD = 0xF3
  __TEMPERATURE_WAIT_TIME = 0.1

  __TRIGGER_HUMIDITY_NO_HOLD = 0xF5
  __HUMIDITY_WAIT_TIME = 0.1

  hardwaretype = None

  def __init__(self, address = 40, device_number = 1, softreset_timeout   = __SOFTRESET_TIMEOUT,
                                                      temperature_timeout = __TEMPERATURE_WAIT_TIME,
                                                      humidity_timeout    = __HUMIDITY_WAIT_TIME):

    self.__address = int('0x' + str(address),16)
    self.__device_number = 1 if device_number is None else int(device_number)

    self.__softreset_timeout = softreset_timeout
    self.__temperature_timeout = temperature_timeout
    self.__humidity_timeout = humidity_timeout

    logger.debug('Initializing sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    self.__bus = smbus.SMBus(self.__device_number)

    #Datasheet recommend do Soft Reset before measurment:
    logger.debug('Send soft reset command %s with a timeout of %s seconds' % (self.__SOFTRESET,self.__softreset_timeout * 2.0))
    self.__bus.write_byte(self.__address, self.__SOFTRESET)
    sleep(self.__softreset_timeout * 2.0)

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def __get_raw_data(self,trigger,timeout):
    self.__bus.write_byte(self.__address, trigger)
    sleep(timeout * 2.0)
    data1 = self.__bus.read_byte(self.__address)
    try:
      data2 = self.__bus.read_byte(self.__address)
    except Exception, ex:
      data2 = data1
      logger.exception('Error getting second part of data in bytes from sensor \'%s\' at device %s with address %s with error: %s',(self.__class__.__name__,self.__device_number,self.__address,ex))

    return (data1,data2)

  def close(self):
    """Closes the i2c connection"""
    logger.debug('Close sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    self.__bus.close()

  def get_temperature(self):
    #From datasheet convert this in human view. Temp C = ((Temp_Code*175.72)/65536)-46.85 / T = -46.82 + (172.72 * (ST/2^16))
    #For convert 2 byte in number need MSB*256+LSB.
    logger.debug('Read temperature value from sensor type \'%s\' at device %s with address %s with command %s and timeout %s' % (self.__class__.__name__,self.__device_number,self.__address,self.__TRIGGER_TEMPERATURE_NO_HOLD,self.__temperature_timeout))
    bytedata = self.__get_raw_data(self.__TRIGGER_TEMPERATURE_NO_HOLD,self.__temperature_timeout * 2.0)
    temperature = ((bytedata[0]*256.0+bytedata[1])*175.72/65536.0)-46.85
    logger.debug('Got data from temperature sensor type \'%s\' at device %s with address %s: byte data: %s, temperature: %s' % (self.__class__.__name__,self.__device_number,self.__address,bytedata,temperature))
    return None if not terrariumUtils.is_float(temperature) else float(temperature)

  def get_humidity(self):
    #From datasheet convert this in human view. RH% = ((RH*125)/65536)-6 / RH = -6 + (125 * (SRH / 2 ^16))
    #For convert 2 byte in number need MSB*256+LSB.
    logger.debug('Read humidity value from sensor type \'%s\' at device %s with address %s with command %s and timeout %s' % (self.__class__.__name__,self.__device_number,self.__address,self.__TRIGGER_HUMIDITY_NO_HOLD,self.__humidity_timeout))
    bytedata = self.__get_raw_data(self.__TRIGGER_HUMIDITY_NO_HOLD,self.__humidity_timeout * 2.0)
    humidity = ((bytedata[0]*256.0+bytedata[1])*125.0/65536.0)-6.0
    logger.debug('Got data from humidity sensor type \'%s\' at device %s with address %s: byte data: %s, humidity: %s' % (self.__class__.__name__,self.__device_number,self.__address,bytedata,humidity))
    return None if not terrariumUtils.is_float(humidity) else float(humidity)

class terrariumSHT2XSensor(terrariumI2CSensor):
  # SHT2XX - 3.3 Volt VCC
  # 黄 = Yellow = DATA
  # 蓝 = Blue   = CLK
  # 黑 = Black  = GND
  # 棕 = Brown  = VCC

  hardwaretype = 'sht2x'
  # datasheet (v4), page 9, table 7, thanks to Martin Milata
  # for suggesting the use of these better values
  # code copied from https://github.com/mmilata/growd
  # http://www.farnell.com/datasheets/1780639.pdf
  # https://cdn-shop.adafruit.com/datasheets/Sensirion_Humidity_SHT1x_Datasheet_V5.pdf
  __TEMPERATURE_WAIT_TIME = 0.086  # (datasheet: typ=66, max=85 in ms)
  __HUMIDITY_WAIT_TIME = 0.030     # (datasheet: typ=22, max=29 in ms)
  __SOFTRESET_TIMEOUT = 0.016      # (datasheet: typ=??, max=15 in ms)

  def __init__(self, address = 40, device_number = 1):
    super(terrariumSHT2XSensor, self).__init__(address,device_number,terrariumSHT2XSensor.__SOFTRESET_TIMEOUT,
                                                                     terrariumSHT2XSensor.__TEMPERATURE_WAIT_TIME,
                                                                     terrariumSHT2XSensor.__HUMIDITY_WAIT_TIME)

class terrariumHTU21DSensor(terrariumI2CSensor):
  hardwaretype = 'htu21d'
  # Datasheet - https://datasheet.octopart.com/HPP845E131R5-TE-Connectivity-datasheet-15137552.pdf
  __TEMPERATURE_WAIT_TIME = 0.059  # (datasheet: typ=44, max=58 in ms)
  __HUMIDITY_WAIT_TIME = 0.019     # (datasheet: typ=14, max=18 in ms)
  __SOFTRESET_TIMEOUT = 0.016      # (datasheet: typ=??, max=15 in ms)

  def __init__(self, address = 40, device_number = 1):
    super(terrariumHTU21DSensor, self).__init__(address,device_number,terrariumHTU21DSensor.__SOFTRESET_TIMEOUT,
                                                                      terrariumHTU21DSensor.__TEMPERATURE_WAIT_TIME,
                                                                      terrariumHTU21DSensor.__HUMIDITY_WAIT_TIME)

class terrariumSi7021Sensor(terrariumI2CSensor):
  hardwaretype = 'si7021'
  # Datasheet - https://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf
  __TEMPERATURE_WAIT_TIME = 0.012  # (datasheet: typ=7, max=10.8 in ms)
  __HUMIDITY_WAIT_TIME = 0.07     # (datasheet: typ=10, max=12 in ms) -> Not correct??
  __SOFTRESET_TIMEOUT = 0.016      # (datasheet: typ=5, max=15 in ms)

  def __init__(self, address = 40, device_number = 1):
    super(terrariumSi7021Sensor, self).__init__(address,device_number,terrariumSi7021Sensor.__SOFTRESET_TIMEOUT,
                                                                      terrariumSi7021Sensor.__TEMPERATURE_WAIT_TIME,
                                                                      terrariumSi7021Sensor.__HUMIDITY_WAIT_TIME)

class terrariumBME280Sensor(object):
  hardwaretype = 'bme280'
  # Datasheet: https://ae-bst.resource.bosch.com/media/_tech/media/datasheets/BST-BME280_DS001-12.pdf

  __SOFTRESET = 0xFE
  __TEMPERATURE_WAIT_TIME = 0.5
  __SOFTRESET_TIMEOUT = 0.002  # (datasheet: typ=??, max=2 in ms)

  def __init__(self, address = 40, device_number = 1):
    self.__address = int('0x' + str(address),16)
    self.__device_number = 1 if device_number is None else int(device_number)

    # BMP280 does not have humidity sensor
    self.__has_humidity = None

    self.__softreset_timeout = __SOFTRESET_TIMEOUT
    self.__temperature_timeout = __TEMPERATURE_WAIT_TIME
    self.__humidity_timeout = self.__temperature_timeout

    self.__current_temperature = None
    self.__current_humidity = None
    self.__current_presure = None
    self.__current_altitude = None

    logger.debug('Initializing sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    self.__bus = smbus.SMBus(self.__device_number)

    #Datasheet recommend do Soft Reset before measurment:
    logger.debug('Send soft reset command %s with a timeout of %s seconds' % (self.__SOFTRESET,self.__softreset_timeout * 2.0))
    self.__bus.write_byte(self.__address, self.__SOFTRESET)
    sleep(self.__softreset_timeout * 2.0)

  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def __get_raw_data(self):
    #Address of BME280 on bus "0x76", but also some sensors uses 0x77.
    #See in "i2cdetect -y 0" (where "0" - needed bus, standart bus - "1").
    #0x88..0x9F - temperature(dig_T1..dig_T3) and pressure(dig_P1..dig_p9).
    #Read "compensation parameter storage" from 0x88, 24 bytes. Table 16, 18 in datasheet.
    b1 = self.__bus.read_i2c_block_data(self.__address, 0x88, 24)

    # Convert "compensation word"=16 bit=2 bytes -> MSB*256+LSB. 4.2.2 in datasheet.
    # Temp coefficients.
    dig_T1 = b1[1] * 256 + b1[0]
    dig_T2 = b1[3] * 256 + b1[2]
    if dig_T2 > 32767 :
        dig_T2 -= 65536
    dig_T3 = b1[5] * 256 + b1[4]
    if dig_T3 > 32767 :
        dig_T3 -= 65536

    #And again with pressure.
    # Pressure coefficients.
    dig_P1 = b1[7] * 256 + b1[6]
    dig_P2 = b1[9] * 256 + b1[8]
    if dig_P2 > 32767 :
        dig_P2 -= 65536
    dig_P3 = b1[11] * 256 + b1[10]
    if dig_P3 > 32767 :
        dig_P3 -= 65536
    dig_P4 = b1[13] * 256 + b1[12]
    if dig_P4 > 32767 :
        dig_P4 -= 65536
    dig_P5 = b1[15] * 256 + b1[14]
    if dig_P5 > 32767 :
        dig_P5 -= 65536
    dig_P6 = b1[17] * 256 + b1[16]
    if dig_P6 > 32767 :
        dig_P6 -= 65536
    dig_P7 = b1[19] * 256 + b1[18]
    if dig_P7 > 32767 :
        dig_P7 -= 65536
    dig_P8 = b1[21] * 256 + b1[20]
    if dig_P8 > 32767 :
        dig_P8 -= 65536
    dig_P9 = b1[23] * 256 + b1[22]
    if dig_P9 > 32767 :
        dig_P9 -= 65536

    #Datasheet table 16, table 18.
    #0xA1 - humidity(dig_H1).
    #Read "compensation parameter storage" from 0xA1, 1 byte.
    try:
      dig_H1 = self.__bus.read_byte_data(self.__address, 0xA1)#Comment this and this work on BMP280.
      self.__has_humidity = True
    except Exception, ex:
      self.__has_humidity = False

    #Datasheet table 16, table 18.
    #0xE1..0xE7 - humidity(dig_H2..dig_H6).
    #Read "compensation parameter storage" from 0xE1, 7 bytes.
    if self.__has_humidity:
      b1 = self.__bus.read_i2c_block_data(self.__address, 0xE1, 7)#Comment this and this work on BMP280.

      #And again...
      #Humidity coefficients.
      #Comment this and this work on BMP280.
      dig_H2 = b1[1] * 256 + b1[0]
      if dig_H2 > 32767 :
          dig_H2 -= 65536
      dig_H3 = (b1[2] &  0xFF)
      dig_H4 = (b1[3] * 16) + (b1[4] & 0xF)
      if dig_H4 > 32767 :
          dig_H4 -= 65536
      dig_H5 = (b1[4] / 16) + (b1[5] * 16)
      if dig_H5 > 32767 :
          dig_H5 -= 65536
      dig_H6 = b1[6]
      if dig_H6 > 127 :
          dig_H6 -= 256

      #Select control humidity register, 0xF2
      #Humidity Oversampling = 1(001 in datasheet table 20) -> in HEX = 01.
      self.__bus.write_byte_data(self.__address, 0xF2, 0x01)#Comment this and this work on BMP280.

    # Select Control measurement register, 0xF4.
    #Temperature + Pressure + Select Mode (Table 22,23,24,25 in datasheet).
    #7,6,5 bits for oversampling temp, 4,3,2 bit for oversampling pressure and 1,0 bit for select mode.
    #Temp oversampling 001, pressure oversampling 001, normal mode 11 -> 001 001 11 -> in HEX = 27.
    self.__bus.write_byte_data(self.__address, 0xF4, 0x27)

    #Select Configuration register, 0xF5(Table 26, 27, 28 in datasheet)
    #Stand_by time = 1000 ms -> 101(datasheet) -> in HEX =A0
    self.__bus.write_byte_data(self.__address, 0xF5, 0xA0)

    sleep(self.__temperature_timeout * 2.0)

    # Read data back from 0xF7(247), 8 bytes
    # Pressure MSB, LSB, xLSB, Temperature MSB, LSB, xLSB, Humidity MSB, LSB
    #Table 18, 29, 30, 31
    data = self.__bus.read_i2c_block_data(self.__address, 0xF7, 8)

    # Convert pressure and temperature data to 19-bits
    adc_p = ((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16
    adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16

    # Convert the humidity data
    if self.__has_humidity:
      adc_h = data[6] * 256 + data[7]#Comment this and this work on BMP280.

    #Formulas from Appendix in datasheet.
    # Temperature offset calculations
    var1 = ((adc_t) / 16384.0 - (dig_T1) / 1024.0) * (dig_T2)
    var2 = (((adc_t) / 131072.0 - (dig_T1) / 8192.0) * ((adc_t)/131072.0 - (dig_T1)/8192.0)) * (dig_T3)
    t_fine = (var1 + var2)
    self.__current_temperature = (var1 + var2) / 5120.0

    #Formulas from Appendix in datasheet.
    # Pressure offset calculations
    var1 = (t_fine / 2.0) - 64000.0
    var2 = var1 * var1 * (dig_P6) / 32768.0
    var2 = var2 + var1 * (dig_P5) * 2.0
    var2 = (var2 / 4.0) + ((dig_P4) * 65536.0)
    var1 = ((dig_P3) * var1 * var1 / 524288.0 + ( dig_P2) * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * (dig_P1)
    p = 1048576.0 - adc_p
    p = (p - (var2 / 4096.0)) * 6250.0 / var1
    var1 = (dig_P9) * p * p / 2147483648.0
    var2 = p * (dig_P8) / 32768.0
    self.__current_presure = (p + (var1 + var2 + (dig_P7)) / 16.0) / 100.0

    #Formulas from Appendix in datasheet.
    # Humidity offset calculations
    #Comment this and this work on BMP280.
    if self.__has_humidity:
      var_H = ((t_fine) - 76800.0)
      var_H = (adc_h - (dig_H4 * 64.0 + dig_H5 / 16384.0 * var_H)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * var_H * (1.0 + dig_H3 / 67108864.0 * var_H)))
      self.__current_humidity = var_H * (1.0 -  dig_H1 * var_H / 524288.0)
      if self.__current_humidity > 100.0 :
        self.__current_humidity = 100.0
      elif self.__current_humidity < 0.0 :
        self.__current_humidity = 0.0

    # https://github.com/avislab/sensorstest/blob/master/BME280/BME280.py#L176
    altitude = self.__current_presure/101325.0
    altitude = 1 - pow(altitude, 0.19029)
    self.__current_altitude = round(44330.0*altitude, 3)

  def close(self):
    """Closes the i2c connection"""
    logger.debug('Close sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    self.__bus.close()

  def get_temperature(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__current_temperature) else float(self.__current_temperature)

  def get_humidity(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__current_humidity) else float(self.__current_humidity)

  def get_presure(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__current_presure) else float(self.__current_presure)

  def get_altitude(self):
    self.__get_raw_data()
    return None if not terrariumUtils.is_float(self.__current_altitude) else float(self.__current_altitude)

class terrariumVEML6075Sensor(object):
  # Rewritten based on https://github.com/alexhla/uva-uvb-sensor-veml6075-driver/
  hardwaretype = 'veml6075'

  # Register Addresses
  __REGISTER_CONF = 0x00
  __REGISTER_UVA = 0x07
  __REGISTER_UVB = 0x09
  __REGISTER_VISIBLE_NOISE = 0x0A
  __REGISTER_IR_NOISE = 0x0B

  # Config Register Bit Masks
  __POWER_ON = 0x00
  __POWER_OFF = 0x01
  __SENSITIVITY_NORMAL_DYNAMIC = 0x00
  __SENSITIVITY_HIGH_DYNAMIC = 0x08
  __SENSITIVITY_INTEGRATION_800 = 0x40
  __SENSITIVITY_INTEGRATION_400 = 0x30
  __SENSITIVITY_INTEGRATION_200 = 0x20
  __SENSITIVITY_INTEGRATION_100 = 0x10
  __SENSITIVITY_INTEGRATION_50 = 0x00

  # UV Coefficents, Responsivity
  __UV_COEFFICENT_UVA_VISIBLE = 2.22
  __UV_COEFFICENT_UVA_IR = 1.33
  __UV_COEFFICENT_UVB_VISIBLE = 2.95
  __UV_COEFFICENT_UVB_IR = 1.74

  # Conversion Factors (VEML6075 Datasheet Rev. 1.2, 23-Nov-16)
  __UVA_COUNTS_PER_UWCM = 0.93
  __UVB_COUNTS_PER_UWCM = 2.10

  __SENSITIVITY_MODE = 0

  def __init__(self, address = 10, device_number = 1):
    self.__address = int('0x' + str(address),16)
    self.__device_number = 1 if device_number is None else int(device_number)

    self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_800
    self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_NORMAL_DYNAMIC
    self.__wait_time = 1.920
    self.__divisor = 16.0

  def __enter__(self):
    """used to enable python's with statement support"""
    self.__bus = smbus.SMBus(self.__device_number)
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def close(self):
    """Closes the i2c connection"""
    logger.debug('Close sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    self.__bus.close()

  def __set_sensitivity(self):
    if terrariumVEML6075Sensor.__SENSITIVITY_MODE == 0:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_800  # Most Sensitive
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_NORMAL_DYNAMIC
      self.__wait_time = 1.920
      self.__divisor = 16.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 1:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_400
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_NORMAL_DYNAMIC
      self.__wait_time = 0.960
      self.__divisor = 8.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 2:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_200
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_NORMAL_DYNAMIC
      self.__wait_time = 0.480
      self.__divisor = 4.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 3:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_100
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_NORMAL_DYNAMIC
      self.__wait_time = 0.240
      self.__divisor = 2.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 4:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_50
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_NORMAL_DYNAMIC
      self.__wait_time = 0.120
      self.__divisor = 1.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 5:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_800
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_HIGH_DYNAMIC
      self.__wait_time = 1.920
      self.__divisor = 16.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 6:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_400
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_HIGH_DYNAMIC
      self.__wait_time = 0.960
      self.__divisor = 8.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 7:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_200
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_HIGH_DYNAMIC
      self.__wait_time = 0.480
      self.__divisor = 4.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 8:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_100
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_HIGH_DYNAMIC
      self.__wait_time = 0.240
      self.__divisor = 2.0
    elif terrariumVEML6075Sensor.__SENSITIVITY_MODE == 9:
      self.__integTimeSelect = terrariumVEML6075Sensor.__SENSITIVITY_INTEGRATION_50  # Least Sensitive
      self.__dynamicSelect = terrariumVEML6075Sensor.__SENSITIVITY_HIGH_DYNAMIC
      self.__wait_time = 0.120
      self.__divisor = 1.0

  def __get_raw_data(self,part):
    self.__set_sensitivity()

    # Write Dynamic and Integration Time Settings to Sensor
    self.__bus.write_byte_data(self.__address, terrariumVEML6075Sensor.__REGISTER_CONF, self.__integTimeSelect|self.__dynamicSelect|terrariumVEML6075Sensor.__POWER_ON)
    # Wait for ADC to finish first and second conversions, discarding the first
    sleep(self.__wait_time)
    # Power OFF
    self.__bus.write_byte_data(self.__address, terrariumVEML6075Sensor.__REGISTER_CONF, terrariumVEML6075Sensor.__POWER_OFF)

    # Get RAW data
    if 'uva' == part:
      __register = terrariumVEML6075Sensor.__REGISTER_UVA
      __compensate_light = terrariumVEML6075Sensor.__UV_COEFFICENT_UVA_VISIBLE
      __compensate_ir = terrariumVEML6075Sensor.__UV_COEFFICENT_UVA_IR
      __counts_per_uWcm = terrariumVEML6075Sensor.__UVA_COUNTS_PER_UWCM

    if 'uvb' == part:
      __register = terrariumVEML6075Sensor.__REGISTER_UVB
      __compensate_light = terrariumVEML6075Sensor.__UV_COEFFICENT_UVB_VISIBLE
      __compensate_ir = terrariumVEML6075Sensor.__UV_COEFFICENT_UVB_IR
      __counts_per_uWcm = terrariumVEML6075Sensor.__UVB_COUNTS_PER_UWCM

    try:
      value = float(self.__bus.read_word_data(self.__address,__register))
      compensate_visible_light = float(self.__bus.read_word_data(self.__address,terrariumVEML6075Sensor.__REGISTER_VISIBLE_NOISE))  # visible noise
      compensate_ir_light = float(self.__bus.read_word_data(self.__address,terrariumVEML6075Sensor.__REGISTER_IR_NOISE))  # infrared noise
    except Exception, ex:
      print ex
      return None

    # Scale down
    value /= self.__divisor
    compensate_visible_light /= self.__divisor
    compensate_ir_light /= self.__divisor

    # Compensate
    value = value - (__compensate_light * compensate_visible_light) - (__compensate_ir * compensate_ir_light)
    if value < 0.0:
      return 0

    # Convert to  uWcm^2
    value /= __counts_per_uWcm
    return value

  def get_uva(self):
    return self.__get_raw_data('uva')

  def get_uvb(self):
    return self.__get_raw_data('uvb')

class terrariumChirpSensor(object):
  hardwaretype = 'chirp'
  # Datasheet: https://wemakethings.net/chirp/

  def __init__(self, address = 20, device_number = 1, min_moist = 160, max_moist = 720, temp_offset = 2):
    self.__address = int('0x' + str(address),16)
    self.__device_number = 1 if device_number is None else int(device_number)

    self.__min_moist = min_moist
    self.__max_moist = max_moist
    self.__temp_offset = temp_offset

    logger.debug('Initializing sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))


  def __enter__(self):
    """used to enable python's with statement support"""
    return self

  def __exit__(self, type, value, traceback):
    """with support"""
    self.close()

  def close(self):
    """Closes the i2c connection"""
    logger.debug('Close sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    #self.__bus.close()

  def __get_raw_data(self,part):
    # min_moist and max_moist are 'best guess' for now
    sensor = chirp.Chirp(bus=self.__device_number,
                  address=self.__address,
                  read_moist=False,
                  read_temp=False,
                  read_light=False,
                  min_moist=self.__min_moist,
                  max_moist=self.__max_moist,
                  temp_scale='celsius',
                  temp_offset=self.__temp_offset)
    value = None

    sensor.read_temp  = 'temperature' == part
    sensor.read_moist = 'moisture' == part
    sensor.read_light = 'light' == part

#    sensor.reset()
    sensor.trigger()

    if 'temperature' == part:
      value = float(sensor.temp)
    if 'moisture' == part:
      value = float(sensor.moist_percent)
    if 'light' == part:
      value = float(sensor.light)

    return value

  def get_temperature(self):
    logger.debug('Read temperature value from sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    temperature = self.__get_raw_data('temperature')
    logger.debug('Got data from temperature sensor type \'%s\' at device %s with address %s: temperature: %s' % (self.__class__.__name__,self.__device_number,self.__address,temperature))
    return None if not terrariumUtils.is_float(temperature) else float(temperature)

  def get_moisture(self):
    logger.debug('Read moisture value from sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    moisture = self.__get_raw_data('moisture')
    logger.debug('Got data from moisture sensor type \'%s\' at device %s with address %s: moisture: %s' % (self.__class__.__name__,self.__device_number,self.__address,moisture))
    return None if not terrariumUtils.is_float(moisture) else float(moisture)

  def get_light(self):
    logger.debug('Read brightness value from sensor type \'%s\' at device %s with address %s' % (self.__class__.__name__,self.__device_number,self.__address))
    light = self.__get_raw_data('light')
    if light is not None:
      light = 100.0 - ((light / 65536.0) * 100.0)
    logger.debug('Got data from brightness sensor type \'%s\' at device %s with address %s: brightness: %s' % (self.__class__.__name__,self.__device_number,self.__address,light))
    return None if not terrariumUtils.is_float(light) else float(light)
