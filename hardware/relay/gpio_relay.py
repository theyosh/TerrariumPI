from . import terrariumRelay, terrariumRelayException
from terrariumUtils import terrariumUtils

# pip install gpiozero
from gpiozero import LED

class terrariumRelayGPIO(terrariumRelay):
  HARDWARE = 'gpio'
  NAME = 'GPIO devices'

  def _load_hardware(self):
    return LED(terrariumUtils.to_BCM_port_number(self._address[0]))

  def _set_hardware_value(self, state):
    if state == self.ON:
      self.device.on()
    else:
      self.device.off()

    return True

  def _get_hardware_value(self):
    return self.ON if terrariumUtils.is_true(self.device.is_lit) else self.OFF

  def stop(self):
    self.device.close()
    super().stop()

class terrariumRelayGPIOInverse(terrariumRelayGPIO):
  HARDWARE = 'gpio-inverse'
  NAME = 'GPIO devices (inverse)'

  def _load_hardware(self):
    return LED(terrariumUtils.to_BCM_port_number(self._address[0]), active_high=False)