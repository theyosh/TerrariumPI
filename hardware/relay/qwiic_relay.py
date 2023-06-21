from . import terrariumRelay

# pip install sparkfun-qwiic-relay
import qwiic_relay


class terrariumRelayQwiic(terrariumRelay):
    HARDWARE = "qwiic-relay"
    NAME = "Qwiic Relay"

    def _load_hardware(self):
        # address is expected as `[relay_number],[i2c_address]`
        i2c_address = self.address.split(",")[1]
        if not i2c_address.startswith("0x"):
            i2c_address = int("0x" + i2c_address, 16)

        device = qwiic_relay.QwiicRelay(address=i2c_address)
        return device

    def _set_hardware_value(self, state):
        relay_number = int(self.address.split(",")[0])

        if state == self.ON:
            self._device["device"].set_relay_on(relay_number)
        else:
            self._device["device"].set_relay_off(relay_number)
        return True

    def _get_hardware_value(self):
        relay_number = int(self.address.split(",")[0])

        return self._device["device"].get_relay_state(relay_number)
