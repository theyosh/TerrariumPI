# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumBluetoothSensor

# pip install lywsd03mmc
from lywsd03mmc import Lywsd03mmcClient


class terrariumLywsd03mmcSensor(terrariumBluetoothSensor):
    HARDWARE = "LYWSD03MMC"
    TYPES = ["temperature", "humidity"]  # Also supports battery, but unused.
    NAME = "LYWSD03MMC bluetooth sensor"

    _UPDATE_TIME_OUT = 30  # This has to be >~25 to reliably get data.

    def _load_hardware(self):
        address = self._address
        logger.debug("Started connecting")
        device = Lywsd03mmcClient(address[0])
        logger.debug("Finished connecting")
        return device

    def _get_data(self):
        data = {}

        logger.debug("starting to fetch data")

        for sensor_type in self.TYPES:
            data[sensor_type] = getattr(self.device, sensor_type)

        logger.debug(data)

        return data

    @staticmethod
    def _scan_sensors(unit_value_callback=None, trigger_callback=None):
        for sensor in terrariumBluetoothSensor._scan_bt_sensors(
            __class__, [__class__.HARDWARE.lower()], unit_value_callback, trigger_callback
        ):
            yield sensor
