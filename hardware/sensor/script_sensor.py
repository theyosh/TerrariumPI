# -*- coding: utf-8 -*-
from . import terrariumSensor, terrariumSensorLoadingException
from terrariumUtils import terrariumUtils

from pathlib import Path

class terrariumScriptSensor(terrariumSensor):
  HARDWARE = 'script'
  # Empty TYPES list as this will be filled with all available hardware TYPES
  TYPES    = []
  NAME     = 'Script sensor'

  def _load_hardware(self):
    script = Path(self.address)
    if not script.exists():
      raise terrariumSensorLoadingException(f'Invalid script location for sensor {self}: {self.address}')

    if oct(script.stat().st_mode)[-3:] not in ['777','775','755']:
      raise terrariumSensorLoadingException(f'Script {self.address} for sensor {self} is not executable.')

    return self.address

  def _get_data(self):
    data = {}
    try:
      data[self.sensor_type] = float(terrariumUtils.get_script_data(self.address).decode('utf-8').strip())
    except Exception:
      return None

    return data