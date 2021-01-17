# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumRelay, terrariumRelayException
from terrariumUtils import terrariumUtils

# pip install meross-iot
# https://github.com/albertogeniola/MerossIot
# TODO: Make it work with the latest version.... using asyncio -> DONE!
#from meross_iot.api import MerossHttpClient, UnauthorizedException

import os
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.controller.mixins.toggle import ToggleXMixin

class terrariumRelayMeross(terrariumRelay):
  HARDWARE = 'meross'
  NAME = 'Meross power switches'

  def _load_hardware(self):
    address = self._address
    if len(address) == 1:
      # When no channels/plugs defined always use the first one...
      address.append(0)

    self._device['device'] = address[1]
    self._device['switch'] = int(address[0])

    return self._device['device']

  def _set_hardware_value(self, state, force = False):

    EMAIL    = os.environ.get('MEROSS_EMAIL', '')
    PASSWORD = os.environ.get('MEROSS_PASSWORD', '')

    async def __set_hardware_state(state):
      # Setup the HTTP client API from user-password
      http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

      # Setup and start the device manager
      manager = MerossManager(http_client=http_api_client)
      await manager.async_init()

      # Get the device based on uuid
      await manager.async_device_discovery()
      device = manager.find_devices(device_uuids=[self._device['device']])

      if len(device) < 1:
        logger.error('Could not find the Meross device at address / by id: {}'.format(self._device['device']))
      else:
        device = device[0]
        if terrariumUtils.is_true(state):
          await device.async_turn_on(channel=self._device['switch'])
        else:
          await device.async_turn_off(channel=self._device['switch'])

      # Close the manager and logout from http_api
      manager.close()
      await http_api_client.async_logout()

      #return True

    try:
      asyncio.run(__set_hardware_state(state))
      return True
    except RuntimeError as err:
      print('Meross set_hardware_state RuntimeError')
      print(err)
      return False

  def _get_hardware_value(self):
    # TODO: Make this cacheable. So that we read out all the switches at once every 30 sec or so.... This will reduce the amount of API calls
    data = []

    EMAIL    = os.environ.get('MEROSS_EMAIL', '')
    PASSWORD = os.environ.get('MEROSS_PASSWORD', '')

    async def __get_hardware_state():
      # Setup the HTTP client API from user-password
      http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

      # Setup and start the device manager
      manager = MerossManager(http_client=http_api_client)
      await manager.async_init()

      # Get the device based on uuid
      await manager.async_device_discovery()
      device = manager.find_devices(device_uuids=[self._device['device']])

      if len(device) < 1:
        logger.error('Could not find the Meross device at address / by id: {}'.format(self._device['device']))
      else:
        device = device[0]
        data.append(device.is_on(channel=self._device['switch']))

      # Close the manager and logout from http_api
      manager.close()
      await http_api_client.async_logout()

    try:
      asyncio.run(__get_hardware_state())
    except RuntimeError as err:
      print('Meross get_hardware_state RuntimeError')
      print(err)
      return None

    return self.ON if len(data) == 1 and terrariumUtils.is_true(data[0]) else self.OFF

  @staticmethod
  def _scan_relays(callback=None):
    EMAIL    = os.environ.get('MEROSS_EMAIL', '')
    PASSWORD = os.environ.get('MEROSS_PASSWORD', '')

    if '' == EMAIL or '' == PASSWORD:
      logger.info('Meross cloud is not enabled.')
      return

    found_devices = []

    async def scan():
      # Setup the HTTP client API from user-password
      http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

      # Setup and start the device manager
      manager = MerossManager(http_client=http_api_client)
      await manager.async_init()

      # Discover devices.
      await manager.async_device_discovery()
      # Filter on devices that can toggle....
      meross_devices = manager.find_devices(device_class=ToggleXMixin)

      # Print them
      print("I've found the following devices:")
      for device in meross_devices:
        print(f"- {device.name} ({device.type})({device.uuid}): {device.online_status}")
        print(dir(device))
        print(device.channels)
        for channel in device.channels:
          if len(device.channels) == 1 or not channel.is_master:
            found_devices.appen(
              terrariumPowerSwitch(md5((terrariumPowerSwitchMeross.TYPE + device.uuid + str(channel.index)).encode()).hexdigest(),
                                         terrariumPowerSwitchMeross.TYPE,
                                         '{},{}'.format(device.uuid,channel.index),
                                         'Channel {}'.format(channel.name),
                                         None,
                                         callback)
            )


      # Close the manager and logout from http_api
      manager.close()
      await http_api_client.async_logout()

    try:
      asyncio.run(scan())
    except RuntimeError as err:
      print('Meross scan_power_switches RuntimeError')
      print(err)
      pass

    for device in found_devices:
       yield device