from . import terrariumRelay
from terrariumUtils import terrariumUtils

import re


class terrariumRelayVoltcraftSEM6000(terrariumRelay):
    HARDWARE = "voltcraft_sem6000"
    NAME = "Voltcraft SEM6000"

    DEFAULT_PIN = "0000"

    POWER_STATE_REGEX = r"Power:\s*(?P<state>On|Off)"

    def _load_hardware(self):
        terrariumUtils.get_script_data(
            f"python 3rdparty/python3-voltcraft-sem6000/sem6000-cli-demo.py {self.address} 0000 synchronize_date_and_time"
        )
        return self.address

    def _set_hardware_value(self, state):
        if state == self.ON:
            terrariumUtils.get_script_data(
                f"python 3rdparty/python3-voltcraft-sem6000/sem6000-cli-demo.py {self.address} 0000 power_on"
            )
        else:
            terrariumUtils.get_script_data(
                f"python 3rdparty/python3-voltcraft-sem6000/sem6000-cli-demo.py {self.address} 0000 power_off"
            )

        # Always return True here, as this should indicate the toggle changed succeeded
        return True

    def _get_hardware_value(self):
        data = terrariumUtils.get_script_data(
            f"python 3rdparty/python3-voltcraft-sem6000/sem6000-cli-demo.py {self.address} 0000 request_measurement"
        )
        if data:
            state = re.search(terrariumRelayVoltcraftSEM6000.POWER_STATE_REGEX, data.decode("utf-8"))
            if state:
                state = state.group("state")

        return self.ON if terrariumUtils.is_true(state) else self.OFF

    @staticmethod
    def _scan_relays(callback=None, **kwargs):
        devices = (
            terrariumUtils.get_script_data(f"python 3rdparty/python3-voltcraft-sem6000/sem6000-cli-demo.py discover")
            .decode("utf-8")
            .strip()
            .split("\n")
        )
        for device in devices:
            device = device.split("\t")
            yield terrariumRelay(
                None,
                terrariumRelayVoltcraftSEM6000.HARDWARE,
                device[1],
                f"{terrariumRelayVoltcraftSEM6000.NAME} {device[0]} device mac: {device[1]}",
                callback=callback,
            )
