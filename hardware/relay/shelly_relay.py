from . import terrariumRelay, terrariumRelayLoadingException
from terrariumUtils import terrariumCache, terrariumUtils

from hashlib import md5
import re

class terrariumRelayShelly(terrariumRelay):
  HARDWARE = 'shelly'
  NAME = 'Shelly'

  __URL_REGEX = re.compile(r'^(?P<protocol>https?):\/\/((?P<user>[^:]+):(?P<passwd>[^@]+)@)?(?P<host>[^#\/]+)(\/)?(#(?P<nr>\d+))?$',re.IGNORECASE)

  @property
  def _address(self):
    address = None
    data = self.__URL_REGEX.match(self.address)
    if data:
      address = data.groupdict()
      if 'nr' not in address or address['nr'] is None or '' == address['nr']:
        address['nr'] = 0

      address['nr'] = int(address['nr'])-1
    else:
      raise terrariumRelayLoadingException(f'Incorrect address for a Shelly device: {self}')

    return address

  # This will update the device based in mac address
  #def load_hardware(self):
  #  super().load_hardware()
  #  # Bad choice: But reload the hardware once more to get the right mac address for unique ID. aKa forcing reloading, ignoring the hardware cache
  #  self._load_hardware()

  def _load_hardware(self):
    # Input format should be either:
    # - http://[HOST]#[POWER_SWITCH_NR]
    # - http://[HOST]/#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]/#[POWER_SWITCH_NR]

    address = self._address
    device = f'{address["protocol"]}://{address["host"]}'

    if 'user' in address and 'password' in address:
      device = f'{address["protocol"]}://{address["user"]}:{address["password"]}@{address["host"]}'


    device += f'/relay/{self._address["nr"]}'

    print('Device')
    print(device)

    data = terrariumUtils.get_remote_data(device)

    if data is None:
      return None

    # Create the cache key for caching the relay states.
    # This is usefully when there are more then 1 relay per hardware device.
    # self.__cache_key = md5(f'{self.HARDWARE}{address["host"].lower()}'.encode()).hexdigest()
    # self.__cache = terrariumCache()
    # self.__cache.set_data(self.__cache_key, state['relays'], self._CACHE_TIMEOUT)

    # We need the use the address_nr value also, as there can multiple relays per sonoff device.
#    if self._device['id'] is None:
#      self.id = md5(f'{self.HARDWARE}{state["StatusNET"]["Mac"].lower()}{address["nr"]}'.encode()).hexdigest()


    return device

  def _set_hardware_value(self, state):
    action = 'on' if state == self.ON else 'off'
    url = f'{self.device}?turn={action}'
    print(f'Set hardware url: {url}')
    data = terrariumUtils.get_remote_data(url)

    if data is None:
      return False

    if 'ison' in data:
      data = data['ison']

    return state == (self.ON if terrariumUtils.is_true(data) else self.OFF)

  def _get_hardware_value(self):

    # data = self.__cache.get_data(self.__cache_key)
    # if data is None:
    #   # Cache is expired, so we update with new data
    #   # Get the overall state information
    #   url = f'{self.device}status'
    #   print(f'Get hardware url: {url}')
    #   data = terrariumUtils.get_remote_data(url)

    #   if data is None:
    #     return None

    #   self.__cache.set_data(self.__cache_key, data['relays'], self._CACHE_TIMEOUT)

    data = terrariumUtils.get_remote_data(self.device)

    if data is None:
      return None

    if 'ison' in data:
      data = data['ison']

    return self.ON if terrariumUtils.is_true(data) else self.OFF