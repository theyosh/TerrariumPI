# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

# pip install sensirion-i2c-sht
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection

from sensirion_i2c_sht.sht2x import Sht2xI2cDevice
from sensirion_i2c_sht.sht3x import Sht3xI2cDevice
from sensirion_i2c_sht.sht4x import Sht4xI2cDevice

import adafruit_sht31d
import board
import busio


class terrariumSHT2XSensor(terrariumI2CSensor):
    HARDWARE = "sht2x"
    TYPES = ["temperature", "humidity"]
    NAME = "Sensirion SHT2X sensor"

    # SHT2XX - 3.3 Volt VCC
    # 黄 = Yellow = DATA
    # 蓝 = Blue   = CLK
    # 黑 = Black  = GND
    # 棕 = Brown  = VCC

    def _load_hardware(self):
        address = self._address

        return f"/dev/i2c-{address[1]}"

    def _get_data(self):
        with LinuxI2cTransceiver(self.device) as transceiver:
            device = Sht2xI2cDevice(I2cConnection(transceiver), self._address[0])
            temperature, humidity = device.single_shot_measurement()

            data = {"temperature": float(temperature.degrees_celsius), "humidity": float(humidity.percent_rh)}

        return data


class terrariumSHT3XSensor(terrariumSHT2XSensor):
    HARDWARE = "sht3x"
    NAME = "Sensirion SHT3X sensor"

    def _get_data(self):
        with LinuxI2cTransceiver(self.device) as transceiver:
            device = Sht3xI2cDevice(I2cConnection(transceiver), self._address[0])
            temperature, humidity = device.single_shot_measurement()

            data = {"temperature": float(temperature.degrees_celsius), "humidity": float(humidity.percent_rh)}

        return data


class terrariumSHT3XDSensor(terrariumSHT2XSensor):
    HARDWARE = "sht3xd"
    NAME = "Sensirion SHT3XD sensor"

    def _load_hardware(self):
        # Only using default addresses
        return busio.I2C(board.SCL, board.SDA)

    def _get_data(self):
        sensor = adafruit_sht31d.SHT31D(self.device)
        sensor.repeatability = adafruit_sht31d.REP_MED
        sensor.mode = adafruit_sht31d.MODE_SINGLE

        data = {"temperature": float(sensor.temperature), "humidity": float(sensor.relative_humidity)}

        return data


class terrariumSHT4XSensor(terrariumSHT2XSensor):
    HARDWARE = "sht4x"
    NAME = "Sensirion SHT4X sensor"

    def _get_data(self):
        with LinuxI2cTransceiver(self.device) as transceiver:
            device = Sht4xI2cDevice(I2cConnection(transceiver), self._address[0])
            temperature, humidity = device.single_shot_measurement()

            data = {"temperature": float(temperature.degrees_celsius), "humidity": float(humidity.percent_rh)}

        return data
