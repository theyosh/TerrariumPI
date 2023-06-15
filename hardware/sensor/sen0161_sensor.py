# -*- coding: utf-8 -*-
from . import terrariumAnalogSensor


class terrariumSEN0161Sensor(terrariumAnalogSensor):
    HARDWARE = "sen0161"
    TYPES = ["ph"]
    NAME = "SEN0161 PH Probe sensor (analog)"

    def _get_data(self):
        data = {}
        voltage = super()._get_data()
        # https://github.com/theyosh/TerrariumPI/issues/108
        # We measure the values in volts already, so no deviding by 1000 as original script does
        data["ph"] = (voltage * (5000.0 / 1024.0)) * 3.3 + 0.1614
        return data
