# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumSensor
from terrariumUtils import terrariumUtils

from gevent import sleep
from time import time
import pigpio

# http://abyz.me.uk/rpi/pigpio/code/sonar_trigger_echo_py.zip


class terrariumHCSR04Sensor(terrariumSensor):
    HARDWARE = "hc-sr04"
    TYPES = ["distance"]
    NAME = "HC-SR04 ultrasonic ranging sensor"

    def _load_hardware(self):
        address = self._address

        pi = pigpio.pi()
        self._trig = terrariumUtils.to_BCM_port_number(address[0])
        self._echo = terrariumUtils.to_BCM_port_number(address[1])

        self._ping = False
        self._high = None
        self._time = None

        self._triggered = False

        self._trig_mode = pi.get_mode(self._trig)
        self._echo_mode = pi.get_mode(self._echo)

        pi.set_mode(self._trig, pigpio.OUTPUT)
        pi.set_mode(self._echo, pigpio.INPUT)

        self._cb = pi.callback(self._trig, pigpio.EITHER_EDGE, self._cbf)
        self._cb = pi.callback(self._echo, pigpio.EITHER_EDGE, self._cbf)

        return pi

    def _cbf(self, gpio, level, tick):
        if gpio == self._trig:
            if level == 0:  # trigger sent
                self._triggered = True
                self._high = None
        else:
            if self._triggered:
                if level == 1:
                    self._high = tick
                else:
                    if self._high is not None:
                        self._time = tick - self._high
                        self._high = None
                        self._ping = True

    def _get_data(self):
        """
        Triggers a reading.  The returned reading is the number
        of microseconds for the sonar round-trip.

        round trip cms = round trip time / 1000000.0 * 34030
        """
        if self.device is not None:
            self._ping = False
            self.device.gpio_trigger(self._trig)
            start = time()
            while not self._ping:
                if time() - start > 5.0:
                    return None
                sleep(0.001)
            # Return in cm
            return {"distance": round(self._time * 17150.5 / 1000000.0, 3)}
        else:
            return None

    def stop(self):
        """
        Cancels the ranger and returns the gpios to their
        original mode.
        """
        if self.device is not None:
            self._cb.cancel()
            self.device.set_mode(self._trig, self._trig_mode)
            self.device.set_mode(self._echo, self._echo_mode)
            self.device.stop()


class terrariumHCSR04PSensor(terrariumHCSR04Sensor):
    HARDWARE = "hc-sr04p"
    NAME = "HC-SR04P ultrasonic ranging sensor"


class terrariumJSNSR04TSensor(terrariumHCSR04Sensor):
    HARDWARE = "jsn-sr04t"
    NAME = "JSN-SR04T ultrasonic ranging sensor"
