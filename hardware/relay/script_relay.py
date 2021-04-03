from . import terrariumRelay, terrariumRelayLoadingException
from terrariumUtils import terrariumUtils

from pathlib import Path

class terrariumRelayScript(terrariumRelay):
  HARDWARE = 'script'
  NAME = 'External script switch'

  def _load_hardware(self):
    script = Path(self.address)
    if not script.exists():
      raise terrariumRelayLoadingException(f'Invalid script location for relay {self}: {self.address}')

    if oct(script.stat().st_mode)[-3:] not in ['777','775','755']:
      raise terrariumRelayLoadingException(f'Script {self.address} for relay {self} is not executable.')

    return self.address

  def _set_hardware_value(self, state):
    cmd = f'{self.address} {state}'

    try:
      data = terrariumUtils.get_script_data(cmd).decode('utf-8').strip()
    except subprocess.CalledProcessError as ex:
      # Device does not exists....
      return None

    return True

  def _get_hardware_value(self):
    try:
      data = terrariumUtils.get_script_data(self.address).decode('utf-8').strip()
      data = float(data)
    except subprocess.CalledProcessError as ex:
      # Device does not exists....
      return None

    return data