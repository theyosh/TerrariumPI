# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumI2CSensor

# Source: http://www.pibits.net/code/am2320-temperature-and-humidity-sensor-and-raspberry-pi-example.php#codesyntax_1
# Slightly modified by TheYOSH
import posix
from fcntl import ioctl
from time import sleep


class AM2320:
    I2C_ADDR = 0x5C
    I2C_SLAVE = 0x0703

    def __init__(self, i2cbus=1, address=I2C_ADDR):
        self._i2cbus = i2cbus
        self._address = address

    @staticmethod
    def _calc_crc16(data):
        crc = 0xFFFF

        for x in data:
            crc = crc ^ x
            for _ in range(0, 8):
                if (crc & 0x0001) == 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1

        return crc

    @staticmethod
    def _combine_bytes(msb, lsb):
        return msb << 8 | lsb

    def readSensor(self):
        fd = posix.open("/dev/i2c-%d" % self._i2cbus, posix.O_RDWR)
        ioctl(fd, self.I2C_SLAVE, self._address)
        # wake AM2320 up, goes to sleep to not warm up and affect the humidity sensor
        # This write will fail as AM2320 won't ACK this write
        try:
            posix.write(fd, b"\0x00")
        except Exception:
            logger.debug(f"Woke up sensor {self}")

        sleep(0.002)  # Wait at least 0.8ms, at most 3ms
        # write at addr 0x03, start reg = 0x00, num regs = 0x04 */
        data = []
        try:
            posix.write(fd, b"\x03\x00\x04")

            sleep(0.0020)  # Wait at least 1.5ms for result

            # Read out 8 bytes of result data
            # Byte 0: Should be Modbus function code 0x03
            # Byte 1: Should be number of registers to read (0x04)
            # Byte 2: Humidity msb
            # Byte 3: Humidity lsb
            # Byte 4: Temperature msb
            # Byte 5: Temperature lsb
            # Byte 6: CRC lsb byte
            # Byte 7: CRC msb byte
            data = bytearray(posix.read(fd, 8))
        except Exception:
            pass
        finally:
            posix.close(fd)

        # Check data[0] and data[1]
        if data[0] != 0x03 or data[1] != 0x04:
            raise Exception("First two read bytes are a mismatch")

        # CRC check
        if self._calc_crc16(data[0:6]) != self._combine_bytes(data[7], data[6]):
            raise Exception("CRC failed")

        # Temperature resolution is 16Bit,
        # temperature highest bit (Bit15) is equal to 1 indicates a
        # negative temperature, the temperature highest bit (Bit15)
        # is equal to 0 indicates a positive temperature;
        # temperature in addition to the most significant bit (Bit14 ~ Bit0)
        # indicates the temperature sensor string value.
        # Temperature sensor value is a string of 10 times the
        # actual temperature value.
        temp = self._combine_bytes(data[4], data[5])
        if temp & 0x8000:
            temp = -(temp & 0x7FFF)
            temp /= 10.0
        else:
            temp /= 10.0

        humi = self._combine_bytes(data[2], data[3]) / 10.0
        return (temp, humi)


class terrariumAM2320Sensor(terrariumI2CSensor):
    HARDWARE = "am2320"
    TYPES = ["temperature", "humidity"]
    NAME = "AM2320 sensor"

    def _load_hardware(self):
        address = self._address
        device = AM2320(address[1], address[0])
        return device

    def _get_data(self):
        data = {}
        values = self.device.readSensor()
        data["temperature"] = values[0]
        data["humidity"] = values[1]
        return data
