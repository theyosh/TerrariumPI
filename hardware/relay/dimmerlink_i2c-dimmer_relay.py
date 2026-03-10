from . import terrariumRelayDimmer

# https://github.com/robotdyn-dimmer/DimmerLink/blob/main/examples/python/i2c_example.py
# pip install smbus2
import smbus2


class terrariumDimmerI2C4CH(terrariumRelayDimmer):
    HARDWARE = "dimmerlink-i2c-dimmer"
    NAME = "DimmerLink(I2C)"

    _DEFAULT_ADDRESS = "0x50"
    # Bugs in driver...
    # 1. Setting to value X, will return previous state before X at first read out
    # 2. After second read out, the value is X-1
    # Fix: keep an internal state and return that value at read out

    __INTERNAL_STATE = None

    def _load_hardware(self):
        # address is expected as `[i2c_address],[I2C bus (optional)]`
        address = self._address
        if len(address) == 0:
            address.append(self._DEFAULT_ADDRESS)

        if not address[0].startswith("0x"):
            address[0] = "0x" + address[0]

        if len(address) == 1:
            address.append(1)  # Default I2C bus

        address[0] = int(address[0], 16)

        return address

    def _set_hardware_value(self, state):
        self.__INTERNAL_STATE = int(state)
        with smbus2.SMBus(self.device[1]) as bus:
            bus.write_byte_data(self.device[0], 0x10, self.__INTERNAL_STATE)

        return True

    def _get_hardware_value(self):
        return self.__INTERNAL_STATE

        # state = None
        # with smbus2.SMBus(self.device[1]) as bus:
        #     state = bus.read_byte_data(self.device[0], 0x10)

        # return state

    def calibrate(self, data):
        super().calibrate(data)

        curve = int(data.get("dimmer_curve", 0))  # curve_type: CURVE_LINEAR (0), CURVE_RMS (1), CURVE_LOG (2)
        with smbus2.SMBus(self.device[1]) as bus:
            bus.write_byte_data(self.device[0], 0x11, curve)
