# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

from gevent import sleep


class terrariumHIH8000Sensor(terrariumI2CSensor):
    HARDWARE = "hih8000"
    TYPES = ["temperature", "humidity"]
    NAME = "Honeywell HumidIcon HIH8000"

    def _get_data(self):
        data = None

        with self._open_hardware() as i2c_bus:
            i2c_bus.write_quick(self.device[0])
            sleep(0.04)
            raw_data = i2c_bus.read_i2c_block_data(self.device[0], 0, 4)

            data = {}
            data["humidity"] = ((raw_data[0] & 0x3F) * 256 + raw_data[1]) / float(0x3FFE) * 100
            data["temperature"] = ((raw_data[2] * 256 + raw_data[3]) >> 2) / float(0x3FFE) * 165 - 40

        return data
