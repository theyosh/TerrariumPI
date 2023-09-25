# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

import RPi.GPIO as GPIO
from gevent import sleep
import threading

from . import terrariumButton


class terrariumLDRSensor(terrariumButton):
    HARDWARE = "ldr"
    NAME = "Light sensor"

    __CAPACITOR = 1  # in uF

    def __run(self):
        self._checker["running"] = True
        while self._checker["running"]:
            count = 0

            # Output on the pin for
            GPIO.setup(self._device["device"], GPIO.OUT)
            GPIO.output(self._device["device"], False)
            sleep(0.1)

            # Change the pin back to input
            GPIO.setup(self._device["device"], GPIO.IN)

            # Count until the pin goes high
            # We found out that a value of capacitor value * 10000 is pretty correct for detecting if there is light
            try:
                while (
                    self._checker["running"]
                    and count <= (self.__CAPACITOR * 10000) + 1
                    and GPIO.input(self._device["device"]) == 0
                ):
                    count += 1

                self._device["internal_state"] = self.PRESSED if count <= (self.__CAPACITOR * 10000) else self.RELEASED
                sleep(0.1)

            except KeyboardInterrupt as ex:
                self._checker["running"] = False
                print(f"Fetch CTRL-c... and now what..? For now.. press again Ctrl-C .. ({ex})")
                self.stop()

    def _get_state(self):
        return self._device["internal_state"]

    def _load_hardware(self):
        self._device["internal_state"] = self.RELEASED

        self.__thread = threading.Thread(target=self.__run)
        self.__thread.start()

        # For the first reading, wait a bit....
        sleep(0.25)

    def calibrate(self, calibration_data):
        super().calibrate(calibration_data)
        self.__CAPACITOR = int(calibration_data.get("ldr_capacitor", self.__CAPACITOR))

    def stop(self):
        self._checker["running"] = False
        try:
            self.__thread.join()
        except Exception as ex:
            logger.debug(f"Could not join thread to wait for: {ex}")

        super().stop()

    @property
    def is_light(self):
        return self.pressed

    @property
    def is_dark(self):
        return not self.is_light
