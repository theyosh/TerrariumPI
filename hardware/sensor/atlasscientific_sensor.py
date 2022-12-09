from . import terrariumI2CSensor

from pathlib import Path
import re

import sys
# Dirty hack to include someone his code... to lazy to make it myself :)
# https://github.com/AtlasScientific/Raspberry-Pi-sample-code
sys.path.insert(0, str((Path(__file__).parent / Path('../../3rdparty/AtlasScientific')).resolve()))
from AtlasI2C import AtlasI2C

class terrariumAtlasScientificSensor(terrariumI2CSensor):
  HARDWARE = 'atlasscientific'
  TYPES    = ['ph','temperature','humidity','co2','conductivity','pressure']
  NAME     = 'AtlasScientific I2C sensor'

  def _load_hardware(self):
    address = self._address
    if len(address) == 1:
      address.append(1)

    print('\n\n===========================================')
    print(f'Loading sensor at address: {address[0]}')
    print('=============================================\n\n')

    return AtlasI2C(address[0],bus=int(address[1]))

  def _get_data(self):
    regex = r"[^:]+: ?(?P<value>[+-]?(\d*\.)?\d+)"

    data = self.device.query('R')
    data = re.search(regex, data)

    if data:
      data = float(data.group('value'))
      return data

    return None

  def stop(self):
    if self.device is not None:
      self.device.close()

    super().stop()