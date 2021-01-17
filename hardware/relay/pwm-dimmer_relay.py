from . import terrariumRelay, terrariumRelayDimmer, terrariumRelayException
from terrariumUtils import terrariumUtils

# pip install gpiozero
from gpiozero import PWMOutputDevice

class terrariumRelayDimmerPWM(terrariumRelayDimmer):
  HARDWARE = 'pwm-dimmer'
  NAME = None

  _DIMMER_FREQ = 1000 # In Hz

  def _load_hardware(self):
    return PWMOutputDevice(terrariumUtils.to_BCM_port_number(self.address),frequency=self._DIMMER_FREQ)

  def _set_hardware_value(self, state):
    self.device.value = float(state) / 100.0
    return True

  def _get_hardware_value(self):
    return round(self.device.value * 100.0)

  def stop(self):
    self.device.close()

class terrariumRelayDimmerNextEVO(terrariumRelayDimmerPWM):
  HARDWARE = 'nextevo-dimmer'
  NAME = 'NextEVO Universal AC MAINS Dimmer (MPDMv4.1)'

  # PWM dimmer settings
  # According to http://www.esp8266-projects.com/2017/04/raspberry-pi-domoticz-ac-dimmer-part-1/
  # is 860 DIM value equal to 95% dimming -> 905 is 100% dimming -> But at after 860 you can't see it working... so 860 is fine!
  # DIMMER_MAXDIM = 860
  _DIMMER_FREQ   = 5000

  def _load_hardware(self):
    return PWMOutputDevice(terrariumUtils.to_BCM_port_number(self.address),active_high=False,frequency=self._DIMMER_FREQ)

class terrariumRelayDimmerDC(terrariumRelayDimmerPWM):
  HARDWARE = 'dc-dimmer'
  NAME = 'DC Dimmer'

  # DC dimmer settings
  #DIMMER_MAXDIM = 1000 # https://github.com/theyosh/TerrariumPI/issues/178#issuecomment-412667010
  _DIMMER_FREQ   = 15000 # https://github.com/theyosh/TerrariumPI/issues/178#issuecomment-413697246

class terrariumRelayDimmerIRF520(terrariumRelayDimmerPWM):
  # https://opencircuit.nl/Product/IRF520-mosfet-module
  # https://github.com/DrLex0/MightyVariableFan/blob/master/pi_files/pwm_server.py#L97
  HARDWARE = 'irf520-dimmer'
  NAME = 'IRF520 Dimmer'

  # # Dimmer settings
  #DIMMER_MAXDIM = 100
  _DIMMER_FREQ   = 10000 # Tested with a 12V PC fan. Low freq. caused some high pitching noise