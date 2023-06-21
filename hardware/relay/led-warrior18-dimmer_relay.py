from . import terrariumRelayDimmer, terrariumRelayLoadingException
from terrariumUtils import terrariumCache

# https://github.com/codemercs-com/lw18/blob/main/src/rpi/python/lw18.py
# pip install smbus2
import smbus2


class terrariumRelayDimmerLEDWarrior18(terrariumRelayDimmer):
    HARDWARE = "led-warrior18-dimmer"
    NAME = "LED-Warrior18-dimmer"

    # Dimmer settings
    _DIMMER_FREQ = 65535  # Strange example code
    _DIMMER_DIM = 65535

    LW18_REG_PWM16 = 0x01  # R/W : 4Byte ; 2x 16 bit PWM
    LW18_REG_FREQUENCY = 0x03  # W : 4Byte ; 2x 16 bit frequency

    # Read 16Bit PWM from LW18
    def ReadPwm16(self):
        # Read 4 byte from device
        buffer = [0, 0, 0, 0]
        with smbus2.SMBus(self.device[2]) as bus:
            buffer = bus.read_i2c_block_data(self.device[1], self.LW18_REG_PWM16, 4)

        # Calc INT values for return
        pwm = [0, 0]
        pwm[0] = buffer[0] | (buffer[1] << 8)
        pwm[1] = buffer[2] | (buffer[3] << 8)
        return pwm

    # Write 16Bit values to LW18
    def WritePwm16(self, v1, v2):
        v1 = v1 & 0xFFFF  # 0...65535 allowed
        v2 = v2 & 0xFFFF  # 0...65535 allowed

        # Write 4 byte to device
        buffer = [0, 0, 0, 0]  # init with defaults
        buffer[0] = v1 & 0x00FF
        buffer[1] = (v1 & 0xFF00) >> 8
        buffer[2] = v2 & 0x00FF
        buffer[3] = (v2 & 0xFF00) >> 8

        with smbus2.SMBus(self.device[2]) as bus:
            bus.write_i2c_block_data(self.device[1], self.LW18_REG_PWM16, buffer)

        return 0

    def WriteFrequency(self, v1, v2):
        v1 = v1 & 0xFFFF  # 0...65535 allowed
        v2 = v2 & 0xFFFF  # 0...65535 allowed

        # Write 4 byte to device
        buffer = [0, 0, 0, 0]  # init with defaults
        buffer[0] = v1 & 0x00FF  # LSB
        buffer[1] = (v1 & 0xFF00) >> 8  # MSB
        buffer[2] = v2 & 0x00FF  # LSB
        buffer[3] = (v2 & 0xFF00) >> 8  # MSB

        with smbus2.SMBus(self.device[2]) as bus:
            bus.write_i2c_block_data(self.device[1], self.LW18_REG_FREQUENCY, buffer)

        return 0

    @property
    def __relay_nr(self):
        return self.device[0] - 1

    def calibrate(self, data):
        super().calibrate(data)

        frequencies = self.device[3].get_data(self.device[4], [self._DIMMER_FREQ, self._DIMMER_FREQ])
        frequency = data.get("dimmer_frequency", self._DIMMER_FREQ)

        if "" == frequency or frequency < 0:
            frequency = self._DIMMER_FREQ

        frequencies[self.__relay_nr] = int(frequency)

        self.WriteFrequency(frequencies[0], frequencies[1])

        self.device[3].set_data(self.device[4], frequencies, -1)

    def _load_hardware(self):
        # address is expected as `[relay_number],[i2c_address],[i2c_bus (optional)]`
        address = self.address.split(",")
        relay_nr = int(address[0])
        if not (relay_nr >= 1 and relay_nr <= 2):
            raise terrariumRelayLoadingException("Invalid relay number.")

        address[0] = relay_nr

        if not address[1].startswith("0x"):
            address[1] = "0x" + address[1]

        address[1] = int(address[1], 16)

        if len(address) == 2:
            address.append(1)
        else:
            address[2] = int(address[2])

        address.append(terrariumCache())
        address.append(f"{self.HARDWARE}{address[1]}{address[2]}")

        return address

    def _set_hardware_value(self, state):
        pwm = self.ReadPwm16()
        pwm[self.__relay_nr] = int((float(state) / 100.0) * float(self._DIMMER_DIM))

        self.WritePwm16(pwm[0], pwm[1])

        return True

    def _get_hardware_value(self):
        pwm = self.ReadPwm16()

        value = int((float(pwm[self.__relay_nr]) / float(self._DIMMER_DIM)) * 100)

        return value
