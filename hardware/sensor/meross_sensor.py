# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

import os

from . import terrariumSensor, terrariumSensorLoadingException
from terrariumUtils import terrariumUtils, terrariumCache
from terrariumCloud import TerrariumMerossCloud


class terrariumMS100Sensor(terrariumSensor):
    HARDWARE = "ms100"
    TYPES = ["temperature", "humidity"]
    NAME = "Meross MS100"

    def _load_hardware(self):
        if TerrariumMerossCloud.is_enabled:
            self.__state_cache = terrariumCache()
            try:
                self.__state_cache.get_data(self.address)
            except Exception:
                raise terrariumSensorLoadingException("Sensor is not found at the Meross cloud.")

            return self.address

    def _get_data(self):
        if TerrariumMerossCloud.is_enabled:
            try:
                return self.__state_cache.get_data(self.address)

            except Exception:
                logger.warning(f"Strange bug... just ignore for now: {self}")
                try:
                    self.__state_cache = terrariumCache()
                    return self.__state_cache.get_data(self.address)

                except Exception as ex:
                    logger.error(f"Error getting new data for {self}: {ex}")
                    return None

    @staticmethod
    def _scan_sensors(unit_value_callback=None, trigger_callback=None):
        found_devices = []

        EMAIL = terrariumUtils.decrypt(os.environ.get("MEROSS_EMAIL", ""))
        PASSWORD = terrariumUtils.decrypt(os.environ.get("MEROSS_PASSWORD", ""))

        if EMAIL != "" and PASSWORD != "":
            cloud = TerrariumMerossCloud(EMAIL, PASSWORD)
            devices = cloud.scan_hardware("sensors")

            for device in devices:
                for sensor_type in terrariumMS100Sensor.TYPES:
                    found_devices.append(
                        terrariumSensor(
                            None,
                            terrariumMS100Sensor.HARDWARE,
                            sensor_type,
                            f"{device.subdevice_id}",
                            f"{terrariumMS100Sensor.NAME} {device.name} measuring {sensor_type}",
                            unit_value_callback=unit_value_callback,
                            trigger_callback=trigger_callback,
                        )
                    )

        for device in found_devices:
            yield device
