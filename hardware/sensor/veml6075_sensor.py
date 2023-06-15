# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

# pip install veml6075
import veml6075


class terrariumVEML6075Sensor(terrariumI2CSensor):
    HARDWARE = "veml6075"
    TYPES = ["uva", "uvb", "uvi"]
    NAME = "VEML6075 UVA and UVB light sensor"

    def _get_data(self):
        data = None
        with self._open_hardware() as i2c_bus:
            sensor = veml6075.VEML6075(i2c_addr=self.device[0], i2c_dev=i2c_bus)
            sensor.set_shutdown(False)
            sensor.set_high_dynamic_range(False)
            sensor.set_integration_time("100ms")

            uva, uvb = sensor.get_measurements()
            uv_comp1, uv_comp2 = sensor.get_comparitor_readings()
            uv_indices = sensor.convert_to_index(uva, uvb, uv_comp1, uv_comp2)

            data = {}
            data["uva"] = uva
            data["uvb"] = uvb
            data["uvi"] = max(0, uv_indices[2])  # Do not allow lower then zero

        return data
