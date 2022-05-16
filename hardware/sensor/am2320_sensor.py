# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumI2CSensor

from struct import unpack
from time import sleep

class terrariumAM2320Sensor(terrariumI2CSensor):

  HARDWARE = 'am2320'
  TYPES    = ['temperature','humidity']
  NAME     = 'AM2320 sensor'

  __PARAM_AM2320_READ = 0x03
  __REG_AM2320_HUMIDITY_MSB = 0x00

  def __get_raw_data(self,command, regaddr, regcount):

    def __am_crc16(buf):
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

    with self._open_hardware() as i2c_bus:
      try:
        # wake AM2320 up, goes to sleep to not warm up and affect the humidity sensor
        # This write will fail as AM2320 won't ACK this write
        i2c_bus.write_i2c_block_data(self.device[0], 0x00, [])
      except Exception as ex:
        logger.debug(f'Wake up {self} hardware: {ex}')

      sleep(0.01)
      i2c_bus.write_i2c_block_data(self.device[0], command, [regaddr, regcount])
      sleep(0.002)
      buf = i2c_bus.read_i2c_block_data(self.device[0], 0, 8)

    buf_str = ''.join(chr(x) for x in buf)

    crc = unpack('<H', buf_str[-2:])[0]
    if crc != __am_crc16(buf[:-2]):
      logger.error('AM2320 CRC error for sensor {}'.format(self.get_name()))
      return None

    return buf_str[2:-2]

  def _get_data(self):
    data = {}
    sensor_data = self.__get_raw_data(self.__PARAM_AM2320_READ, self.__REG_AM2320_HUMIDITY_MSB, 4)
    data['temperature'] = unpack('>H', sensor_data[-2:])[0] / 10.0
    data['humidity']    = unpack('>H', sensor_data[-4:2])[0] / 10.0

    return data
