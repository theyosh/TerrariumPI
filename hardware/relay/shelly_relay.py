from . import terrariumRelay, terrariumRelayLoadingException
from terrariumUtils import terrariumUtils

import re


class terrariumRelayShelly(terrariumRelay):
    HARDWARE = "shelly"
    NAME = "Shelly"

    __URL_REGEX = re.compile(
        r"^(?P<protocol>https?):\/\/(((?P<user>[^:]+):)?(?P<passwd>[^@]+)?@)?(?P<host>[^#\/]+)(\/)?(#(?P<nr>\d+))?$",
        re.IGNORECASE,
    )

    @property
    def _address(self):
        address = None
        data = self.__URL_REGEX.match(self.address)
        if data:
            address = data.groupdict()
            if "nr" not in address or address["nr"] is None or "" == address["nr"]:
                # Humans start counting at 1
                address["nr"] = 1

            # Computers start counting at 0
            address["nr"] = int(address["nr"]) - 1
        else:
            raise terrariumRelayLoadingException(f"Incorrect address for a Shelly device: {self}")

        return address

    def _load_hardware(self):
        # Input format should be either:
        # - http://[HOST]#[POWER_SWITCH_NR]
        # - http://[HOST]/#[POWER_SWITCH_NR]
        # - http://[PASSWORD]@[HOST]#[POWER_SWITCH_NR]
        # - http://[PASSWORD]@[HOST]/#[POWER_SWITCH_NR]

        address = self._address
        device = f'{address["protocol"]}://{address["host"]}'

        if "user" in address and "password" in address:
            device = f'{address["protocol"]}://{address["user"]}:{address["password"]}@{address["host"]}'
        elif "password" in address:
            device = f'{address["protocol"]}://{address["password"]}@{address["host"]}'

        device += f'/relay/{self._address["nr"]}'

        data = terrariumUtils.get_remote_data(device)

        if data is None:
            return None

        return device

    def _set_hardware_value(self, state):
        action = "on" if state == self.ON else "off"
        url = f"{self.device}?turn={action}"
        data = terrariumUtils.get_remote_data(url)

        if data is None:
            return False

        if "ison" in data:
            data = data["ison"]

        return state == (self.ON if terrariumUtils.is_true(data) else self.OFF)

    def _get_hardware_value(self):
        data = terrariumUtils.get_remote_data(self.device)

        if data is None:
            return None

        if "ison" in data:
            data = data["ison"]

        return self.ON if terrariumUtils.is_true(data) else self.OFF
