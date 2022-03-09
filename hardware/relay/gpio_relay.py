from . import terrariumRelay
from terrariumUtils import terrariumUtils

# pip install gpiozero
from gpiozero import LED

from hardware.io_expander import terrariumIOExpander

class terrariumRelayGPIO(terrariumRelay):
  HARDWARE = 'gpio'
  NAME = 'GPIO devices'

  def _load_hardware(self):
    address = self._address

    if len(address) >= 2:
      # IO Expander in use... Only valid for motion and magnetic... LDR seems not suitable at the moment
      device = None
      if address[0].lower().startswith('pcf8575-'):
        device = terrariumIOExpander('PCF8575',','.join(address[1:]))
      elif address[0].lower().startswith('pcf8574-'):
        device = terrariumIOExpander('PCF8574',','.join(address[1:]))

      if device is not None:
        device.set_pin(int(address[0].split('-')[1]))

      return device

    else:
      return LED(terrariumUtils.to_BCM_port_number(self._address[0]))

  def _set_hardware_value(self, state):
    if isinstance(self._device['device'], terrariumIOExpander):
      self._device['device'].state = (state == self.ON)

    else:
      if state == self.ON:
        self.device.on()
      else:
        self.device.off()

    return True

  def _get_hardware_value(self):
    if isinstance(self._device['device'], terrariumIOExpander):
      # IO Expander in use
      state = self._device['device'].state
      if state is None:
        # Device in error...
        return None
      else:
        return self.ON if state else self.OFF

    else:
      return self.ON if terrariumUtils.is_true(self.device.is_lit) else self.OFF

  def stop(self):
    self.device.close()
    super().stop()

class terrariumRelayGPIOInverse(terrariumRelayGPIO):
  HARDWARE = 'gpio-inverse'
  NAME = 'GPIO devices (inverse)'

  def _load_hardware(self):
    return LED(terrariumUtils.to_BCM_port_number(self._address[0]), active_high=False)

  def _set_hardware_value(self, state):
    if isinstance(self._device['device'], terrariumIOExpander):
      state = not state

    return super()._set_hardware_value(state)

  def _get_hardware_value(self):
    state = super()._get_hardware_value()
    if isinstance(self._device['device'], terrariumIOExpander):
      state = not state

    return state
