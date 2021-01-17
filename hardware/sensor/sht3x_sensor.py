from . import terrariumI2CSensor
from terrariumUtils import terrariumUtils

import time
# https://github.com/OlivierdenOuden/Sensirion_SHT35/blob/master/simple_SHT31.py

class terrariumSHT3XSensor(terrariumI2CSensor):
  HARDWARE = 'sht3x'
  TYPES    = ['temperature']
  NAME     = 'Sensirion SHT3X sensor'

  __SHT3x_SS   = 0x2C
  __SHT3x_READ = 0x00

  def _get_data(self):
    data = None
    with self._open_hardware() as i2c_bus:
      # MS to SL
      i2c_bus.write_i2c_block_data(self.device[0],self.__SHT3x_SS,[0x06])
      time.sleep(0.2)
      # Read out data
      data = i2c_bus.read_i2c_block_data(self.device[0],self.__SHT3x_READ,6)
      # Devide data into counts Temperature
      data = {}
      data['temperature'] = data[0] << 8 | data[1]
      data['temperature'] = -45.0 + 175.0 * float(data['temperature']) / 65535.0

      # Devide data into counts Humidity
      data['humidity'] = data[3] << 8 | data[4]
      data['humidity'] = 100.0 * float(data['humidity']) / 65535.0

    return data