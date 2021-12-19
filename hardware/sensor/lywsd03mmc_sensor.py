from . import terrariumBluetoothSensor

# pip install lywsd03mmc
from lywsd03mmc import Lywsd03mmcClient

class terrariumLywsd03mmcSensor(terrariumBluetoothSensor):
  HARDWARE = 'LYWSD03MMC'
  TYPES    = ['temperature','humidity']
  NAME     = 'LYWSD03MMC bluetooth sensor'

  def _load_hardware(self):
    address = self._address
    device = Lywsd03mmcClient(address[0])
    return device

  def _get_data(self):
    data = {}

    # BUG: Firmware data en battery will only be set at the first measurement.
    #self._device['firmware'] = self._device['device'].firmware_version()
    #self._device['battery']  = self._device['device'].parameter_value(MI_BATTERY)

    data['temperature'] = self.device.temperature
    data['humidity']    = self.device.humidity
    data['battery']     = self.device.battery

    return data

  @staticmethod
  def _scan_sensors(unit_value_callback = None, trigger_callback = None):
    for sensor in terrariumBluetoothSensor._scan_sensors(__class__, ['mj_ht_v1'], unit_value_callback, trigger_callback):
      yield sensor
