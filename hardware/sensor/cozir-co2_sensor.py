# -*- coding: utf-8 -*-
from . import terrariumSensor

import serial

from gevent import sleep

# http://www.co2meters.com/Documentation/AppNotes/AN127-COZIR-sensor-raspberry-pi-uart.pdf
# pip install pyserial


class terrariumCOZIRCO2Sensor(terrariumSensor):
    HARDWARE = "cozirco2"
    TYPES = ["temperature", "humidity", "co2"]
    NAME = "COZIR CO2 Sensor"

    def _load_hardware(self):
        with serial.Serial(self.address, baudrate=9600, timeout=1) as device:
            device.write(b"M 4164\r\n")  # Show temperature, humdity and CO2 values
            device.write(b"K 2\r\n")  # Set to polling mode
            device.flushInput()
            # Give the sensor some time to warm up
            sleep(1)

            return device

    def _get_data(self):
        data = None
        with self.device as sensor:
            sensor.write(b"Z\r\n")
            response = sensor.readline().strip().split(" ")
            # output should be: 'H 00345 T 01195 Z 00651\r\n'
            data = {}
            data["humidity"] = float(response[1]) / 10.0
            data["temperature"] = (float(response[3]) - 1000.0) / 10.0
            data["co2"] = int(response[5])

        return data
