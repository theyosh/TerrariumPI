# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

# pip install RPi.bme280
import bme280


class terrariumBME280Sensor(terrariumI2CSensor):
    HARDWARE = "bme280"
    TYPES = ["temperature", "humidity", "altitude", "pressure"]
    NAME = "BME280 sensor"

    def _get_data(self):
        data = None
        with self._open_hardware() as i2c_bus:
            calibration_params = bme280.load_calibration_params(i2c_bus, self.device[0])

            # the sample method will take a single reading and return a
            # compensated_reading object
            sensor = bme280.sample(i2c_bus, self.device[0], calibration_params)

            # the compensated_reading class has the following attributes
            data = {}
            data["temperature"] = sensor.temperature
            data["humidity"] = sensor.humidity
            data["pressure"] = sensor.pressure

        # https://github.com/avislab/sensorstest/blob/master/BME280/BME280.py#L176
        data["altitude"] = data["pressure"] / 101325.0
        data["altitude"] = 1 - pow(data["altitude"], 0.19029)
        data["altitude"] = round(44330.0 * data["altitude"], 3)

        return data
