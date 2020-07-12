# -*- coding: utf-8 -*-
# Sources: https://github.com/iotify/custom-lab/blob/master/sht2x.py
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import smbus
import smbus2
import sys
import Adafruit_SHT31
import bme280

# Dirty hack to include someone his code... to lazy to make it myself :)
# https://github.com/ageir/chirp-rpi
sys.path.insert(0, './chirp-rpi')
import chirp
sys.path.insert(0, './python-MLX90614')
from mlx90614 import MLX90614
from struct import unpack
from gevent import sleep
try:
  import melopero_amg8833 as mp
except Exception:
  pass # Needs python3

try:
  import adafruit_sht31d
  import board
  import busio
except Exception:
  pass # Needs python3

from terrariumSensor import terrariumSensorSource
from terrariumUtils import terrariumUtils

class terrariumI2CSensor(terrariumSensorSource):
  TYPE = None
  VALID_SENSOR_TYPES = ['temperature','humidity']

  # control constants
  SOFTRESET = 0xFE
  SOFTRESET_TIMEOUT = 0.1

  TRIGGER_TEMPERATURE_NO_HOLD = 0xF3
  TEMPERATURE_WAIT_TIME = 0.1

  TRIGGER_HUMIDITY_NO_HOLD = 0xF5
  HUMIDITY_WAIT_TIME = 0.1

  def load_data(self):
    self.i2c_bus = None

    data = None
    if self.open():
      data = self.load_raw_data()
      self.close()

    return data

  def open(self):
    try:
      gpio_pins = self.get_address().split(',')
      logger.debug('Open sensor type \'{}\' with address {}'.format(self.get_type(),gpio_pins))
      #Datasheet recommend do Soft Reset before measurment:
      self.i2c_bus = smbus.SMBus(1 if len(gpio_pins) == 1 else int(gpio_pins[1]))
      if self.SOFTRESET_TIMEOUT > 0.0:
        logger.debug('Send soft reset command \'{}\' with a timeout of {} seconds'.format(self.SOFTRESET,self.SOFTRESET_TIMEOUT * 2.0))
        self.i2c_bus.write_byte(int('0x' + gpio_pins[0],16), self.SOFTRESET)
        sleep(self.SOFTRESET_TIMEOUT * 2.0)

    except Exception as ex:
      logger.warning('Error opening {} sensor \'{}\'. Error message: {}'.format(self.get_type(),self.get_name(),ex))
      self.close()
      return False

    return True

  def get_raw_data(self,trigger,timeout):
    gpio_pins = self.get_address().split(',')
    self.i2c_bus.write_byte(int('0x' + gpio_pins[0],16), trigger)
    sleep(timeout * 2.0)
    data1 = self.i2c_bus.read_byte(int('0x' + gpio_pins[0],16))
    try:
      data2 = self.i2c_bus.read_byte(int('0x' + gpio_pins[0],16))
    except Exception as ex:
      data2 = data1
      logger.warning('Error getting second part of data in bytes from sensor \'{}\' with address {} with error: {}'.format(self.get_name(),self.get_address(),ex))

    return (data1,data2)

  def load_raw_data(self):
    data = None

    try:
      data = {}
      bytedata = self.get_raw_data(self.TRIGGER_TEMPERATURE_NO_HOLD,self.TEMPERATURE_WAIT_TIME)
      data['temperature'] = ((bytedata[0]*256.0+bytedata[1])*175.72/65536.0)-46.85
    except Exception as ex:
      print('load_raw_data temp:')
      print(ex)

    try:
      if data is None:
        data = {}
      bytedata = self.get_raw_data(self.TRIGGER_HUMIDITY_NO_HOLD,self.HUMIDITY_WAIT_TIME)
      data['humidity'] = ((bytedata[0]*256.0+bytedata[1])*125.0/65536.0)-6.0
    except Exception as ex:
      print('load_raw_data humid:')
      print(ex)

    return data

  def close(self):
    try:
      self.i2c_bus.close()
    except AttributeError as ex:
      pass # Bus is already closed
    except Exception as ex:
      logger.warning('Error closing {} sensor \'{}\'. Error message: {}'.format(self.get_type(),self.get_name(),ex))

  def stop(self):
    self.close()
    super(terrariumI2CSensor,self).stop()

