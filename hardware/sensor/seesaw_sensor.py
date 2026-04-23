# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

# pip install adafruit-circuitpython-seesaw
import board
from adafruit_seesaw.seesaw import Seesaw


class terrariumSeesawSensor(terrariumI2CSensor):
    HARDWARE = "seesaw"
    TYPES = ["temperature", "moisture"]
    NAME = "Seesaw soil sensor"

    def _load_hardware(self):
        # Only using default I2C bus
        return Seesaw(board.I2C(), self._address[0])

    def _get_data(self):

        return {"temperature": float(self.device.get_temp()), "moisture": float(self.device.moisture_read())}
