from . import terrariumRelay
from terrariumUtils import terrariumUtils

# pip install pylibftdi
# https://pylibftdi.readthedocs.io/en/latest/
from pylibftdi import Driver, BitBangDevice, SerialDevice


class terrariumRelayFTDI(terrariumRelay):
    HARDWARE = "ftdi"
    NAME = "FTDI devices"

    SERIAL = 0
    BITBANG = 1

    BITBANG_ADDRESSES = {
        "1": "2",
        "2": "8",
        "3": "20",
        "4": "80",
        "5": "1",
        "6": "4",
        "7": "10",
        "8": "40",
        "all": "FF",
    }

    @property
    def _address(self):
        address = super()._address
        if len(address) == 1:
            address.append(1)
        elif address[1] is None or "" == address[1]:
            address[1] = 1

        address[0] = int(address[0])
        return address

    def _load_hardware(self):
        # Address value = Switch_number,board_serial (optional). When board_serial is missing, use the first found device and update the address....
        address = self._address

        number_mode = terrariumUtils.is_float(address[1])
        counter = 1
        for _, device_type, serial in Driver().list_devices():
            # Loop until we reach the number (amount) or serial that is entered
            if (number_mode and counter != address[1]) or (not number_mode and address[1] != serial):
                counter += 1
                continue

            device_type = (
                terrariumRelayFTDI.SERIAL if device_type.lower().endswith("uart") else terrariumRelayFTDI.BITBANG
            )

            self.address = f"{address[0]},{serial}"

            return (serial, device_type)

    def _set_hardware_value(self, state):
        (serial, device_type) = self.device

        if device_type == terrariumRelayFTDI.SERIAL:
            with SerialDevice(serial) as device:
                device.baudrate = 9600
                cmd = chr(0xFF) + chr(0x0 + self._address[0]) + chr(0x0 + (1 if state == self.ON else 0))
                device.write(cmd)

        elif device_type == terrariumRelayFTDI.BITBANG:
            with BitBangDevice(serial) as device:
                device.baudrate = 9600
                if state == self.ON:
                    device.port |= int(terrariumRelayFTDI.BITBANG_ADDRESSES[str(self._address[0])], 16)
                else:
                    device.port &= ~int(terrariumRelayFTDI.BITBANG_ADDRESSES[str(self._address[0])], 16)

        return True

    def _get_hardware_value(self):
        def get_relay_state(data, relay):
            def testBit(int_type, offset):
                mask = 1 << offset
                return int_type & mask

            if relay == "1":
                return testBit(data, 1)
            if relay == "2":
                return testBit(data, 3)
            if relay == "3":
                return testBit(data, 5)
            if relay == "4":
                return testBit(data, 7)
            if relay == "5":
                return testBit(data, 2)
            if relay == "6":
                return testBit(data, 4)
            if relay == "7":
                return testBit(data, 6)
            if relay == "8":
                return testBit(data, 8)

        data = None
        (serial, device_type) = self.device
        if device_type == terrariumRelayFTDI.SERIAL:
            # As we cannot read out this device, we borrow the current state as the new state....
            data = 1 if self.state == self.ON else 0

        elif device_type == terrariumRelayFTDI.BITBANG:
            with BitBangDevice(serial) as device:
                device.baudrate = 9600
                data = int(get_relay_state(device.port, str(self._address[0])))

        if data is None:
            return None

        return self.ON if data > 0 else self.OFF

    @staticmethod
    def _scan_relays(callback=None, **kwargs):
        device_nr = 0
        for _, _, serial in Driver().list_devices():
            device_nr += 1
            # It is impossible to detect amount of relays per board. So we can only auto discover 4 at maximum.
            for x in range(4):
                # Explicit None value for ID. This will force to generate a new ID based on the address
                yield terrariumRelay(
                    None,
                    terrariumRelayFTDI.HARDWARE,
                    f"{x+1},{serial}",
                    f"{terrariumRelayFTDI.NAME} device nr: {device_nr}({serial}) socket: {x+1}",
                    {},
                    callback=callback,
                )
