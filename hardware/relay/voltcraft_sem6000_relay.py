from . import terrariumRelay
from terrariumUtils import terrariumUtils

import re


class terrariumRelayVoltcraftSEM6000(terrariumRelay):
    HARDWARE = "voltcraft_sem6000"
    NAME = "Voltcraft SEM6000"

    DEFAULT_PIN = "0000"

    POWER_STATE_REGEX = r"Power:\s*(?P<state>On|Off)"
    CMD = "python 3rdparty/python3-voltcraft-sem6000/sem6000-cli-demo.py"

    def _load_hardware(self):
        terrariumUtils.get_script_data(
            f"{terrariumRelayVoltcraftSEM6000.CMD} {self.address} 0000 synchronize_date_and_time 2>/dev/null"
        )
        return self.address

    def _set_hardware_value(self, state):
        if state == self.ON:
            terrariumUtils.get_script_data(
                f"{terrariumRelayVoltcraftSEM6000.CMD} {self.address} 0000 power_on 2>/dev/null"
            )
        else:
            terrariumUtils.get_script_data(
                f"{terrariumRelayVoltcraftSEM6000.CMD} {self.address} 0000 power_off 2>/dev/null"
            )

        # Always return True here, as this should indicate the toggle changed succeeded
        return True

    def _get_hardware_value(self):
        data = terrariumUtils.get_script_data(
            f"{terrariumRelayVoltcraftSEM6000.CMD} {self.address} 0000 request_measurement 2>/dev/null"
        )
        state = False
        if data:
            state = re.search(terrariumRelayVoltcraftSEM6000.POWER_STATE_REGEX, data.decode("utf-8"))
            if state:
                state = state.group("state")

        return self.ON if terrariumUtils.is_true(state) else self.OFF

    @staticmethod
    def _scan_relays(callback=None, **kwargs):
        devices = (
            terrariumUtils.get_script_data(f"{terrariumRelayVoltcraftSEM6000.CMD} discover 2>/dev/null")
            .decode("utf-8")
            .strip()
        )
        if devices:
            for device in devices.split("\n"):
                device = device.split("\t")
                yield terrariumRelay(
                    None,
                    terrariumRelayVoltcraftSEM6000.HARDWARE,
                    device[1],
                    f"{terrariumRelayVoltcraftSEM6000.NAME} {device[0]} device mac: {device[1]}",
                    callback=callback,
                )
