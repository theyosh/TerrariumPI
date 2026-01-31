# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

from pathlib import Path

import sys

# Dirty hack to include someone his code... to lazy to make it myself :)
sys.path.insert(0, str((Path(__file__).parent / Path("../../3rdparty/iorodeo-as7331/iorodeo_as7331")).resolve()))
import board
import iorodeo_as7331 as as7331


class terrariumAS7331Sensor(terrariumI2CSensor):
    HARDWARE = "AS7331"
    TYPES = ["uva", "uvb", "uvc", "temperature"]
    NAME = "AS7331 UVA, UVB, UVC light and temperature sensor"

    def _load_hardware(self):
        i2c = board.I2C()
        device = as7331.AS7331(i2c, self._address[1])

        device.gain = as7331.GAIN_512X
        device.integration_time = as7331.INTEGRATION_TIME_128MS

        return device

    def _get_data(self):
        uva, uvb, uvc, temp = self.device.values
        data = {"uva": uva, "uvb": uvb, "uvc": uvc, "temperature": temp}

        return data
