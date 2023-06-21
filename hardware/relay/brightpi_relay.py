from . import terrariumRelayDimmer

import statistics
import sys
from pathlib import Path

# https://github.com/PiSupply/Bright-Pi
# Dirty hack to include someone his code... to lazy to make it myself :)
# Also, do not want to compile stuff....
sys.path.insert(0, str((Path(__file__).parent / Path("../../3rdparty/Bright-Pi/brightpi")).resolve()))
import brightpilib as brightpi


class terrariumRelayDimmerBrightPi(terrariumRelayDimmer):
    HARDWARE = "brightpi-dimmer"
    NAME = "Bright-PI (dimmer)"

    def _load_hardware(_):
        device = brightpi.BrightPi()
        # By resetting, we lose the old state after a reboot.....
        device.reset()

        return device

    def _set_hardware_value(self, state):
        leds = brightpi.LED_IR if "ir" == self._address[-1].lower() else brightpi.LED_WHITE

        led_status = self.device.get_led_on_off(leds)
        on = all([led_status[led - 1] for led in leds])

        dim_value = round(self.device._max_dim * (state / 100.0))
        self.device.set_led_dim(leds, dim_value)

        if state > 0 and not on:
            self.device.set_led_on_off(leds, brightpi.ON)
        elif state == 0 and on:
            self.device.set_led_on_off(leds, brightpi.OFF)

        return True

    def _get_hardware_value(self):
        leds = brightpi.LED_IR if "ir" == self._address[-1].lower() else brightpi.LED_WHITE
        if all(v == 0 for v in self.device.get_led_on_off(leds)):
            # LEDS needs to be on, to have a valid dimming value
            return self.OFF

        led_status = self.device.get_led_dim()
        avg = statistics.mean([led_status[led - 1] for led in leds]) / self.device._max_dim * 100
        return round(avg)

    def calibrate(self, data):
        max_power = int(data.get("dimmer_max_power", -1))
        if 0 <= max_power <= 100:
            self.ON = max_power
            if self.state > self.ON:
                self.set_state(self.ON)
