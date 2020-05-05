# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from terriumSwitch import terrariumPowerSwitchSource

from kasa import Discover

class terrariumPowerSwitchTPLinkKasa(terrariumPowerSwitchSource):
  TYPE = 'tplinkkasa'
  URL = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

  def __get_address(self):
    data = self.get_address().strip().explode(',')
    if len(data) == 2 and '' == data[1]:
      del(data[1])

    return data

  def load_hardware(self):
    address = self.__get_address()
    if len(address) == 2:
      self._device = kasa.smartplug.SmartStrip(address[0])
      self._device_type = 'strip'
    else:
      self._device = kasa.smartplug.SmartPlug(address[0])
      self._device_type = 'plug'

  def set_hardware_state(self, state, force = False):
    address = self.__get_address()
    strip = len(address) == 2

    if state is terrariumPowerSwitch.ON:
      if strip:
        #await self._device.plugs[address[1]].turn_on()
        self._device.plugs[address[1]].turn_on()
      else:
        #await self._device.turn_off()
        self._device.turn_off()
    else:
      if strip:
        #await self._device.plugs[address[1]].turn_off()
        self._device.plugs[address[1]].turn_off()
      else:
        #await self._device.turn_off()
        self._device.turn_off()

  def get_hardware_state(self):
    address = self.__get_address()
    strip = len(address) == 2

    data = None
    try:
      #await self._device.update()
      self._device.update()
      if strip:
        data = self._device.plugs[address[1]].is_on
      else:
        data =  self._device.is_on

      print('Current state:')
      print(self._device)
      print(data)

    except Exception as err:
      # Ignore for now
      print(err)

    return terrariumPowerSwitch.ON if 'ON' == data or terrariumUtils.is_true(data) else terrariumPowerSwitch.OFF

  @staticmethod
  def scan_power_switches(callback=None, **kwargs):

    async def scan():
      print('Start scanning.....')
      devices = await Discover.discover()
      for device in devices:
        print('Found device')
        print(device)
        print(dir(device))
        if device.is_strip:
          # First do an update to get the total amount of power switches
          await device.update()
          for counter in range(1,len(device.plugs)+1):
            yield terrariumPowerSwitch(md5((terrariumPowerSwitchTPLinkKasa.TYPE + device.device_id + counter).encode()).hexdigest(),
                                      terrariumPowerSwitchTPLinkKasa.TYPE,
                                      '{},{}'.format(device.host,counter),
                                      device.plugs[counter-1].alias,
                                      None,
                                      callback)

#      sleep(1)
      print('Done scanning')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(scan())
    loop.close()

#     print('Scan kasa switches')
#     loop = asyncio.get_event_loop()
#     devices = loop.run_until_complete(kasa.Discover.discover().values())

# #    for device in kasa.Discover.discover().values():
#     for device in devices:
#       print('Found device')
#       print(device)
#       print(dir(device))

#       if device.is_plug:
#         yield terrariumPowerSwitch(md5((terrariumPowerSwitchTPLinkKasa.TYPE + device.device_id).encode()).hexdigest(),
#                                   terrariumPowerSwitchTPLinkKasa.TYPE,
#                                   device.host,
#                                   device.alias,
#                                   None,
#                                   callback)
#       elif device.is_strip:
#         
#         #await device.update()
#         device.update()
#         for counter in range(1,len(device.plugs)+1):
#           yield terrariumPowerSwitch(md5((terrariumPowerSwitchTPLinkKasa.TYPE + device.device_id + counter).encode()).hexdigest(),
#                                     terrariumPowerSwitchTPLinkKasa.TYPE,
#                                     '{},{}'.format(device.host,counter),
#                                     device.plugs[counter-1].alias,
#                                     None,
#                                     callback)

