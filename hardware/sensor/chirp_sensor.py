# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

from pathlib import Path

import sys

# Dirty hack to include someone his code... to lazy to make it myself :)
# https://github.com/ageir/chirp-rpi
sys.path.insert(0, str((Path(__file__).parent / Path("../../3rdparty/chirp-rpi")).resolve()))
import chirp


class terrariumChirpSensor(terrariumI2CSensor):
    HARDWARE = "chirp"
    # Light is disabled, as we cannot use it
    TYPES = ["temperature", "moisture"]
    NAME = "CHIRP sensor"

    # Some basic calibration values which should be overruled in the interface
    __MIN_MOIST = 160
    __MAX_MOIST = 720

    @property
    def __min_moist(self):
        try:
            return self.__calibration.get("min_moist", self.__MIN_MOIST)
        except Exception:
            return self.__MIN_MOIST

    @property
    def __max_moist(self):
        try:
            return self.__calibration.get("max_moist", self.__MAX_MOIST)
        except Exception:
            return self.__MAX_MOIST

    def calibrate(self, calibration_data):
        self.__calibration = {
            "min_moist": calibration_data["chirp_min_moist"],
            "max_moist": calibration_data["chirp_max_moist"],
        }

    def _get_data(self):
        data = None
        with self._open_hardware() as i2c_bus:
            # TODO: Fix the bus number....
            sensor = chirp.Chirp(
                bus=1,
                address=self.device[0],
                read_moist=True,
                read_temp=True,
                read_light=False,
                min_moist=self.__min_moist,
                max_moist=self.__max_moist,
                temp_scale="celsius",
                temp_offset=0,
            )  # Temperature offset is handled by the TerrariumEngine
            # Hack to overrule the Chirp bus, so it will be closed when we are done.
            # Close old smbus(1) connection to the sensor
            sensor.bus.close()
            # Replace it now with the new smbus2 connection
            sensor.bus = i2c_bus

            sensor.trigger()
            data = {}
            data["temperature"] = float(sensor.temp)
            data["moisture"] = float(sensor.moist_percent)
        #      data['light']       = 100.0 - ((float(sensor.light) / 65536.0) * 100.0)

        return data
