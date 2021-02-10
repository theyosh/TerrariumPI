from . import terrariumRelay, terrariumRelayDimmer, terrariumRelayException
from terrariumUtils import terrariumUtils

# pip install PCA9685-driver
# pip uninstall smbus-cffi
import pca9685_driver

class terrariumRelayDimmerPCA9685(terrariumRelayDimmer):
  HARDWARE = 'pca9685-dimmer'
  NAME = 'PCA9685-dimmer'

  # Dimmer settings
  _DIMMER_FREQ   = 1000
  _DIMMER_MAXDIM = 4095

  def _load_hardware(self):
    address = self._address
    if len(address) == 1:
      address.append(1)

    self._device['switch'] = int(address[0] if address[0].startswith('0x') else '0x' + address[0],16)
    self._device['device'] = pca9685_driver.Device(self._device['switch'], int(address[1]))
    self._device['device'].set_pwm_frequency(self._DIMMER_FREQ)

    return self._device['device']

  def _set_hardware_value(self, state):
    dim_value = int(self._DIMMER_MAXDIM * (float(state) / 100.0))
    self._device['device'].set_pwm(self._device['switch'], dim_value)
    return True

  def _get_hardware_value(self):
    return round((1 - self._device['device'].get_pwm(self._device['switch']) / 1000 / self._DIMMER_MAXDIM) * 100)