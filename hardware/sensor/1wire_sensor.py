# -*- coding: utf-8 -*-
from . import terrariumSensor, terrariumSensorLoadingException

from pathlib import Path
import re


class terrarium1WireSensor(terrariumSensor):
    HARDWARE = "1wire"
    TYPES = ["temperature", "humidity"]
    NAME = "1-Wire sensor"

    __W1_BASE_PATH = "/sys/bus/w1/devices/"
    __W1_TEMP_REGEX = re.compile(r"(?P<type>t|f)=(?P<value>[0-9\-]+)", re.IGNORECASE)

    def _load_hardware(self):
        # Create a full Path object to the 1wire sensor filesystem
        device = Path(self.__W1_BASE_PATH).joinpath(self.address.strip("/")).joinpath("w1_slave")
        # Check if path exists
        if device.exists():
            # Return the sensor
            return device

        # Raise a loading error
        raise terrariumSensorLoadingException(
            f"Unable to load sensor {self.HARDWARE} {self.name} at address {self.address}: Invalid path."
        )

    def _get_data(self):
        data = None
        with self.device.open("r") as sensor:
            sensor_data = terrarium1WireSensor.__W1_TEMP_REGEX.search(sensor.read())

        if sensor_data is None:
            return None

        data = {}
        if "t" == sensor_data.group("type"):
            data["temperature"] = float(sensor_data.group("value")) / 1000.0
        if "h" == sensor_data.group("type"):
            data["humidity"] = float(sensor_data.group("value")) / 1000.0

        return data

    @staticmethod
    def _scan_sensors(unit_value_callback=None, trigger_callback=None):
        # Scanning w1 system bus
        for device in sorted(Path(terrarium1WireSensor.__W1_BASE_PATH).glob("[1-9][0-9]-*")):
            with device.joinpath("w1_slave").open("r") as sensor:
                sensor_data = terrarium1WireSensor.__W1_TEMP_REGEX.search(sensor.read())

            if sensor_data:
                sensor_type = None

                if "t" == sensor_data.group("type"):
                    sensor_type = "temperature"
                elif "h" == sensor_data.group("type"):
                    sensor_type = "humidity"

                if sensor_type is not None:
                    yield terrariumSensor(
                        None,
                        terrarium1WireSensor.HARDWARE,
                        sensor_type,
                        device.name,
                        f"{terrarium1WireSensor.NAME} measuring {sensor_type}",
                        unit_value_callback=unit_value_callback,
                        trigger_callback=trigger_callback,
                    )
