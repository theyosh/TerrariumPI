# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import os
from unsync import unsync
from hashlib import md5

from . import terrariumRelay, terrariumRelayException
from terrariumUtils import terrariumUtils, terrariumCache

# pip install meross-iot
# https://github.com/albertogeniola/MerossIot
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.controller.mixins.toggle import ToggleXMixin
from meross_iot.model.http.exception import BadLoginException

class terrariumRelayMeross(terrariumRelay):
  HARDWARE = 'meross'
  NAME = 'Meross power switches'

  def _load_hardware(self):
    # Use an internal caching for speeding things up.
    self.__state_cache = terrariumCache()

    address = self._address
    if len(address) == 1:
      # When no channels/plugs defined always use the first one...
      address.append(0)

    self._device['device'] = address[0]
    self._device['switch'] = int(address[1])

    return self._device['device']

  def _set_hardware_value(self, state):
    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL'))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD'))

    if '' == EMAIL or '' == PASSWORD:
      logger.error('Meross cloud is not enabled.')
      return

    @unsync
    async def __set_hardware_state(state):
      try:
        # Setup the HTTP client API from user-password
        http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

        # Setup and start the device manager
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        # Get the device based on uuid
        await manager.async_device_discovery()
        device = manager.find_devices(device_uuids=[self._device['device']])

        if len(device) < 1:
          logger.error(f'Could not find the Meross device by id: {self._device["device"]}')
        else:
          device = device[0]
          if state != 0.0:
            await device.async_turn_on(channel=self._device['switch'])
          else:
            await device.async_turn_off(channel=self._device['switch'])

      except CommandTimeoutError:
        logger.error(f'Meross communication timed out connecting with the server.')
      except BadLoginException:
        logger.error(f'Wrong login credentials for Meross. Please check your settings')

      finally:
        # Close the manager and logout from http_api
        manager.close()
        await http_api_client.async_logout()

      return state


    data = self.__state_cache.get_data(self._device['device'])
    if data is not None and terrariumUtils.is_true(data[self._device['switch']]) == (state != 0.0):
      # If we have recent cached data and the new state is the cached current state, just return True....
      return True

#    try:
    work = __set_hardware_state(state)
    data = work.result()
    return data == state
  # except BadLoginException:
    #   logger.error(f'Wrong login credentials for Meross. Please check your settings')
    # except RuntimeError as err:
    #   logger.exception(err)
    # except Exception as ex:
    #   logger.exception(ex)

    # return False

  def _get_hardware_value(self):
    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL'))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD'))

    if '' == EMAIL or '' == PASSWORD:
      logger.error('Meross cloud is not enabled.')
      return None

    @unsync
    async def __get_hardware_state():
      data = []
      try:
        # Setup the HTTP client API from user-password
        http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

        # Setup and start the device manager
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        # Get the device based on uuid
        await manager.async_device_discovery()
        device = manager.find_devices(device_uuids=[self._device['device']])

        if len(device) < 1:
          logger.error(f'Could not find the Meross device by id: {self._device["device"]}')
        else:
          device = device[0]
          await device.async_update()
          for channel in device.channels:
            data.append(device.is_on(channel=channel.index))

      except CommandTimeoutError:
        logger.error(f'Meross communication timed out connecting with the server.')
      except BadLoginException:
        logger.error(f'Wrong login credentials for Meross. Please check your settings')

      finally:
        # Close the manager and logout from http_api
        manager.close()
        await http_api_client.async_logout()

      return data

    data = self.__state_cache.get_data(self._device['device'])

    if data is None:
      work = __get_hardware_state()
      data = work.result()
      self.__state_cache.set_data(self._device['device'],data,cache_timeout=20)

    return self.ON if len(data) >= self._device['switch'] and terrariumUtils.is_true(data[self._device['switch']]) else self.OFF

  @staticmethod
  def _scan_relays(callback=None):

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
        meross_devices = manager.find_devices(device_class=ToggleXMixin)

        for device in meross_devices:
          for channel in device.channels:
            if len(device.channels) == 1 or not channel.is_master_channel:
              found_devices.append(
                terrariumRelay(None,
                              terrariumRelayMeross.HARDWARE,
                              '{},{}'.format(device.uuid,channel.index),
                              'Channel {}'.format(channel.name),
                              None,
                              callback)
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


    EMAIL    = terrariumUtils.decrypt(os.environ.get('MEROSS_EMAIL'))
    PASSWORD = terrariumUtils.decrypt(os.environ.get('MEROSS_PASSWORD'))

    found_devices = []

    if '' == EMAIL or '' == PASSWORD:
      logger.info('Meross cloud is not enabled.')
    else:
      work = __scan()
      found_devices = work.result()

    for device in found_devices:
       yield device