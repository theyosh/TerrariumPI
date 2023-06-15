# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

# https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bh1750.py


class terrariumBH1750Sensor(terrariumI2CSensor):
    HARDWARE = "bh1750"
    TYPES = [
        "light",
    ]
    NAME = "BH1750 LUX light sensor"

    # Start measurement at 4lx resolution. Time typically 16ms.
    CONTINUOUS_LOW_RES_MODE = 0x13
    # Start measurement at 1lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_1 = 0x10
    # Start measurement at 0.5lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_LOW_RES_MODE = 0x23

    def _get_data(self):
        data = None
        with self._open_hardware() as i2c_bus:
            value = i2c_bus.read_i2c_block_data(self.device[0], self.ONE_TIME_HIGH_RES_MODE_1, 2)

            data = {}
            data["light"] = (value[1] + (256 * value[0])) / 1.2

        return data