class terrariumSHT2XSensor(terrariumI2CSensor):
  TYPE = 'sht2x'
  # SHT2XX - 3.3 Volt VCC
  # 黄 = Yellow = DATA
  # 蓝 = Blue   = CLK
  # 黑 = Black  = GND
  # 棕 = Brown  = VCC

  # datasheet (v4), page 9, table 7, thanks to Martin Milata
  # for suggesting the use of these better values
  # code copied from https://github.com/mmilata/growd
  # http://www.farnell.com/datasheets/1780639.pdf
  # https://cdn-shop.adafruit.com/datasheets/Sensirion_Humidity_SHT1x_Datasheet_V5.pdf
  TEMPERATURE_WAIT_TIME = 0.086  # (datasheet: typical=66, max=85 in ms)
  HUMIDITY_WAIT_TIME = 0.030     # (datasheet: typical=22, max=29 in ms)
  SOFTRESET_TIMEOUT = 0.016      # (datasheet: typical=??, max=15 in ms)

class terrariumSHT3XSensor(terrariumSensorSource):
  TYPE = 'sht3x'
  VALID_SENSOR_TYPES = ['temperature','humidity']

  # Datasheet: https://cdn-shop.adafruit.com/product-files/2857/Sensirion_Humidity_SHT3x_Datasheet_digital-767294.pdf
  def load_data(self):
    data = None
    try:
      data = {}
      gpio_pins = self.get_address().split(',')
      sensor = Adafruit_SHT31.SHT31(int('0x' + gpio_pins[0],16))

      data['temperature'] = float(sensor.read_temperature())
      data['humidity'] = float(sensor.read_humidity())

    except Exception as ex:
      print(ex)

    return data

class terrariumSHT3XDSensor(terrariumSensorSource):
  TYPE = 'sht3xd'
  VALID_SENSOR_TYPES = ['temperature','humidity']

  # https://github.com/adafruit/Adafruit_CircuitPython_SHT31D/
  def load_data(self):
    data = None
    try:
      data = {}
      # Used 2 fixed known addresses
      i2c = busio.I2C(board.SCL, board.SDA)
      sensor = adafruit_sht31d.SHT31D(i2c)
      sensor.repeatability = adafruit_sht31d.REP_MED
      sensor.mode = adafruit_sht31d.MODE_SINGLE

      data['temperature'] = float(sensor.temperature)
      data['humidity'] = float(sensor.relative_humidity)

    except Exception as ex:
      print(ex)

    return data

class terrariumHTU21DSensor(terrariumI2CSensor):
  TYPE = 'htu21d'

  # Datasheet - https://datasheet.octopart.com/HPP845E131R5-TE-Connectivity-datasheet-15137552.pdf
  TEMPERATURE_WAIT_TIME = 0.059  # (datasheet: typ=44, max=58 in ms)
  HUMIDITY_WAIT_TIME = 0.019     # (datasheet: typ=14, max=18 in ms)
  SOFTRESET_TIMEOUT = 0.016      # (datasheet: typ=??, max=15 in ms)

class terrariumSi7021Sensor(terrariumI2CSensor):
  TYPE = 'si7021'

  # Datasheet - https://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf
  TEMPERATURE_WAIT_TIME = 0.012  # (datasheet: typ=7, max=10.8 in ms)
  HUMIDITY_WAIT_TIME = 0.07     # (datasheet: typ=10, max=12 in ms) -> Not correct??
  SOFTRESET_TIMEOUT = 0.016      # (datasheet: typ=5, max=15 in ms)

