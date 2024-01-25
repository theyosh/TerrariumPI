from . import terrariumRelay
from terrariumUtils import terrariumUtils

# pip install PyP100
from PyP100 import PyP100


class terrariumRelayTAPOP100(terrariumRelay):
    HARDWARE = "tapop100"
    NAME = "TAPO P100/5"

    def _load_hardware(self):
        address = self.address.split(",")
        print('Parsed address')
        print(address)

        print('Loading TAPO device')
        try:
            # address: [IP],[EMAIL],[PASSWORD]
            device = PyP100.P100(address[0].strip(), address[1].strip(), address[2].strip())
            print('Start handshaking')
            device.handshake()
            print('Login to device')
            device.login()
            print('All good, return device')
        except Exception as ex:
            print('Something went wrong..??')
            print(ex)
            return None

        return device

    def _set_hardware_value(self, state):
        if state == self.ON:
            self.device.turnOn()
        else:
            self.device.turnOff()

        # Always return True here, as this should indicate the toggle changed succeeded
        return True

    def _get_hardware_value(self):
        data = self.device.getDeviceInfo()
        print("Get current state:")
        print(data)

        # In testing mode, we just return the current state
        return self.ON if terrariumUtils.is_true(self.state) else self.OFF
