from . import terrariumSensor
from terrariumUtils import terrariumUtils

from gpiozero import DigitalInputDevice

class terrariumYTXXSensorDigital(terrariumSensor):
  HARDWARE = 'ytxx-digital'
  TYPES    = ['moisture']
  NAME     = 'YT-69 sensor (digital)'

  def _load_hardware(self):
    address = self._address
    if len(address) >= 2 and terrariumUtils.is_float(address[1]):
      # Set / enable power management
      self._device['power_mngt'] = terrariumUtils.to_BCM_port_number(address[1])

    device = DigitalInputDevice(terrariumUtils.to_BCM_port_number(address[0]))
    return device

  def _get_data(self):
    data = {}
    data['moisture'] = 0 if self.device.is_active else 100
    return data

  def stop(self):
    self.device.close()
    super().stop()