class terrariumBME280Sensor(terrariumI2CSensor):
  TYPE = 'bme280'
  VALID_SENSOR_TYPES = ['temperature','humidity','altitude','pressure']

  def __get_address(self):
    address = self.get_address().split(',')
    bus = 1 if len(address) == 1 else int(address[1])
    address = int('0x' + address[0],16)


    # (address,*bus) = self.get_address().split(',')
    # address = int('0x' + address,16)
    # bus = 1 if len(bus) == 0 else int(bus[0])
    return (address,bus)

  def load_raw_data(self):
    sensor_data = None

    try:
      sensor_data = self.get_empty_data_set()
      (address,bus) = self.__get_address()

      with smbus2.SMBus(bus) as i2cbus:
        calibration_params = bme280.load_calibration_params(i2cbus, address)

        # the sample method will take a single reading and return a
        # compensated_reading object
        data = bme280.sample(i2cbus, address, calibration_params)

        # the compensated_reading class has the following attributes
        sensor_data['temperature'] = data.temperature
        sensor_data['humidity'] = data.humidity
        sensor_data['pressure'] = data.pressure

      # https://github.com/avislab/sensorstest/blob/master/BME280/BME280.py#L176
      sensor_data['altitude'] = sensor_data['pressure']/101325.0
      sensor_data['altitude'] = 1 - pow(sensor_data['altitude'], 0.19029)
      sensor_data['altitude'] = round(44330.0*sensor_data['altitude'], 3)

    except Exception as ex:
      print('terrariumBME280Sensor Ex:')
      print(ex)

    return sensor_data

class terrariumVEML6075Sensor(terrariumI2CSensor):
  TYPE = 'veml6075'
  VALID_SENSOR_TYPES = ['uva','uvb','uvi']

  # Disable the I2C softreset
  SOFTRESET_TIMEOUT = 0

  # Rewritten based on https://github.com/alexhla/uva-uvb-sensor-veml6075-driver/
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

  __UVA_RESP = 0.001461
  __UVB_RESP = 0.002591

  # Conversion Factors (VEML6075 Datasheet Rev. 1.2, 23-Nov-16)
  __UVA_COUNTS_PER_UWCM = 0.93
  __UVB_COUNTS_PER_UWCM = 2.10

  __SENSITIVITY_MODE = 0

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

  def load_raw_data(self):
    data = None

    try:
      data = {}
      gpio_pins = self.get_address().split(',')

      self.__set_sensitivity()
      # Write Dynamic and Integration Time Settings to Sensor
      self.i2c_bus.write_byte_data(int('0x' + gpio_pins[0],16), terrariumVEML6075Sensor.__REGISTER_CONF, self.__integTimeSelect|self.__dynamicSelect|terrariumVEML6075Sensor.__POWER_ON)
      # Wait for ADC to finish first and second conversions, discarding the first
      sleep(self.__wait_time)
      # Power OFF
      self.i2c_bus.write_byte_data(int('0x' + gpio_pins[0],16), terrariumVEML6075Sensor.__REGISTER_CONF, terrariumVEML6075Sensor.__POWER_OFF)

      value_uva = float(self.i2c_bus.read_word_data(int('0x' + gpio_pins[0],16),terrariumVEML6075Sensor.__REGISTER_UVA))
      value_uvb = float(self.i2c_bus.read_word_data(int('0x' + gpio_pins[0],16),terrariumVEML6075Sensor.__REGISTER_UVB))

      compensate_visible_light = float(self.i2c_bus.read_word_data(int('0x' + gpio_pins[0],16),terrariumVEML6075Sensor.__REGISTER_VISIBLE_NOISE))  # visible noise
      compensate_ir_light = float(self.i2c_bus.read_word_data(int('0x' + gpio_pins[0],16),terrariumVEML6075Sensor.__REGISTER_IR_NOISE))  # infrared noise

      # Scale down
      value_uva /= self.__divisor
      value_uvb /= self.__divisor
      compensate_visible_light /= self.__divisor
      compensate_ir_light /= self.__divisor

      # Compensate
      value_uva = value_uva - (terrariumVEML6075Sensor.__UV_COEFFICENT_UVA_VISIBLE * compensate_visible_light) - (terrariumVEML6075Sensor.__UV_COEFFICENT_UVA_IR * compensate_ir_light)
      value_uvb = value_uvb - (terrariumVEML6075Sensor.__UV_COEFFICENT_UVB_VISIBLE * compensate_visible_light) - (terrariumVEML6075Sensor.__UV_COEFFICENT_UVB_IR * compensate_ir_light)

      value_uva = value_uva if value_uva > 0.0 else 0.0
      value_uvb = value_uvb if value_uvb > 0.0 else 0.0

      # Calculate UV Index value
      data['uvi'] = ((value_uva * terrariumVEML6075Sensor.__UVA_RESP) + (value_uvb * terrariumVEML6075Sensor.__UVB_RESP)) / 2

      # Convert to  uW/cm^2
      value_uva /= terrariumVEML6075Sensor.__UVA_COUNTS_PER_UWCM
      value_uvb /= terrariumVEML6075Sensor.__UVB_COUNTS_PER_UWCM

      data['uva'] = value_uva
      data['uvb'] = value_uvb

    except Exception as ex:
      print('load_raw_data temp:')
      print(ex)

    return data

