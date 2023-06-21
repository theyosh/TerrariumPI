# -*- coding: utf-8 -*-
from . import terrariumI2CSensor, terrariumI2CSensorMixin


class terrariumSi7021Sensor(terrariumI2CSensor, terrariumI2CSensorMixin):
    HARDWARE = "si7021"
    TYPES = ["temperature", "humidity"]
    NAME = "SI7021 sensor"

    # Datasheet - https://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf
    TEMPERATURE_WAIT_TIME = 0.012  # (datasheet: typ=7, max=10.8 in ms)
    HUMIDITY_WAIT_TIME = 0.07  # (datasheet: typ=10, max=12 in ms) -> Not correct??
    SOFTRESET_TIMEOUT = 0.016  # (datasheet: typ=5, max=15 in ms)
