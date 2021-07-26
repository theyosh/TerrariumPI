from . import terrariumRelay, terrariumRelayException
from terrariumUtils import terrariumUtils, terrariumCache

import subprocess
import re

class terrariumRelayDenkoviV2(terrariumRelay):
  HARDWARE = 'denkovi_v2'
  NAME = None # This sensor can not be selected directly. This is also a kind of abstract class

  # TODO: Fix path here to an absolute path and check if installed. If so, add scanning option
  __CMD = '/usr/bin/sudo /usr/bin/java -jar 3rdparty/DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar'.split(' ')

  def __get_relay_count(self):
    return int(self.HARDWARE.split('_')[-1])

  def __get_board_type(self):
    return '{}{}'.format(self.__get_relay_count(), self._device['type'])

  def _load_hardware(self):
    self.__cache = terrariumCache()
    address = self._address
    if len(address) == 1:
       address.append(1)
    elif address[1] is None or '' == address[1]:
      address[1] = 1

    if terrariumUtils.is_float(address[1]):
      address[1] -= 1 # Reduce board number by one, human start counting at 1, computers at 0 (zero)

    scan_regex = r'^(?P<serial>[^ ]+)\W(\[(?P<device>[^\]]+\]))\W\[id=\d\]$'
    number_mode = terrariumUtils.is_float(address[1])
    counter = 0

    cmd = self.__CMD + ['list']

    try:
      data = subprocess.check_output(cmd).strip().decode('utf-8').strip().split('\n')
    except subprocess.CalledProcessError as ex:
      # Device does not exists....
      return False

    #print(data)

    for line in data:
      line = re.match(scan_regex,line)
      if line is not None:
        line = line.groupdict()

        if (number_mode and counter != address[1]) or (not number_mode and address[1] != line['serial']):
          counter += 1
          continue

        self._device['device'] = line['serial']
        self._device['type']   = 'v2' if 'mcp' in line['device'].lower() else ''
        self._device['switch'] = int(address[0])
        if self._device['switch'] == 0:
          self._device['switch'] = self.__get_relay_count()

        # TODO: Do we make an address update so we have always the serial of the device instead of the number.... will fix USB replug issues and/or order changes...
        self.address = '{},{}'.format(self._device['switch'],self._device['device'])
        break

    return self._device['device']

  def _get_hardware_value(self):
    cache_key = self._relay_cache_key
    data = self.__cache.get_data(cache_key)

    if data is None and not self.__cache.is_running(cache_key):
      self.__cache.set_running(cache_key)
      cmd = self.__CMD + [self._device['serial'], self.__get_board_type(), 'all', 'status']

      data = subprocess.check_output(cmd).strip().decode('utf-8').strip()
      #print('Got data: *{}*'.format(data))
      self.__cache.set_data(cache_key,data)
      self.__cache.clear_running(cache_key)

    if data is None:
      return None

    data = list(data)
    return self.ON if terrariumUtils.is_true(data[self._device['switch']]) else self.OFF

  def set_hardware_state(self, state, force = False):
    cache_key = self._relay_cache_key
    cmd = self.__CMD + [self._device['serial'], self.__get_board_type(), str(self._device['switch']), str(1 if state is self.ON else 0)]

    data = subprocess.check_output(cmd).strip().decode('utf-8').strip()
    # Data should contain the current relay status for all relais...
    self.__cache.set_data(cache_key,data)
    return True

class terrariumRelayDenkoviV2_4(terrariumRelayDenkoviV2):
  HARDWARE = 'denkovi_v2_4'
  NAME = 'Denkovi Relay v2 (4 sockets)'

class terrariumRelayDenkoviV2_8(terrariumRelayDenkoviV2):
  HARDWARE = 'denkovi_v2_8'
  NAME = 'Denkovi Relay v2 (8 sockets)'

class terrariumRelayDenkoviV2_16(terrariumRelayDenkoviV2):
  HARDWARE = 'denkovi_v2_16'
  NAME = 'Denkovi Relay v2 (16 sockets)'