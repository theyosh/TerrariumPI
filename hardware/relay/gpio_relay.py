from . import terrariumRelay
from terrariumUtils import terrariumUtils

# pip install gpiozero
from gpiozero import OutputDevice

from hardware.io_expander import terrariumIOExpander, terrariumPCF8574IOExpander, terrariumPCF8575IOExpander

# For traditional GPIO the inverse is fixed by setting active_high to HIGH
# For IO Expander we do it by hand


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
                device = terrariumPCF8574IOExpander(",".join(address[1:]))
            elif address[0].lower().startswith("pcf8575-"):
                device = terrariumPCF8575IOExpander(",".join(address[1:]))

            return device

        else:
            return OutputDevice(
                terrariumUtils.to_BCM_port_number(self._address[0]), active_high=not self.INVERSE, initial_value=None
            )

    def _set_hardware_value(self, state) -> bool:
        if isinstance(self.device, terrariumIOExpander):
            if self.INVERSE:
                state = self.ON if state == self.OFF else self.OFF

            port = int(self._address[0].split("-")[1])
            if state == self.ON:
                self.device.switch_on(port)
            else:
                self.device.switch_off(port)

        else:
            if state == self.ON:
                self.device.on()
            else:
                self.device.off()

        return True

    def _get_hardware_value(self):
        state = None

        if isinstance(self.device, terrariumIOExpander):
            state = self.device.is_on(int(self._address[0].split("-")[1]))
            if self.INVERSE:
                state = self.ON if state == False else self.OFF

        else:
            state = self.device.value

        if state is None:
            return None

        state = self.OFF if terrariumUtils.is_true(state) == False else self.ON

        return state

    def calibrate(self, data) -> None:
        self.calibration = data
        self.INVERSE = terrariumUtils.is_true(self.calibration.get("inverse", False))

    def stop(self) -> None:
        # TODO: This will toggle down the relay while restarting TP. Not sure if we want to change that and keep relay on while restarting
        self.device.close()
        super().stop()
