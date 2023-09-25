# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)
from terrariumUtils import terrariumUtils
from gevent import sleep
import threading

from . import terrariumButton


class terrariumRemoteButton(terrariumButton):
    HARDWARE = "remote"
    NAME = "Remote button"

    __TIMEOUT = 10

    def __run(self):
        self._checker["running"] = True
        while self._checker["running"]:
            try:
                value = 1 if int(terrariumUtils.get_remote_data(self._device["device"])) != 0 else 0
                self._device["internal_state"] = value
            except Exception as ex:
                logger.warning(f"Could not update remote button: {ex}")

            sleep(self.__TIMEOUT)

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
        self.__TIMEOUT = int(calibration_data.get("timeout", self.__TIMEOUT))

    def stop(self):
        self._checker["running"] = False
        try:
            self.__thread.join()
        except Exception as ex:
            logger.debug(f"Could not join thread to wait for: {ex}")

        super().stop()

    @property
    def is_open(self):
        return self.pressed

    @property
    def is_closed(self):
        return not self.is_open

    @property
    def is_light(self):
        return self.pressed

    @property
    def is_dark(self):
        return not self.is_light

    @property
    def motion(self):
        return self.pressed

    @property
    def no_motion(self):
        return not self.motion
