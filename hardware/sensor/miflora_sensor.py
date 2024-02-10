# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumBluetoothSensor

# apt install libglib2.0-dev
# pip install bluepy (buster, bullseye)
# pip install git+https://github.com/Mausy5043/bluepy3 (bookworm)
from struct import unpack
from bluepy.btle import Peripheral, BTLEException


class terrariumMiFloraSensor(terrariumBluetoothSensor):
    HARDWARE = "miflora"
    TYPES = ["temperature", "light", "moisture", "fertility"]
    NAME = "MiFlora bluetooth sensor"

    __MIFLORA_FIRMWARE_AND_BATTERY = 56
    __MIFLORA_REALTIME_DATA_TRIGGER = 51
    __MIFLORA_GET_DATA = 53
    __MIFLORA_TIMEOUT = 10

    __POWER_STATE = 100

    # Overrule the update function to update the current battery state
    def update(self, force=False):
        value = super().update(force)
        data = self._sensor_cache.get_data(self._sensor_cache_key)
        self.__POWER_STATE = data["battery"]
        return value

    def __repr__(self):
        return f"{super().__repr__()} battery {self.__POWER_STATE}%"

    def _load_hardware(self):
        address = self._address
        # Load Bluetooth device and try to load battery and firmware version to check if the connection does work
        with Peripheral(address[0], iface=address[1], timeout=terrariumMiFloraSensor.__MIFLORA_TIMEOUT) as device:
            data = device.readCharacteristic(terrariumMiFloraSensor.__MIFLORA_FIRMWARE_AND_BATTERY)
            data = {"battery": data[0], "firmware": data[2:].decode("utf8")}
            # Return the device
            return device

    def _get_data(self):
        try:
            data = {}
            with self.device as sensor:
                sensor.connect(sensor.addr, iface=sensor.iface, timeout=terrariumMiFloraSensor.__MIFLORA_TIMEOUT)
                # Read battery and firmware version attribute
                data = sensor.readCharacteristic(terrariumMiFloraSensor.__MIFLORA_FIRMWARE_AND_BATTERY)
                data = {"battery": data[0], "firmware": data[2:].decode("utf8")}

                # Enable real-time data reading
                sensor.writeCharacteristic(
                    terrariumMiFloraSensor.__MIFLORA_REALTIME_DATA_TRIGGER, bytearray([0xA0, 0x1F]), True
                )
                # Read plant data
                data["temperature"], data["light"], data["moisture"], data["fertility"] = unpack(
                    "<hxIBHxxxxxx", sensor.readCharacteristic(terrariumMiFloraSensor.__MIFLORA_GET_DATA)
                )
                sensor.disconnect()

            # Clean up
            data["temperature"] = float(data["temperature"]) / 10.0
            data["light"] = float(data["light"])
            data["moisture"] = float(data["moisture"])
            data["conductivity"] = float(data["fertility"])
            data["battery"] = float(data["battery"])
            data["firmware"] = data["firmware"]

            return data

        except BTLEException as ex:
            # Lost connection.... retry getting a 'new' device. The data will be red the next round
            logger.warning(f"Lost connection with sensor {self}. Reconnecting... (BTLEException): {ex}")
            self.load_hardware(True)

        except BrokenPipeError as ex:
            # Lost connection.... retry getting a 'new' device. The data will be red the next round
            logger.warning(f"Lost connection with sensor {self}. Reconnecting... (BrokenPipeError): {ex}")
            self.load_hardware(True)

        logger.warning(f"Reconnecting sensor {self} hardware. (No data)")
        self.load_hardware(True)

        return None

    @staticmethod
    def _scan_sensors(unit_value_callback=None, trigger_callback=None):
        for sensor in terrariumBluetoothSensor._scan_bt_sensors(
            __class__, ["flower mate", "flower care"], unit_value_callback, trigger_callback
        ):
            yield sensor
