from . import terrariumRelay
from terrariumUtils import terrariumUtils

# pip install gpiozero
from gpiozero import LED

from hardware.io_expander import terrariumIOExpander


class terrariumRelayGPIO(terrariumRelay):
    HARDWARE = "gpio"
    NAME = "GPIO devices"
    INVERSE = False

    def _load_hardware(self):
        address = self._address
        self.INVERSE = terrariumUtils.is_true(self.calibration.get("inverse", False))

        if len(address) >= 2:
            # IO Expander in use...
            device = None
            if address[0].lower().startswith("pcf8574-"):
                device = terrariumIOExpander("PCF8574", ",".join(address[1:]))

            if device is not None:
                device.set_port(int(address[0].split("-")[1]))

            return device

        else:
            return LED(terrariumUtils.to_BCM_port_number(self._address[0]), initial_value=None)

    def _set_hardware_value(self, state):
        if self.INVERSE:
            state = self.ON if state == self.OFF else self.OFF

        if isinstance(self.device, terrariumIOExpander):
            self.device.state = state == self.ON

        else:
            if state == self.ON:
                self.device.on()
            else:
                self.device.off()

        return True

    def _get_hardware_value(self):
        state = None

        if isinstance(self.device, terrariumIOExpander):
            state = self.device.state

        else:
            state = self.device.is_lit

        if state is None:
            return None

        state = terrariumUtils.is_true(state)
        if self.INVERSE:
            state = self.ON if state == False else self.OFF
        else:
            state = self.OFF if state == False else self.ON

        return state

    def calibrate(self, data):
        self.calibration = data
        self.INVERSE = terrariumUtils.is_true(self.calibration.get("inverse", False))

    def stop(self):
        # TODO: This will toggle down the relay while restarting TP. Not sure if we want to change that and keep relay on while restarting
        self.device.close()
        super().stop()
