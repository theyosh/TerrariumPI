# -*- coding: utf-8 -*-
from . import terrariumSensor

import serial
from gevent import sleep

# https://github.com/UedaTakeyuki/mh-z19/blob/master/pypi/mh_z19/__init__.py
# https://www.circuits.dk/testing-mh-z19-ndir-co2-sensor-module/
# https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf
# https://www.winsen-sensor.com/d/files/MH-Z19B.pdf
# pip install pyserial


class terrariumMHZ19Sensor(terrariumSensor):
    HARDWARE = "mh-z19"
    TYPES = ["co2", "temperature"]
    NAME = "MH-Z19 CO2 Sensor"

    def _load_hardware(self):
        with serial.Serial(self.address, baudrate=9600, timeout=1) as device:
            device.flushInput()
            return device

    def _get_data(self):
        data = None
        with self.device as sensor:
            sensor.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
            # device.write(b'\xFF\x01\x86\x00\x00\x00\x00\x00')
            sleep(0.5)
            response = sensor.read(9)
            if len(response) >= 9 and response[0] == 0xFF and response[1] == 0x86:
                data = {}
                data["co2"] = int(response[2] * 256 + response[3])
                data["temperature"] = float(response[4]) - 40.0

        return data


class terrariumMHZ19BSensor(terrariumMHZ19Sensor):
    HARDWARE = "mh-z19b"
    NAME = "MH-Z19B CO2 Sensor"
