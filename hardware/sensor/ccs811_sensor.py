# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumI2CSensor, terrariumSensorUpdateException

# https://gist.github.com/xxlukas42/60ae08f75e68a0cfcdb7c9dd60145d34
#
# CCS811_RPi
#
# Petr Lukas
# July, 11 2017
#
# Version 1.0

from gevent import sleep
import struct, array, io, fcntl

# I2C Address
CCS811_ADDRESS = 0x5A

# Registers
CCS811_HW_ID = 0x20
CSS811_STATUS = 0x00
CSS811_APP_START = 0xF4
CSS811_MEAS_MODE = 0x01
CSS811_ERROR_ID = 0xE0
CSS811_RAW_DATA = 0x03
CSS811_ALG_RESULT_DATA = 0x02
CSS811_BASELINE = 0x11
CSS811_ENV_DATA = 0x05

# Errors ID
ERROR = {}
ERROR[0] = "WRITE_REG_INVALID"
ERROR[1] = "READ_REG_INVALID"
ERROR[2] = "MEASMODE_INVALID"
ERROR[3] = "MAX_RESISTANCE"
ERROR[4] = "HEATER_FAULT"
ERROR[5] = "HEATER_SUPPLY"

I2C_SLAVE = 0x0703

CCS811_fw = 0
CCS811_fr = 0


class CCS811_RPi:
    def __init__(self, twi=1, addr=CCS811_ADDRESS):
        global CCS811_fr, CCS811_fw

        CCS811_fr = io.open("/dev/i2c-" + str(twi), "rb", buffering=0)
        CCS811_fw = io.open("/dev/i2c-" + str(twi), "wb", buffering=0)

        # set device address
        fcntl.ioctl(CCS811_fr, I2C_SLAVE, addr)
        fcntl.ioctl(CCS811_fw, I2C_SLAVE, addr)
        sleep(0.015)

    # public functions
    def checkHWID(self):
        s = [CCS811_HW_ID]  # Hardware ID
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.0625)

        data = CCS811_fr.read(1)

        buf = array.array("B", data)
        return hex(buf[0])

    def readStatus(self):
        sleep(0.015)

        s = [CSS811_STATUS]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.0625)

        data = CCS811_fr.read(1)
        buf = array.array("B", data)
        return buf[0]

    def checkError(self, status_byte):
        sleep(0.015)
        error_bit = ((status_byte) >> 0) & 1
        if not error_bit:
            return False

        s = [CSS811_ERROR_ID]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.0625)

        data = CCS811_fr.read(1)
        buf = array.array("B", data)
        return ERROR[int(buf[0])]

    def configureSensor(self, configuration):
        # Switch sensor to application mode
        s = [CSS811_APP_START]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.0625)

        s = [CSS811_MEAS_MODE, configuration, 0x00]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.015)
        return

    def readMeasMode(self):
        sleep(0.015)
        s = [CSS811_MEAS_MODE]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.0625)

        data = CCS811_fr.read(1)
        buf = array.array("B", data)
        return bin(buf[0])

    def readRaw(self):
        sleep(0.015)
        s = [CSS811_RAW_DATA]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.0625)

        data = CCS811_fr.read(2)
        buf = array.array("B", data)
        return buf[0] * 256 + buf[1]

    def readAlg(self):
        sleep(0.015)
        s = [CSS811_ALG_RESULT_DATA]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.0625)

        data = CCS811_fr.read(8)
        buf = array.array("B", data)
        result = {}

        # Read eCO2 value and check if it is valid
        result["eCO2"] = buf[0] * 256 + buf[1]
        if result["eCO2"] > 8192:
            return False

        # Read TVOC value and check if it is valid
        result["TVOC"] = buf[2] * 256 + buf[3]
        if result["TVOC"] > 1187:
            return False

        result["status"] = buf[4]

        # Read the last error ID and check if it is valid
        result["errorid"] = buf[5]
        if result["errorid"] > 5:
            return False

        result["raw"] = buf[6] * 256 + buf[7]
        return result

    def readBaseline(self):
        sleep(0.015)
        s = [CSS811_BASELINE]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.0625)

        data = CCS811_fr.read(2)
        buf = array.array("B", data)
        return buf[0] * 256 + buf[1]

    def checkDataReady(self, status_byte):
        ready_bit = ((status_byte) >> 3) & 1
        if ready_bit:
            return True
        else:
            return False

    def setCompensation(self, temperature, humidity):
        temperature = round(temperature, 2)
        humidity = round(humidity, 2)
        hum1 = int(humidity // 0.5)
        hum2 = int(humidity * 512 - hum1 * 256)

        temperature = temperature + 25
        temp1 = int(temperature // 0.5)
        temp2 = int(temperature * 512 - temp1 * 256)

        s = [CSS811_ENV_DATA, hum1, hum2, temp1, temp2, 0x00]
        s2 = bytearray(s)
        CCS811_fw.write(s2)

        return

    def setBaseline(self, baseline):
        buf = [0, 0]
        s = struct.pack(">H", baseline)
        buf[0], buf[1] = struct.unpack(">BB", s)

        s = [CSS811_BASELINE, buf[0], buf[1], 0x00]
        s2 = bytearray(s)
        CCS811_fw.write(s2)
        sleep(0.015)


class terrariumCCS811Sensor(terrariumI2CSensor):
    HARDWARE = "css811"
    TYPES = ["co2"]
    NAME = "CCS811 sensor"

    """
  MEAS MODE REGISTER AND DRIVE MODE CONFIGURATION
  0b0       Idle (Measurements are disabled in this mode)
  0b10000   Constant power mode, IAQ measurement every second
  0b100000  Pulse heating mode IAQ measurement every 10 seconds
  0b110000  Low power pulse heating mode IAQ measurement every 60
  0b1000000 Constant power mode, sensor measurement every 250ms
  """

    # Set MEAS_MODE (measurement interval)
    MODE = 0b100000

    def _load_hardware(self):
        address = self._address
        device = CCS811_RPi(addr=address[0], twi=address[1])
        device.configureSensor(terrariumCCS811Sensor.MODE)

        self.calibrate()

        return device

    def _get_data(self):
        data = None
        try:
            self.device.setCompensation(self.__calibration["temperature"], self.__calibration["humidity"])
            statusbyte = self.device.readStatus()
            error = self.device.checkError(statusbyte)

            if error:
                return None

            if not self.device.checkDataReady(statusbyte):
                return None

            result = self.device.readAlg()
            if not result:
                return None

            if result.get("eCO2", None):
                data = {"co2": result["eCO2"]}

            return data

        except Exception as ex:
            raise terrariumSensorUpdateException(ex)

    def calibrate(self, temperature=20, humidity=50):
        self.__calibration = {
            "temperature": temperature,
            "humidity": humidity,
        }
