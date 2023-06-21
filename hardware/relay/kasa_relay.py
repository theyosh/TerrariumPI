import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

import asyncio

from . import terrariumRelay
from terrariumUtils import terrariumUtils, terrariumAsync, terrariumCache

# pip install python-kasa
from kasa import Discover, SmartStrip, SmartPlug


class terrariumRelayTPLinkKasa(terrariumRelay):
    HARDWARE = "tplinkkasa"
    NAME = "Kasa Smart"

    URL = "^\d{1,3}\.\d{1,3}\.\d{1,3}(,\d{1,3})?$"

    def _load_hardware(self):
        # Input format should be either:
        # - [IP],[POWER_SWITCH_NR]

        # Use an internal caching for speeding things up.
        self.__state_cache = terrariumCache()
        self._async = terrariumAsync()

        address = self._address
        if len(address) == 1:
            self._device["device"] = SmartPlug(address[0])
            self._device["switch"] = 0
        else:
            self._device["device"] = SmartStrip(address[0])
            self._device["switch"] = int(address[1]) - 1

        return self._device["device"]

    def _set_hardware_value(self, state):
        async def __set_hardware_state(state):
            await self.device.update()
            plug = self.device if len(self._address) == 1 else self.device.children[self._device["switch"]]

            if state != 0.0:
                await plug.turn_on()
            else:
                await plug.turn_off()

            return state

        data = self.__state_cache.get_data(self._address[0])
        if data is not None and terrariumUtils.is_true(data[self._device["switch"]]) == (state != 0.0):
            return True

        toggle = asyncio.run_coroutine_threadsafe(__set_hardware_state(state), self._async.async_loop)
        data = toggle.result()
        return data == state

    def _get_hardware_value(self):
        async def __get_hardware_state():
            data = []
            await self.device.update()

            plugs = [self.device] if len(self._address) == 1 else self.device.children
            for plug in plugs:
                data.append(plug.is_on)

            return data

        try:
            data = self.__state_cache.get_data(self._address[0])

            if data is None:
                toggle = asyncio.run_coroutine_threadsafe(__get_hardware_state(), self._async.async_loop)
                data = toggle.result()

                self.__state_cache.set_data(self._address[0], data, cache_timeout=20)

            return (
                self.ON
                if len(data) >= self._device["switch"] and terrariumUtils.is_true(data[self._device["switch"]])
                else self.OFF
            )
        except RuntimeError as err:
            logger.exception(err)
        except Exception as ex:
            logger.exception(ex)

        return None

    @staticmethod
    def _scan_relays(callback=None):
        async def __scan():
            found_devices = []

            devices = await Discover.discover()
            for ip_address in devices:
                device = devices[ip_address]
                await device.update()
                if device.is_strip:
                    for counter in range(1, len(device.children) + 1):
                        found_devices.append(
                            terrariumRelay(
                                None,
                                terrariumRelayTPLinkKasa.HARDWARE,
                                "{},{}".format(device.host, counter),
                                f"Channel {device.children[counter-1].alias}",
                                None,
                                callback,
                            )
                        )

                else:
                    found_devices.append(
                        terrariumRelay(
                            None,
                            terrariumRelayTPLinkKasa.HARDWARE,
                            f"{device.host}",
                            f"Channel {device.alias}",
                            None,
                            callback,
                        )
                    )

            return found_devices

        found_devices = []
        _async_loop = terrariumAsync()
        data = asyncio.run_coroutine_threadsafe(__scan(), _async_loop.async_loop)
        found_devices = data.result()

        for device in found_devices:
            yield device
