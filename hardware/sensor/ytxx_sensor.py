# -*- coding: utf-8 -*-
from . import terrariumSensor
from terrariumUtils import terrariumUtils

import RPi.GPIO as GPIO


class terrariumYTXXSensorDigital(terrariumSensor):
    HARDWARE = "ytxx-digital"
    TYPES = ["moisture"]
    NAME = "YT-69 sensor (digital)"

    def _load_hardware(self):
        address = self._address
        if len(address) >= 2 and terrariumUtils.is_float(address[1]):
            # Set / enable power management
            self._device["power_mngt"] = terrariumUtils.to_BCM_port_number(address[1])

        GPIO.setup(terrariumUtils.to_BCM_port_number(address[0]), GPIO.IN)  # Data in
        return terrariumUtils.to_BCM_port_number(address[0])

    def _get_data(self):
        data = {}
        data["moisture"] = 0 if GPIO.input(self.device) else 100
        return data

    def stop(self):
        GPIO.cleanup(self.device)
        super().stop()
