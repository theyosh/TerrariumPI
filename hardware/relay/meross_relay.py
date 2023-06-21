# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

import os

from . import terrariumRelay
from terrariumUtils import terrariumUtils, terrariumCache
from terrariumCloud import TerrariumMerossCloud


class terrariumRelayMeross(terrariumRelay):
    HARDWARE = "meross"
    NAME = "Meross power switches"

    def _load_hardware(self):
        # Use an internal caching for speeding things up.
        self.__state_cache = terrariumCache()
        EMAIL = terrariumUtils.decrypt(os.environ.get("MEROSS_EMAIL", ""))
        PASSWORD = terrariumUtils.decrypt(os.environ.get("MEROSS_PASSWORD", ""))

        if "" == EMAIL or "" == PASSWORD:
            logger.error("Meross credentials are not set!")
            return None

        self._cloud = TerrariumMerossCloud(EMAIL, PASSWORD)

        address = self._address
        if len(address) == 1:
            # When no channels/plugs defined always use the first one...
            address.append(0)

        self._device["device"] = address[0]
        self._device["switch"] = int(address[1])

        return self._device["device"]

    def _set_hardware_value(self, state):
        EMAIL = terrariumUtils.decrypt(os.environ.get("MEROSS_EMAIL"))
        PASSWORD = terrariumUtils.decrypt(os.environ.get("MEROSS_PASSWORD"))

        if "" == EMAIL or "" == PASSWORD:
            logger.error("Meross credentials are not set!")
            return

        return self._cloud.toggle_relay(self._device["device"], self._device["switch"], state)

    def _get_hardware_value(self):
        EMAIL = terrariumUtils.decrypt(os.environ.get("MEROSS_EMAIL"))
        PASSWORD = terrariumUtils.decrypt(os.environ.get("MEROSS_PASSWORD"))

        if "" == EMAIL or "" == PASSWORD:
            logger.error("Meross credentials are not set!")
            return None

        data = self.__state_cache.get_data(self._device["device"])

        if data is None:
            return None

        return (
            self.ON
            if len(data) >= self._device["switch"] and terrariumUtils.is_true(data[self._device["switch"]])
            else self.OFF
        )

    @staticmethod
    def _scan_relays(callback=None):
        found_devices = []
        EMAIL = terrariumUtils.decrypt(os.environ.get("MEROSS_EMAIL", ""))
        PASSWORD = terrariumUtils.decrypt(os.environ.get("MEROSS_PASSWORD", ""))

        if not ("" == EMAIL or "" == PASSWORD):
            cloud = TerrariumMerossCloud(EMAIL, PASSWORD)
            devices = cloud.scan_hardware("relays")

            for device in devices:
                for channel in device.channels:
                    if len(device.channels) == 1 or not channel.is_master_channel:
                        found_devices.append(
                            terrariumRelay(
                                None,
                                terrariumRelayMeross.HARDWARE,
                                "{},{}".format(device.uuid, channel.index),
                                "Channel {}".format(channel.name),
                                None,
                                callback,
                            )
                        )

        for device in found_devices:
            yield device
