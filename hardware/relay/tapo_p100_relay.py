from . import terrariumRelay
from terrariumUtils import terrariumUtils

# pip install git+https://github.com/almottier/TapoP100.git
from PyP100 import PyP100
from hashlib import md5

class terrariumRelayTAPOP100(terrariumRelay):
    HARDWARE = "tapop100"
    NAME = "TAPO P100/5"

    # This will update the device based in mac address
    def load_hardware(self):
        super().load_hardware()
        # Always overrule the ID generating, as we want to use the MAC as that is unique if the IP address is changing
        data = self.device.getDeviceInfo()
        self.id = md5(f"{self.HARDWARE}{data['mac'].lower()}".encode()).hexdigest()

    def _load_hardware(self):
        address = self.address.split(",")

        # address: [IP],[EMAIL],[PASSWORD]
        device = PyP100.P100(address[0].strip(), address[1].strip(), address[2].strip())
        device.handshake()
        device.login()

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

        # In testing mode, we just return the current state
        return self.ON if terrariumUtils.is_true(data["device_on"]) else self.OFF
