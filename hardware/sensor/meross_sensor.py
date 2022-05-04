# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import os

from . import terrariumSensor, terrariumSensorLoadingException
from terrariumUtils import terrariumUtils, terrariumCache
from terrariumCloud import TerrariumMerossCloud

class terrariumMS100Sensor(terrariumSensor):
  HARDWARE = 'ms100'
  TYPES    = ['temperature','humidity']
  NAME     = 'Meross MS100'

  def _load_hardware(self):
    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL',''))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD',''))

    if '' == EMAIL or '' == PASSWORD:
      raise terrariumSensorLoadingException('Meross cloud is not enabled.')

    self._cache = terrariumCache()

    print(f'Loaded the cache for {self.name}')
    print(self)
    print(dir(self))
    print(self._cache)
    print(dir(self._cache))

    return self.address

  def _get_data(self):
    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL',''))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD',''))

    if '' == EMAIL or '' == PASSWORD:
      logger.error('Meross cloud is not enabled.')
      return

    try:
      return self._cache.get_data(self.address)
    except Exception as ex:
      print(f'Error with caching merross: {ex}')
      print(self)
      print(dir(self))
      print(self._cache)
      logger.error(f'Error getting new data for {self}: {ex}')
      return None


  @staticmethod
  def _scan_sensors(unit_value_callback = None, trigger_callback = None):
    found_devices = []

    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL',''))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD',''))

    if not ('' == EMAIL or '' == PASSWORD):

      cloud = TerrariumMerossCloud(EMAIL,PASSWORD)
      devices = cloud.scan_hardware('sensors')

      for device in devices:
        for sensor_type in terrariumMS100Sensor.TYPES:
          found_devices.append(
            terrariumSensor(None,
                            terrariumMS100Sensor.HARDWARE,
                            sensor_type,
                            f'{device.subdevice_id}',
                            f'{terrariumMS100Sensor.NAME} {device.name} measuring {sensor_type}',
                            unit_value_callback = unit_value_callback,
                            trigger_callback    = trigger_callback)
          )

    for device in found_devices:
      yield device