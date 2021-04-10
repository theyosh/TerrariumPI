# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import os
from unsync import unsync
from datetime import datetime

from . import terrariumSensor, terrariumSensorLoadingException
from terrariumUtils import terrariumUtils

# pip install meross-iot
# https://github.com/albertogeniola/MerossIot
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.model.http.exception import BadLoginException
from meross_iot.model.exception import CommandTimeoutError


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

    @unsync
    async def __get_hardware_state():
      data = {}
      try:
        # Setup the HTTP client API from user-password
        http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

        # Setup and start the device manager
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        # Get the device based on uuid
        await manager.async_device_discovery()
        meross_devices = manager.find_devices(device_type='ms100')

        for device in meross_devices:
          # TODO: Cache this data also....
          if self.device != device.subdevice_id:
            continue

          await device.async_update()

          if device.last_sampled_time is not None and (datetime.utcnow() - device.last_sampled_time).total_seconds() < 5 * 60:
            data['temperature'] = device.last_sampled_temperature
            data['humidity']    = device.last_sampled_humidity
          else:
            logger.warning(f'Sensor {self} is not reporting new data. Last update time is more then 5 minutes ago: {device.last_sampled_time}')

      except CommandTimeoutError:
        logger.error(f'Meross communication timed out connecting with the server.')
      except BadLoginException:
        logger.error(f'Wrong login credentials for Meross. Please check your settings')

      finally:
        # Close the manager and logout from http_api
        manager.close()
        await http_api_client.async_logout()

      return data

    work = __get_hardware_state()
    data = work.result()
    return data

  @staticmethod
  def _scan_sensors(unit_value_callback = None, trigger_callback = None):

    @unsync
    async def __scan():
      found_devices = []
      try:
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

      except CommandTimeoutError:
        logger.error(f'Meross communication timed out connecting with the server.')
      except BadLoginException:
        logger.error(f'Wrong login credentials for Meross. Please check your settings')

      finally:
        # Close the manager and logout from http_api
        manager.close()
        await http_api_client.async_logout()

      return found_devices

    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL',''))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD',''))

    found_devices = []

    if '' == EMAIL or '' == PASSWORD:
      logger.info('Meross cloud is not enabled.')
    else:
      work = __scan()
      found_devices = work.result()

    for device in found_devices:
       yield device