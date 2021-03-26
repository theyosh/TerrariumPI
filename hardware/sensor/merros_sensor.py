# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import os
import asyncio
from datetime import datetime

from . import terrariumSensor, terrariumSensorLoadingException
from terrariumUtils import terrariumUtils

# pip install meross-iot
# https://github.com/albertogeniola/MerossIot
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.model.http.exception import BadLoginException


class terrariumMS100Sensor(terrariumSensor):
  HARDWARE = 'ms100'
  TYPES    = ['temperature','humidity']
  NAME     = 'Meross MS100'

  def _load_hardware(self):
    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL',''))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD',''))

    if '' == EMAIL or '' == PASSWORD:
      raise terrariumSensorLoadingException('Meross cloud is not enabled.')

    return self.address

  def _get_data(self):
    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL',''))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD',''))

    if '' == EMAIL or '' == PASSWORD:
      logger.error('Meross cloud is not enabled.')
      return

    async def __get_hardware_state():
      # Setup the HTTP client API from user-password
      http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

      # Setup and start the device manager
      manager = MerossManager(http_client=http_api_client)
      await manager.async_init()

      # Get the device based on uuid
      await manager.async_device_discovery()
      meross_devices = manager.find_devices(device_type='ms100')

      for device in meross_devices:
        if self.device != device.subdevice_id:
          #print('Wrong device... skip')
          continue

        await device.async_update()
        if (datetime.utcnow() - device.last_sampled_time).total_seconds() < 5 * 60:
          data['temperature'] = device.last_sampled_temperature
          data['humidity']    = device.last_sampled_humidity

      # Close the manager and logout from http_api
      manager.close()
      await http_api_client.async_logout()

    try:
      data = {}
      asyncio.run(__get_hardware_state())
      return data

    except BadLoginException:
      logger.error(f'Wrong login credentials for Meross. Please check your settings')
    except RuntimeError as err:
      pass

    return None

  @staticmethod
  def _scan_sensors(unit_value_callback = None, trigger_callback = None):
    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL',''))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD',''))

    if '' == EMAIL or '' == PASSWORD:
      logger.info('Meross cloud is not enabled.')
      return

    found_devices = []

    async def __scan():
      # Setup the HTTP client API from user-password
      http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

      # Setup and start the device manager
      manager = MerossManager(http_client=http_api_client)
      await manager.async_init()

      # Discover devices.
      await manager.async_device_discovery()
      # Filter on devices that can toggle....
      meross_devices = manager.find_devices(device_type='ms100')

      for device in meross_devices:
        await device.async_update()

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

      # Close the manager and logout from http_api
      manager.close()
      await http_api_client.async_logout()

    try:
      asyncio.run(__scan())
    except BadLoginException:
      logger.error(f'Wrong login credentials for Meross. Please check your settings')
    except RuntimeError as err:
      #logger.exception(err)
      pass

    for device in found_devices:
       yield device