from . import terrariumSensor, terrariumSensorLoadingException
from terrariumUtils import terrariumUtils

class terrariumScriptSensor(terrariumSensor):
  HARDWARE = 'script'
  # Empty TYPES list as this will be filled with all available hardware TYPES
  TYPES    = []
  NAME     = 'Script sensor'

def _load_hardware(self):
  if Path(self.address).exists():
    device = self.address
    return device
  else:
    raise terrariumSensorLoadingException('Not a valid script path.')

def _get_data(self):
  data = {}
  data[self.sensor_type] = terrariumUtils.get_script_data(self.device)
  return data