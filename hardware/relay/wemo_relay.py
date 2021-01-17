from . import terrariumRelay, terrariumRelayLoadingException
from terrariumUtils import terrariumUtils

# pip install pywemo
import pywemo
from hashlib import md5

class terrariumRelayWeMo(terrariumRelay):
  HARDWARE = 'wemo'
  NAME = 'WEMO Smart plug'

  # TODO: Figure out if the retry wrapper still works...
  # This will update the device based in mac address
  def load_hardware(self):
    super().load_hardware()
    # Always overule the ID generating, as we want to use the MAC as that is unique if the IP address is changing
    self.id = md5(f'{self.HARDWARE}{self.device.mac.lower()}'.encode()).hexdigest()

  def _load_hardware(self):
    port = pywemo.ouimeaux_device.probe_wemo(self.address,probe_timeout=3)
    if port is None:
      raise terrariumRelayLoadingException(f'Relay {self} is not found')

    device = pywemo.discovery.device_from_description(f'http://{self.address}:{port}/setup.xml', None)
    return device

  def _set_hardware_value(self, state):
    if state == self.ON:
      self.device.on()
    else:
      self.device.off()

    # Always return True here, as this should indicate the toggle changed succeeded
    return True

  def _get_hardware_value(self):
    self.device.reconnect_with_device()
    data = self.device.get_state()
    if data is None:
      return None

    return self.ON if terrariumUtils.is_true(data) else self.OFF

  @staticmethod
  def _scan_relays(callback=None, **kwargs):
    for device in pywemo.discover_devices():
      yield terrariumRelay(None,
                           terrariumRelayWeMo.HARDWARE,
                           device.host,
                           f'{terrariumRelayWeMo.NAME} {device.name} device ip: {device.host}({device.mac})',
                           callback=callback)