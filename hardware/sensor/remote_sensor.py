from . import terrariumSensor, terrariumSensorLoadingException
from terrariumUtils import terrariumUtils

class terrariumRemoteSensor(terrariumSensor):
  HARDWARE = 'remote'
  # Empty TYPES list as this will be filled with all available hardware TYPES
  TYPES    = []
  NAME     = 'Remote sensor (http/https)'

  def _load_hardware(self):
    if terrariumUtils.is_valid_url(self.address):
      device = self.address
      return device
    else:
      raise terrariumSensorLoadingException('Not a valid url.')

  def _get_data(self):
    data = {}
    data[self.sensor_type] = terrariumUtils.get_remote_data(self.device)
    return data