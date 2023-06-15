# -*- coding: utf-8 -*-
from . import terrariumDisplay

# pip install i2c_lcd
# pip install smbus2
# pip install pyserial
import i2c_lcd
import smbus2
import serial


class terrariumDisplayLCDI2CMixin:
    def _load_hardware(self):
        address = self._address
        self._device["device"] = i2c_lcd.lcd(address[0])

        # Hack to have better control on the I2C bus. Close old smbus. And use new one (smbus2)
        self._device["device"].lcd_device.bus.close()
        self._device["device"].lcd_device.bus = smbus2.SMBus(1 if len(address) == 1 else int(address[1]))

        self.width = self.WIDTH
        self.height = self.HEIGHT

    def _unload_hardware(self):
        self._device["device"].lcd_device.bus.close()

    def _write_line(self, text, line_nr):
        self._device["device"].lcd_display_string(text, line_nr)

    def _write_title(self):
        self._write_line(self.title[: self.width].ljust(self.width), 1)

    def clear(self):
        self._device["device"].lcd_clear()
        super().clear()


class terrariumDisplayLCDSerialMixin:
    def _load_hardware(self):
        address = self._address
        self._device["device"] = serial.Serial(address[0], baudrate=9600, timeout=1)
        with self._device["device"] as device:
            device.flushInput()

    def _unload_hardware(self):
        pass

    def _write_line(self, text, line_nr):
        with self._device["device"] as device:
            device.write(f"0{line_nr-1}{text}")

    def clear(self):
        for i in range(1, self.height + 1):
            self._write_line("".ljust(self.width), i)

        super().clear()


class terrariumLCD16x2(terrariumDisplay, terrariumDisplayLCDI2CMixin):
    HARDWARE = "LCD16x2I2C"
    NAME = "LCD 16 x 2 display (I2C)"

    WIDTH = 16
    HEIGHT = 2


class terrariumLCD20x4(terrariumDisplay, terrariumDisplayLCDI2CMixin):
    HARDWARE = "LCD20x4I2C"
    NAME = "LCD 20 x 4 display (I2C)"

    WIDTH = 20
    HEIGHT = 4


class terrariumLCDSerial16x2(terrariumDisplay, terrariumDisplayLCDSerialMixin):
    HARDWARE = "LCD16x2Serial"
    NAME = "LCD 16 x 2 display (serial)"

    WIDTH = 16
    HEIGHT = 2


class terrariumLCDSerial20x4(terrariumDisplay, terrariumDisplayLCDSerialMixin):
    HARDWARE = "LCD20x4Serial"
    NAME = "LCD 20 x 4 display (serial)"

    WIDTH = 20
    HEIGHT = 4
