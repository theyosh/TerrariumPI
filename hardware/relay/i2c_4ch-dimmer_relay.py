from . import terrariumRelayDimmer, terrariumRelayLoadingException

# https://www.tindie.com/products/bugrovs2012/i2c-4ch-ac-led-dimmer-module/
# pip install smbus2
import smbus2


class terrariumDimmerI2C4CH(terrariumRelayDimmer):
    HARDWARE = "i2c_4ch-dimmer"
    NAME = "I2C 4Channel LED AC dimmer"

    def _load_hardware(self):
        self._dimmer_state = 0
        # address is expected as `[relay_number],[i2c_address],[i2c_bus (optional)]`
        address = self.address.split(",")
        relay_nr = int(address[0])
        if not (relay_nr >= 1 and relay_nr <= 4):
            raise terrariumRelayLoadingException("Invalid relay number")

        address[0] = 0x7F + relay_nr

        if not address[1].startswith("0x"):
            address[1] = "0x" + address[1]

        address[1] = int(address[1], 16)

        if len(address) == 2:
            address.append(1)
        else:
            address[2] = int(address[2])

        return address

    def _set_hardware_value(self, state):
        with smbus2.SMBus(self.device[2]) as bus:
            # Select channel
            bus.write_byte(self.device[1], self.device[0])
            # Set dim value
            bus.write_byte(self.device[1], int(100.0 - state))
            # Keep copy for readout
            self._dimmer_state = state

        return True

    def _get_hardware_value(self):
        return self._dimmer_state
