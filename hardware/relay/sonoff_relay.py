from . import terrariumRelay, terrariumRelayDimmer, terrariumRelayLoadingException
from terrariumUtils import terrariumCache, terrariumUtils

from hashlib import md5
import re


class terrariumRelaySonoff(terrariumRelay):
    HARDWARE = "sonoff"
    NAME = "Sonoff (Tasmota)"

    __URL_REGEX = re.compile(
        r"^(?P<protocol>https?):\/\/(((?P<user>[^:]+):)?(?P<passwd>[^@]+)?@)?(?P<host>[^#\/]+)(\/)?(#(?P<nr>\d+))?$",
        re.IGNORECASE,
    )

    # Input format should be either:
    # - http://[HOST]
    # - http://[HOST]#[POWER_SWITCH_NR]
    # - http://[HOST]/#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]/#[POWER_SWITCH_NR]
    @property
    def _address(self):
        address = None
        data = self.__URL_REGEX.match(self.address)
        if data:
            address = data.groupdict()
            if "nr" not in address or address["nr"] is None or "" == address["nr"]:
                address["nr"] = 1

            address["nr"] = int(address["nr"])
        else:
            raise terrariumRelayLoadingException(f"Incorrect address for a Sonoff device: {self}")

        return address

    def _load_hardware(self):
        address = self._address

        # Try Tasmota
        # http://sonoff/cm?cmnd=Power[POWER_SWITCH_NR]%201
        # http://sonoff/cm?cmnd=Power[POWER_SWITCH_NR]%200
        # http://sonoff/cm?user=admin&password=joker&cmnd=Power[POWER_SWITCH_NR]%201

        device = f'{address["protocol"]}://{address["host"]}/cm?'

        if "user" in address and "password" in address:
            device += f'user={address["user"]}&password={address["password"]}&'

        device += "cmnd="
        state = terrariumUtils.get_remote_data(f"{device}Status%200")

        if state is None:
            return None

        # Create the cache key for caching the relay states.
        # This is usefully when there are more then 1 relay per hardware device.
        self.__cache_key = md5(f'{self.HARDWARE}{state["StatusNET"]["Mac"].lower()}'.encode()).hexdigest()
        self.__cache = terrariumCache()
        self.__cache.set_data(self.__cache_key, state["StatusSTS"], self._CACHE_TIMEOUT)

        return device

    def _set_hardware_value(self, state):
        action = 1 if state == self.ON else 0
        url = f'{self.device}Power{self._address["nr"]}%20{action}'
        data = terrariumUtils.get_remote_data(url)

        if data is None:
            return False

        if "POWER" in data:
            data = data["POWER"]
        elif f'POWER{self._address["nr"]}' in data:
            data = data[f'POWER{self._address["nr"]}']

        return state == (self.ON if terrariumUtils.is_true(data) else self.OFF)

    def _get_hardware_value(self):
        data = self.__cache.get_data(self.__cache_key)
        if data is None:
            # Cache is expired, so we update with new data
            # Get the overall state information
            url = f"{self.device}State"
            data = terrariumUtils.get_remote_data(url)

            if data is None:
                return None

            self.__cache.set_data(self.__cache_key, data, self._CACHE_TIMEOUT)

        if "POWER" in data:
            data = data["POWER"]
        elif f'POWER{self._address["nr"]}' in data:
            data = data[f'POWER{self._address["nr"]}']

        return self.ON if terrariumUtils.is_true(data) else self.OFF


class terrariumRelayDimmerSonoffD1(terrariumRelayDimmer):
    HARDWARE = "sonoff_d1-dimmer"
    NAME = "Sonoff D1 Dimmer (Tasmota/DIY)"
    MODE = None

    __URL_REGEX = re.compile(
        r"^(?P<protocol>https?):\/\/((?P<user>[^:]+):(?P<passwd>[^@]+)@)?(?P<host>[^#\/]+)(\/)?(#(?P<nr>\d+))?$",
        re.IGNORECASE,
    )

    @property
    def _address(self):
        address = None
        data = self.__URL_REGEX.match(self.address)
        if data:
            address = data.groupdict()
            if "nr" not in address or address["nr"] is None or "" == address["nr"]:
                address["nr"] = 1

            address["nr"] = int(address["nr"])
        else:
            raise terrariumRelayLoadingException(f"Incorrect address for a Sonoff Dimmer device: {self}")

        return address

    def _load_hardware(self):
        address = self._address

        # Try Tasmota
        # http://sonoff/cm?cmnd=Dimmer%20[STATE]

        # Tasmota test
        device = f'{address["protocol"]}://{address["host"]}/cm?'

        if "user" in address and "password" in address:
            device += f'user={address["user"]}&password={address["password"]}&'

        device += "cmnd="
        state = terrariumUtils.get_remote_data(f"{device}Status%200")

        if state is not None:
            self.MODE = "tasmota"

            return device

        # DIY test
        # http://sonoff:8081/zeroconf
        # https://sonoff.tech/sonoff-diy-developer-documentation-d1-http-api/#9
        device = f'{address["protocol"]}://{address["host"]}/zeroconf'
        state = terrariumUtils.get_remote_data(f"{device}/info", json=True, post={"deviceid": "", "data": {}})

        if state is not None:
            self.MODE = "DIY"

            return device

        return None

    def _set_hardware_value(self, state):
        state = int(max(0.0, min(100.0, float(state + self._dimmer_offset))))

        if self.MODE == "tasmota":
            data = terrariumUtils.get_remote_data(f"{self.device}Dimmer%20{state}")
        elif self.MODE == "DIY":
            if state == 0:
                data = terrariumUtils.get_remote_data(
                    f"{self.device}/switch", json=True, post={"deviceid": "", "data": {"switch": "off"}}
                )
            else:
                # request switch on and specified brightness
                # switch must be on, mode 0, brightness between brightmin and brightmax
                data = terrariumUtils.get_remote_data(
                    f"{self.device}/dimmable",
                    json=True,
                    post={
                        "deviceid": "",
                        "data": {"switch": "on", "brightness": state, "mode": 0, "brightmin": 0, "brightmax": 100},
                    },
                )

        if data is None:
            return False

        return True

    def _get_hardware_value(self):
        if self.MODE == "tasmota":
            data = terrariumUtils.get_remote_data(f"{self.device}Dimmer")
            if data is not None and "Dimmer" in data:
                return int(data["Dimmer"])

        elif self.MODE == "DIY":
            data = terrariumUtils.get_remote_data(f"{self.device}/info", json=True, post={"deviceid": "", "data": {}})
            if data is not None and "data" in data:
                return int(data["data"]["brightness"])

        return None
