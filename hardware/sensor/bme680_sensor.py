# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

# pip install bme680
import bme680


class terrariumBME680Sensor(terrariumI2CSensor):
    HARDWARE = "bme680"
    TYPES = ["temperature", "humidity", "altitude", "pressure"]
    NAME = "BME680 sensor"

    def _get_data(self):
        data = None
        with self._open_hardware() as i2c_bus:
            sensor = bme680.BME680(self.device[0], i2c_bus)

            if sensor.get_sensor_data():
                data = {}
                data["temperature"] = sensor.data.temperature
                data["humidity"] = sensor.data.humidity
                data["pressure"] = sensor.data.pressure
                # What to do with this data...
                data["gas"] = sensor.data.gas_resistance

                # https://github.com/avislab/sensorstest/blob/master/BME280/BME280.py#L176
                data["altitude"] = data["pressure"] / 101325.0
                data["altitude"] = 1 - pow(data["altitude"], 0.19029)
                data["altitude"] = round(44330.0 * data["altitude"], 3)

        return data
