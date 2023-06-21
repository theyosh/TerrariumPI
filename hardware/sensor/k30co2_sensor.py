# -*- coding: utf-8 -*-
from . import terrariumSensor

import serial
from gevent import sleep

# https://computenodes.net/2017/08/18/__trashed-4/ , https://github.com/theyosh/TerrariumPI/issues/177
# pip install pyserial


class terrariumK30CO2Sensor(terrariumSensor):
    HARDWARE = "k30co2"
    TYPES = ["co2"]
    NAME = "K30 CO2 Sensor"

    def _load_hardware(self):
        with serial.Serial(self.address, baudrate=9600, timeout=1) as device:
            device.flushInput()
            return device

    def _get_data(self):
        data = None
        with self.device as sensor:
            sensor.write(b"\xFE\x44\x00\x08\x02\x9F\x25")
            # Give the sensor some time to warm up
            sleep(0.5)
            response = sensor.read(7)
            high = float(response[3])
            low = float(response[4])
            data = {}
            data["co2"] = int((high * 256) + low)

        return data
