# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger("terrariumSensor")

from . import terrariumI2CSensor

# pip install py-AHTx0
import py_AHTx0

class terrariumATHx0Sensor(terrariumI2CSensor):
    HARDWARE = "athx0"
    TYPES = ["temperature", "humidity"]
    NAME = "Adafruit AHTX0 I2C sensor"

    def _load_hardware(self):
        device = py_AHTx0.AHTx0(self._address[1], self._address[0])
        if not device.calibrate():
            logger.warning(f"Failing to calibrate {self}")

        return device

    def _get_data(self):
        data = {
            "temperature": self.device.temperature,
            "humidity" : self.device.relative_humidity
        }

        return data