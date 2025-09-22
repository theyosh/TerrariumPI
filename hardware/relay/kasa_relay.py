import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumRelay
from terrariumUtils import terrariumUtils, terrariumAsync, terrariumCache

# pip install python-kasa
from kasa import Discover


class terrariumRelayTPLinkKasa(terrariumRelay):
    HARDWARE = "tplinkkasa"
    NAME = "Kasa Smart"

    URL = "^\d{1,3}\.\d{1,3}\.\d{1,3}(,\d{1,3})?$"

    def _load_hardware(self):
        async def __load_hardware(ip):
            device = await Discover.discover_single(ip)

            return device

        self._device["device"] = None
        # Input format should be either:
        # - [IP],[POWER_SWITCH_NR]

        # Use an internal caching for speeding things up.
        self.__state_cache = terrariumCache()
        self.__asyncio = terrariumAsync()

        address = self._address
        try:
            self._device["device"] = self.__asyncio.run(__load_hardware(address[0]))
            self._device["switch"] = 0 if len(address) == 1 else int(address[1]) - 1
        except Exception as ex:
            logger.error(f"Error loading {self} at address {address[0]}: {ex}")

        return self._device["device"]

    def _set_hardware_value(self, state):
        async def __set_hardware_state(state):
            await self.device.update()
            plug = self.device if not self.device.is_strip else self.device.children[self._device["switch"]]

            if state != 0.0:
                await plug.turn_on()
            else:
                await plug.turn_off()

            return state

        data = self.__asyncio.run(__set_hardware_state(state))

        # Update the cache after relay change
        self._get_hardware_value(True)

        return data == state

    def _get_hardware_value(self, force=False):
        async def __get_hardware_state():
            data = []
            await self.device.update()

            plugs = [self.device] if not self.device.is_strip else self.device.children
            for plug in plugs:
                data.append(plug.is_on)

            return data

        try:
            data = self.__state_cache.get_data(self._address[0])

            if data is None or force:
                data = self.__asyncio.run(__get_hardware_state())
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

                try:
                    await device.update()
                except Exception as ex:
                    logger.warning(ex)
                    continue

                if device.is_strip:
                    for counter in range(1, len(device.children) + 1):
                        found_devices.append(
                            terrariumRelay(
                                None,
                                terrariumRelayTPLinkKasa.HARDWARE,
                                f"{device.host},{counter}",
                                f"Channel {device.children[counter-1].alias}",
                                {},
                                callback=callback,
                            )
                        )

                else:
                    found_devices.append(
                        terrariumRelay(
                            None,
                            terrariumRelayTPLinkKasa.HARDWARE,
                            f"{device.host}",
                            f"Channel {device.alias}",
                            {},
                            callback=callback,
                        )
                    )

            return found_devices

        found_devices = []
        __asyncio = terrariumAsync()
        found_devices = __asyncio.run(__scan())

        for device in found_devices:
            yield device
