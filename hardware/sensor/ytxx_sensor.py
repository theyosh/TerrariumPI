# -*- coding: utf-8 -*-
from . import terrariumSensor
from terrariumUtils import terrariumUtils

from gpiozero import Button


class terrariumYTXXSensorDigital(terrariumSensor):
    HARDWARE = "ytxx-digital"
    TYPES = ["moisture"]
    NAME = "YT-69 sensor (digital)"

    def _load_hardware(self):
        address = self._address
        if len(address) >= 2 and terrariumUtils.is_float(address[1]):
            # Set / enable power management
            self._device["power_mngt"] = address[1]

        return Button(terrariumUtils.to_BCM_port_number(address[0]))

    def _get_data(self):
        data = {}
        data["moisture"] = 0 if not self.device.is_pressed else 100
        return data

    def stop(self):
        super().stop()
