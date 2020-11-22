# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from terrariumSwitch import terrariumPowerSwitchSource
from terrariumUtils import terrariumUtils

from hashlib import md5

import asyncio
from kasa import Discover, SmartStrip, SmartPlug

class terrariumPowerSwitchTPLinkKasa(terrariumPowerSwitchSource):
  TYPE = 'tplinkkasa'
  URL = '^\d{1,3}\.\d{1,3}\.\d{1,3}(,\d{1,3})?$'

  def __get_address(self):
    data = self.get_address().strip().split(',')
    if len(data) == 2 and '' == data[1]:
      del(data[1])

    return data

  def load_hardware(self):
    address = self.__get_address()
    if len(address) == 2:
      self._device = SmartStrip(address[0])
    else:
      self._device = SmartPlug(address[0])

  def set_hardware_state(self, state, force = False):

    async def __set_hardware_state(device,address,state):
      await device.update()
      strip = len(address) == 2
      plug = (device if not strip else device.plugs[int(address[1])-1])
      if state is True:
        await plug.turn_on()
      else:
        await plug.turn_off()

      return True

    address = self.__get_address()
    try:
      asyncio.run(__set_hardware_state(self._device,address,state))
      return True
    except RuntimeError as err:
      return True

  def get_hardware_state(self):
    data = []

    async def __get_hardware_state(device,address):
      await device.update()
      strip = len(address) == 2
      if strip:
        data.append(device.plugs[int(address[1])-1].is_on)
      else:
        data.append(device.is_on)

    address = self.__get_address()
    try:
      asyncio.run(__get_hardware_state(self._device,address))
    except RuntimeError as err:
      return None

    return len(data) == 1 and terrariumUtils.is_true(data[0])

  @staticmethod
  def scan_power_switches(callback=None, **kwargs):
    found_devices = []

    async def scan():
      devices = await Discover.discover()
      for ip_address in devices:
        device = devices[ip_address]
        await device.update()
        if device.is_strip:
          for counter in range(1,len(device.plugs)+1):
            found_devices.append(terrariumPowerSwitchTPLinkKasa(
                                    md5(('{}{}{}'.format(terrariumPowerSwitchTPLinkKasa.TYPE,device.device_id,counter)).encode()).hexdigest(),
                                    '{},{}'.format(device.host,counter),
                                    device.plugs[counter-1].alias,
                                    None,
                                    callback))

        else:
          found_devices.append(terrariumPowerSwitchTPLinkKasa(
                                  md5(('{}{}'.format(terrariumPowerSwitchTPLinkKasa.TYPE,device.device_id)).encode()).hexdigest(),
                                  '{}'.format(device.host),
                                  device.alias,
                                  None,
                                  callback))
    try:
      asyncio.run(scan())
    except RuntimeError as err:
      pass

    for device in found_devices:
       yield device
