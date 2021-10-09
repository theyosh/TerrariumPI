from . import terrariumRelay, terrariumRelayDimmer, terrariumRelayLoadingException
from terrariumUtils import terrariumUtils

from pathlib import Path
import subprocess

class terrariumRelayScript(terrariumRelay):
  HARDWARE = 'script'
  NAME = 'Script relay'

  def _load_hardware(self):
    script = Path(self.address)
    if not script.exists():
      raise terrariumRelayLoadingException(f'Invalid script location for relay {self}: {self.address}')

    if oct(script.stat().st_mode)[-3:] not in ['777','775','755','744','544','554','555','550','540','770','750','740']:
      raise terrariumRelayLoadingException(f'Script {self.address} for relay {self} is not executable.')

    return self.address

  def _set_hardware_value(self, state):
    cmd = f'{self.address} {state}'

    try:
      terrariumUtils.get_script_data(cmd)
    except subprocess.CalledProcessError as ex:
      # Device does not exists....
      return None

    return True

  def _get_hardware_value(self):

    try:
      data = float(terrariumUtils.get_script_data(self.address).decode('utf-8').strip())

      # When the return value is -1, it means that there is not readout possible. So return the current state from memory
      if -1.0 == data:
        data = self.state
    except subprocess.CalledProcessError as ex:
      # Device does not exists....
      return None

    return self.ON if data != 0.0 else self.OFF

class terrariumDimmerScript(terrariumRelayDimmer):
  HARDWARE = 'script-dimmer'
  NAME = 'Script dimmer'

  def _load_hardware(self):
    script = Path(self.address)
    if not script.exists():
      raise terrariumRelayLoadingException(f'Invalid script location for relay {self}: {self.address}')

    if oct(script.stat().st_mode)[-3:] not in ['777','775','755','744','544','554','555','550','540','770','750','740']:
      raise terrariumRelayLoadingException(f'Script {self.address} for relay {self} is not executable.')

    return self.address

  def _set_hardware_value(self, state):
    cmd = f'{self.address} {state}'

    try:
      data = terrariumUtils.get_script_data(cmd).decode('utf-8').strip()
    except subprocess.CalledProcessError as ex:
      # Device does not exists....
      return None

    return state

  def _get_hardware_value(self):
    try:
      data = terrariumUtils.get_script_data(self.address).decode('utf-8').strip()
      data = float(data)

      # When the return value is -1, it means that there is not readout possible. So return the current state from memory
      if -1.0 == data:
        data = self.state
    except subprocess.CalledProcessError as ex:
      # Device does not exists....
      return None

    return data