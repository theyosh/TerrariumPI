# -*- coding: utf-8 -*-
from . import terrariumBluetoothSensor

# pip install mitemp-bt
from mitemp_bt.mitemp_bt_poller import MiTempBtPoller, MI_TEMPERATURE, MI_HUMIDITY, MI_BATTERY
from btlewrap.bluepy import BluepyBackend


class terrariumMiTempSensor(terrariumBluetoothSensor):
    HARDWARE = "mitemp"
    TYPES = ["temperature", "humidity"]
    NAME = "MiTemperature bluetooth sensor"

    def _load_hardware(self):
        address = self._address
        device = MiTempBtPoller(address[0], BluepyBackend, 10, adapter=f"hci{address[1]}")
        return device

    def _get_data(self):
        data = {}

        # BUG: Firmware data en battery will only be set at the first measurement.
        # self._device['firmware'] = self._device['device'].firmware_version()
        # self._device['battery']  = self._device['device'].parameter_value(MI_BATTERY)

        data["temperature"] = self.device.parameter_value(MI_TEMPERATURE)
        data["humidity"] = self.device.parameter_value(MI_HUMIDITY)
        data["battery"] = float(self.device.parameter_value(MI_BATTERY))
        data["firmware"] = self.device.firmware_version()

        return data

    @staticmethod
    def _scan_sensors(unit_value_callback=None, trigger_callback=None):
        for sensor in terrariumBluetoothSensor._scan_bt_sensors(
            __class__, ["mj_ht_v1"], unit_value_callback, trigger_callback
        ):
            yield sensor
