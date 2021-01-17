from . import terrariumRelay, terrariumRelayException
from terrariumUtils import terrariumUtils

import asyncio
from kasa import Discover, SmartStrip, SmartPlug

# pip install asyncio
# pip install python-kasa

class terrariumRelayTPLinkKasa(terrariumRelay):
  HARDWARE = 'tplinkkasa'
  NAME = 'Kasa Smart'

  URL = '^\d{1,3}\.\d{1,3}\.\d{1,3}(,\d{1,3})?$'

  def _load_hardware(self):
    # Input format should be either:
    # - http://[HOST]#[POWER_SWITCH_NR]
    # - http://[HOST]/#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]/#[POWER_SWITCH_NR]

    address = self._address
    if len(address) == 2:
      self._device['device'] = SmartStrip(address[0])
    else:
      self._device['device'] = SmartPlug(address[0])


    return self._device['device']

  def _set_hardware_value(self, state, force = False):

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
      asyncio.run(__set_hardware_state(self._device['device'],address,state))
      return True
    except RuntimeError as err:
      return True

  def _get_hardware_value(self):
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
      asyncio.run(__get_hardware_state(self._device['device'],address))
    except RuntimeError as err:
      return None

    return self.ON if len(data) == 1 and terrariumUtils.is_true(data[0]) else self.OFF

  @staticmethod
  def _scan_relays(callback=None, **kwargs):
    found_devices = []

    async def scan():
      devices = await Discover.discover()
      for ip_address in devices:
        device = devices[ip_address]
        await device.update()
        if device.is_strip:
          for counter in range(1,len(device.plugs)+1):
            found_devices.append(terrariumRelayTPLinkKasa(None,
                                                                '{},{}'.format(device.host,counter),
                                                                device.plugs[counter-1].alias,
                                                                callback=callback))

        else:
          found_devices.append(terrariumRelayTPLinkKasa(None,
                                                              '{}'.format(device.host),
                                                              device.alias,
                                                              callback=callback))
    try:
      asyncio.run(scan())
    except RuntimeError as err:
      pass

    for device in found_devices:
       yield device
