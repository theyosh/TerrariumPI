# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import asyncio
import contextlib
import datetime
import threading

from time import sleep, time

from terrariumUtils import terrariumCache, terrariumUtils, terrariumSingleton, terrariumAsync

# pip install meross-iot
# https://github.com/albertogeniola/MerossIot
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.controller.mixins.toggle import ToggleXMixin
from meross_iot.model.http.exception import BadLoginException
from meross_iot.model.exception import CommandTimeoutError

class TerrariumMerossCloud(terrariumSingleton):

  def __init__(self, username, password):
    start = time()
    self.__engine = { 'cache' : terrariumCache(), 'running': False, 'event': asyncio.Event() , 'asyncio' : terrariumAsync()}

    self._data = {}
    self._username = username
    self._password = password
    self._start()

    while not self.__engine['running']:
      logger.info('Waiting for Meross cloud connection ... ')
      sleep(1)

    logger.info(f'Meross cloud is connected! Found {len(self._data)} devices in {time()-start:.2f} seconds.')

  def _start(self):

    def _run():
      data = asyncio.run_coroutine_threadsafe(self._main_process(), self.__engine['asyncio'].async_loop)
      data.result()

    self.__engine['thread'] = threading.Thread(target=_run)
    self.__engine['thread'].start()

  def _store_data(self):
    for key in self._data:
      self.__engine['cache'].set_data(key, self._data[key],90)

  def scan_hardware(self,type):

    async def _scan_hardware(type):
      await self.manager.async_device_discovery()
      meross_devices = []
      if 'sensors' == type:
        meross_devices = self.manager.find_devices(device_type='ms100')
      elif 'relays' == type:
        meross_devices = self.manager.find_devices(device_class=ToggleXMixin)

      return meross_devices

    data = asyncio.run_coroutine_threadsafe(_scan_hardware(type), self.__engine['asyncio'].async_loop)
    devices = data.result()
    return devices


  def toggle_relay(self, device, switch, state):

    async def _toggle_relay(device, switch, state):
      device = self.manager.find_devices(device_uuids=[device])
      if len(device) == 1:
        device = device[0]

        if state != 0.0:
          await device.async_turn_on(channel=switch)
        else:
          await device.async_turn_off(channel=switch)

        return True

      return None

    data = asyncio.run_coroutine_threadsafe(_toggle_relay(device, switch, state), self.__engine['asyncio'].async_loop)
    result = data.result()
    return result

  def stop(self):
    logger.info('Stopping Meross cloud ... ')
    self.__engine['running'] = False
    self.__engine['event'].set()
    self.__engine['thread'].join()

  async def _main_process(self):

    # https://stackoverflow.com/a/49632779
    async def event_wait(evt, timeout):
      # suppress TimeoutError because we'll return False in case of timeout
      with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(evt.wait(), timeout)
      return evt.is_set()

    async def _notification(push_notification, target_devices):
      logger.info('Got an update from the Meross Cloud.')
      for device in target_devices:
        if hasattr(device,'is_on'):
          self._data[f'{device.uuid}'] = []

          for channel in device.channels:
            self._data[f'{device.uuid}'].append(device.is_on(channel=channel.index))

        if hasattr(device,'last_sampled_temperature'):
          self._data[f'{device.subdevice_id}'] = {
            'temperature' : device.last_sampled_temperature,
            'humidity'    : device.last_sampled_humidity
          }

      self._store_data()

    try:
      # Setup the HTTP client API from user-password
      http_api_client = await MerossHttpClient.async_from_user_password(email=self._username, password=self._password)

      # Setup and start the device manager
      self.manager = MerossManager(http_client=http_api_client)
      await self.manager.async_init()

      # Discover devices.
      await self.manager.async_device_discovery()
      meross_devices = self.manager.find_devices()
      for dev in meross_devices:

        # Is a relay
        if hasattr(dev,'is_on'):
          await dev.async_update()
          self._data[f'{dev.uuid}'] = []

          for channel in dev.channels:
            self._data[f'{dev.uuid}'].append(dev.is_on(channel=channel.index))

        # Is a sensor
        if hasattr(dev,'last_sampled_temperature'):
          await dev.async_update()
          #print(f'Last data: {dev.last_sampled_time}')
          self._data[f'{dev.subdevice_id}'] = {
            'temperature' : dev.last_sampled_temperature,
            'humidity'    : dev.last_sampled_humidity
          }

      self._store_data()
      self.__engine['running'] = True
      self.manager.register_push_notification_handler_coroutine(_notification)

      while not await event_wait(self.__engine['event'], 30):
        self._store_data()

    except CommandTimeoutError:
      logger.error(f'Meross communication timed out connecting with the server.')
    except BadLoginException:
      logger.error(f'Wrong login credentials for Meross. Please check your settings')

    finally:
      # Close the manager and logout from http_api
      self.manager.close()
      await http_api_client.async_logout()
      logger.info('Closed Meross cloud connection')