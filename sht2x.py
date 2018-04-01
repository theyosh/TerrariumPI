# -*- coding: utf-8 -*-
# Shamelessly copied from: https://github.com/iotify/custom-lab/blob/master/sht2x.py
import fcntl
import time

class SHT21:
    """Class to read temperature and humidity from SHT21, much of class was
    derived from:
    http://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/Humidity/Sensirion_Humidity_SHT21_Datasheet_V3.pdf
    and Martin Steppuhn's code from http://www.emsystech.de/raspi-sht21"""

    # control constants
    _SOFTRESET = 0xFE
    _I2C_ADDRESS = 0x40
    _TRIGGER_TEMPERATURE_NO_HOLD = 0xF3
    _TRIGGER_HUMIDITY_NO_HOLD = 0xF5
    _STATUS_BITS_MASK = 0xFFFC

    # From: /linux/i2c-dev.h
    I2C_SLAVE = 0x0703
    I2C_SLAVE_FORCE = 0x0706

    # datasheet (v4), page 9, table 7, thanks to Martin Milata
    # for suggesting the use of these better values
    # code copied from https://github.com/mmilata/growd
    _TEMPERATURE_WAIT_TIME = 0.086  # (datasheet: typ=66, max=85)
    _HUMIDITY_WAIT_TIME = 0.030     # (datasheet: typ=22, max=29)

    def __init__(self, device_number=1, address=0x40):
        """Opens the i2c device (assuming that the kernel modules have been
        loaded).  Note that this has only been tested on first revision
        raspberry pi where the device_number = 0, but it should work
        where device_number=1"""
        self.i2c = open('/dev/i2c-%s' % device_number, 'r+', 0)
        fcntl.ioctl(self.i2c, self.I2C_SLAVE, address)
        self.i2c.write(chr(self._SOFTRESET))
        time.sleep(0.100)

    def read_temperature(self):
        """Reads the temperature from the sensor.  Not that this call blocks
        for ~86ms to allow the sensor to return the data"""
        self.i2c.write(chr(self._TRIGGER_TEMPERATURE_NO_HOLD))
        time.sleep(self._TEMPERATURE_WAIT_TIME)
        data = self.i2c.read(3)
        if self._calculate_checksum(data, 2) == ord(data[2]):
            return self._get_temperature_from_buffer(data)

    def read_humidity(self):
        """Reads the humidity from the sensor.  Not that this call blocks
        for ~30ms to allow the sensor to return the data"""
        self.i2c.write(chr(self._TRIGGER_HUMIDITY_NO_HOLD))
        time.sleep(self._HUMIDITY_WAIT_TIME)
        data = self.i2c.read(3)
        if self._calculate_checksum(data, 2) == ord(data[2]):
            return self._get_humidity_from_buffer(data)

    def close(self):
        """Closes the i2c connection"""
        self.i2c.close()

    def __enter__(self):
        """used to enable python's with statement support"""
        return self

    def __exit__(self, type, value, traceback):
        """with support"""
        self.close()

    @staticmethod
    def _calculate_checksum(data, number_of_bytes):
        """5.7 CRC Checksum using the polynomial given in the datasheet"""
        # CRC
        POLYNOMIAL = 0x131  # //P(x)=x^8+x^5+x^4+1 = 100110001
        crc = 0
        # calculates 8-Bit checksum with given polynomial
        for byteCtr in range(number_of_bytes):
            crc ^= (ord(data[byteCtr]))
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ POLYNOMIAL
                else:
                    crc = (crc << 1)
        return crc

    @staticmethod
    def _get_temperature_from_buffer(data):
        """This function reads the first two bytes of data and
        returns the temperature in C by using the following function:
        T = =46.82 + (172.72 * (ST/2^16))
        where ST is the value from the sensor
        """
        unadjusted = (ord(data[0]) << 8) + ord(data[1])
        unadjusted &= SHT21._STATUS_BITS_MASK  # zero the status bits
        unadjusted *= 175.72
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 46.85
        return unadjusted

    @staticmethod
    def _get_humidity_from_buffer(data):
        """This function reads the first two bytes of data and returns
        the relative humidity in percent by using the following function:
        RH = -6 + (125 * (SRH / 2 ^16))
        where SRH is the value read from the sensor
        """
        unadjusted = (ord(data[0]) << 8) + ord(data[1])
        unadjusted &= SHT21._STATUS_BITS_MASK  # zero the status bits
        unadjusted *= 125.0
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 6
        return unadjusted


if __name__ == "__main__":
    try:
        with SHT21(1) as sht21:
            print "Temperature: %s" % sht21.read_temperature()
            print "Humidity: %s" % sht21.read_humidity()
    except IOError, e:
        print e
        print "Error creating connection to i2c.  This must be run as root"
