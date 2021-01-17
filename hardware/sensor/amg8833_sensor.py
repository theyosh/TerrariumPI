from . import terrariumI2CSensor
from terrariumUtils import terrariumUtils

# pip install melopero-amg8833
import melopero_amg8833

class terrariumAMG8833Sensor(terrariumI2CSensor):
  HARDWARE = 'amg8833'
  TYPES    = ['temperature']
  NAME     = 'AMG8833 Grid-Eye IR Thermometer sensor'

  def _load_hardware(self):
    address = self._address
    device = melopero_amg8833.AMGGridEye(address[0],1 if len(address) == 1 or int(address[1]) < 1 else int(address[1]))
    device.set_fps_mode(melopero_amg8833.AMGGridEye.FPS_1_MODE)
    return device

  def _get_data(self):
    data = {}
    self.device.update_pixel_temperature_matrix()
    time.sleep(0.1)
    data['temperature'] = float(self.device.get_thermistor_temperature())
    return data