class terrariumChirpSensor(terrariumSensorSource):
  TYPE = 'chirp'
  VALID_SENSOR_TYPES = ['temperature','moisture','light']

  # Datasheet: https://wemakethings.net/chirp/
  def __init__(self, sensor_id, sensor_type, address, name = '', callback_indicator = None):
    self.set_min_moist_calibration(160)
    self.set_max_moist_calibration(720)
    self.set_temperature_offset_calibration(2)

    if sensor_type in ['light']:
      self.set_limit_max(1000)

    super(terrariumChirpSensor,self).__init__(sensor_id, sensor_type, address, name, callback_indicator)

  def set_min_moist_calibration(self,limit):
    self.__min_moist = float(limit)

  def get_min_moist_calibration(self):
    return self.__min_moist

  def set_max_moist_calibration(self,limit):
    self.__max_moist = float(limit)

  def get_max_moist_calibration(self):
    return self.__max_moist

  def set_temperature_offset_calibration(self,limit):
    self.__temp_offset = float(limit)

  def get_temperature_offset_calibration(self):
    return self.__temp_offset

  def load_data(self):
    data = None
    try:
      data = {}
      gpio_pins = self.get_address().split(',')
      sensor = chirp.Chirp(bus=1 if len(gpio_pins) == 1 else int(gpio_pins[1]),
                           address=int('0x' + gpio_pins[0],16),
                           read_moist=True,
                           read_temp=True,
                           read_light=True,
                           min_moist=self.get_min_moist_calibration(),
                           max_moist=self.get_max_moist_calibration(),
                           temp_scale='celsius',
                           temp_offset=self.get_temperature_offset_calibration())

      sensor.trigger()
      data['temperature'] = float(sensor.temp)
      data['moisture'] = float(sensor.moist_percent)
      data['light'] = 100.0 - ((float(sensor.light) / 65536.0) * 100.0)
      # Dirty hack. The Chirp sensor does not close it connection. We will force it here
      sensor.bus.close()

    except Exception as ex:
      print(ex)

    return data

  def get_data(self, temperature_type = None):
    data = super(terrariumChirpSensor,self).get_data(temperature_type)
    data['min_moist'] = self.get_min_moist_calibration()
    data['max_moist']  = self.get_max_moist_calibration()
    data['temp_offset']  = self.get_temperature_offset_calibration()

    return data

