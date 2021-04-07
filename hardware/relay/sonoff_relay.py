from . import terrariumRelay, terrariumRelayLoadingException
from terrariumUtils import terrariumUtils

from zeroconf import ServiceBrowser, Zeroconf
from gevent import sleep
from hashlib import md5
import re

# pip install zeroconf
# https://github.com/jstasiak/python-zeroconf
# https://python-zeroconf.readthedocs.io/
# Needs mDNS: https://tasmota.github.io/docs/Commands/#setoption55 => SO55 1

class terrariumRelaySonoff(terrariumRelay):
  HARDWARE = 'sonoff'
  NAME = 'Sonoff (Tasmota)'

  __URL_REGEX = re.compile(r'^(?P<protocol>https?):\/\/((?P<user>[^:]+):(?P<passwd>[^@]+)@)?(?P<host>[^#\/]+)(\/)?(#(?P<nr>\d+))?$',re.IGNORECASE)
  __SCAN_TIME = 5

  @property
  def _address(self):
    address = None
    data = self.__URL_REGEX.match(self.address)
    if data:
      address = data.groupdict()
      if 'nr' not in address or address['nr'] is None or '' == address['nr']:
        address['nr'] = 1

      address['nr'] = int(address['nr'])
    else:
      raise terrariumRelayLoadingException(f'Incorrect address for a Sonoff device: {self}')

    return address

  # This will update the device based in mac address
  def load_hardware(self):
    super().load_hardware()
    # Bad choice: But reload the hardware once more to get the right mac address for unique ID. aKa forcing reloading, ignoring the hardware cache
    self._load_hardware()

  def _load_hardware(self):
    # Input format should be either:
    # - http://[HOST]#[POWER_SWITCH_NR]
    # - http://[HOST]/#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]/#[POWER_SWITCH_NR]

    address = self._address

    # Try Tasmota
    # http://sonoff/cm?cmnd=Power[POWER_SWITCH_NR]%201
    # http://sonoff/cm?cmnd=Power[POWER_SWITCH_NR]%200
    # http://sonoff/cm?user=admin&password=joker&cmnd=Power[POWER_SWITCH_NR]%201

    device = f'{address["protocol"]}://{address["host"]}/cm?'

    if 'user' in address and 'password' in address:
      device += f'user={address["user"]}&password={address["password"]}&'

    device += 'cmnd='
    state = terrariumUtils.get_remote_data(f'{device}Status%200')

    if state is None:
      return None

    # Always overule the ID generating, as we want to use the MAC as that is unique if the IP address is changing
    self.id = md5(f'{self.HARDWARE}{state["StatusNET"]["Mac"].lower()}'.encode()).hexdigest()

    return device

  def _set_hardware_value(self, state):
    action = 1 if state == self.ON else 0
    url = f'{self.device}Power{self._address["nr"]}%20{action}'
    data = terrariumUtils.get_remote_data(url)

    if data is None:
      return False

    return state == (self.ON if terrariumUtils.is_true(data['POWER']) else self.OFF)

  def _get_hardware_value(self):
    url = f'{self.device}Power{self._address["nr"]}'
    data = terrariumUtils.get_remote_data(url)

    if data is None:
      return None

    if 'POWER' in data:
      data = data['POWER']
    elif f'POWER{self._address["nr"]}' in data:
      data = data[f'POWER{self._address["nr"]}']

    return self.ON if terrariumUtils.is_true(data) else self.OFF

  @staticmethod
  def _scan_relays(callback=None, **kwargs):
    found_devices = []

    class Listener():
      def remove_service(self, zeroconf, type, name):
        pass

      def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        # Check for Tasmota firmware...
        address = f'{info.parsed_addresses()[0]}:{info.port}'
        data = terrariumUtils.get_remote_data(f'http://{address}/cm?cmnd=Status')
        if data is not None:
          for switch_nr in range(len(data['Status']['FriendlyName'])):
            found_devices.append(terrariumRelay(None,
                                                terrariumRelaySonoff.HARDWARE,
                                                f'http://{address}#{switch_nr+1}',
                                                f'{terrariumRelaySonoff.NAME} {data["Status"]["FriendlyName"][switch_nr]}({switch_nr+1}) device ip: {address}',
                                                callback=callback) )

    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", Listener())
    sleep(terrariumRelaySonoff.__SCAN_TIME)
    zeroconf.close()

    for device in found_devices:
       yield device