# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

import struct


class terrariumArduinoSensor(terrariumI2CSensor):
    # [block_data],[I2C Address],[I2C Bus number]
    HARDWARE = "Arduino"
    TYPES = ["distance", "temperature", "co2"]
    NAME = "Arduino Sensor"

    __I2C_READ = 0x00

    @property
    def _address(self):
        address = super()._address
        if len(address) > 1:
            address = [address[1], address[2], address[0]] if len(address) != 2 else [address[1], 1, address[0]]

        if isinstance(address[0], str):
            if not address[0].startswith("0x"):
                address[0] = "0x" + address[0]
            address[0] = int(address[0], 16)
        return address

    def _get_data(self):
        data = None
        address = self._address
        sensor_pos = 0 if len(address) != 3 else int(address[2])
        with self._open_hardware() as i2c_bus:
            bytedata = i2c_bus.read_i2c_block_data(address[0], sensor_pos, 4)
            value = bytes(bytedata[0:])

            float_value = struct.unpack("!f", value)[0]
            int_value = struct.unpack("!i", value)[0]

            data = {}
            data["distance"] = float_value
            data["temperature"] = int_value
            data["co2"] = int_value

        return data