class terrariumMLX90614Sensor(terrariumSensorSource):
  TYPE = 'mlx90614'
  VALID_SENSOR_TYPES = ['temperature']

  def set_address(self,address):
    super(terrariumMLX90614Sensor,self).set_address(address)
    data = self.get_address().split(',')
    self.i2c_address = int('0x' + data[0],16)
    self.i2c_bus = 1
    self.temp_type = 'object'
    if len(data) == 3:
      _, self.i2c_bus, self.temp_type = data
    elif len(data) == 2:
      if 'a' == data[1]:
        self.temp_type = 'ambient'
      elif 'o' == data[1]:
        self.temp_type = 'object'
      else:
        self.i2c_bus = data[1]

  def load_data(self):
    data = None

    try:
      data = {}
      sensor = MLX90614(self.i2c_address,int(self.i2c_bus))

      # we cannot cache data here.... as both are 'temperature' values
      if 'object' == self.temp_type:
        data['temperature'] = float(sensor.get_obj_temp())
      elif 'ambient' == self.temp_type:
        data['temperature'] = float(sensor.get_amb_temp())
      else:
        data = None

      # We need to close the I2C bus manually... :(
      sensor.bus.close()

    except Exception as ex:
      print(ex)

    return data

class terrariumAM2320Sensor(terrariumI2CSensor):
  TYPE = 'am2320'

  SOFTRESET_TIMEOUT = 0.0

  PARAM_AM2320_READ = 0x03
  REG_AM2320_HUMIDITY_MSB = 0x00

  def _am_crc16(self, buf):
    crc = 0xFFFF
    for c in buf:
      crc ^= c
      for i in range(8):
        if crc & 0x01:
          crc >>= 1
          crc ^= 0xA001
        else:
          crc >>= 1
    return crc

  def get_raw_data(self,command, regaddr, regcount):
    gpio_pins = self.get_address().split(',')
    try:
      try:
        # wake AM2320 up, goes to sleep to not warm up and affect the humidity sensor
        # This write will fail as AM2320 won't ACK this write
        self.i2c_bus.write_i2c_block_data(int('0x' + gpio_pins[0],16), 0x00, [])
      except Exception as ex:
        pass # As this is expected

      self.i2c_bus.write_i2c_block_data(int('0x' + gpio_pins[0],16), command, [regaddr, regcount])

      sleep(0.002)

      buf = self.i2c_bus.read_i2c_block_data(int('0x' + gpio_pins[0],16), 0, 8)
    except Exception as ex:
      #logger.error('Error reading sensor {}'.format(self.get_name()))
      return None

    buf_str = "".join(chr(x) for x in buf)

    crc = unpack('<H', buf_str[-2:])[0]
    if crc != self._am_crc16(buf[:-2]):
      logger.warning('AM2320 CRC error for sensor {}'.format(self.get_name()))
      return None

    return buf_str[2:-2]

  def load_raw_data(self):
    data = None

    try:
      raw_data = self.get_raw_data(self.PARAM_AM2320_READ, self.REG_AM2320_HUMIDITY_MSB, 4)
      if raw_data is None:
        return raw_data

      data = {}
      data['temperature'] = unpack('>H', raw_data[-2:])[0] / 10.0
      data['humidity'] = unpack('>H', raw_data[-4:2])[0] / 10.0
    except Exception as ex:
      print('load_raw_data error:')
      print(ex)

    return data

class terrariumAMG8833Sensor(terrariumSensorSource):
  TYPE = 'amg8833'
  VALID_SENSOR_TYPES = ['temperature']

  def set_address(self,address):
    super(terrariumAMG8833Sensor,self).set_address(address)
    data = self.get_address().split(',')
    self.i2c_address = int('0x' + data[0],16)
    self.i2c_bus = 1

  def load_data(self):
    data = None

    try:
      data = {}
      sensor = mp.AMGGridEye(self.i2c_address,self.i2c_bus)
      sensor.set_fps_mode(mp.AMGGridEye.FPS_1_MODE)
      sensor.update_temperature()
      data['temperature'] = float(sensor.get_temperature())

    except Exception as ex:
      print(ex)

    return data
