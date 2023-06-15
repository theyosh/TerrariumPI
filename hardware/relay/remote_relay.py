from . import terrariumRelay, terrariumRelayDimmer, terrariumRelayLoadingException
from terrariumUtils import terrariumUtils


class terrariumRelayRemote(terrariumRelay):
    HARDWARE = "remote"
    NAME = "Remote power switch (API)"

    def _load_hardware(self):
        if terrariumUtils.parse_url(self.address):
            return self.address

        raise terrariumRelayLoadingException(f"Invalid url for relay {self}")

    # Overrule the main set_hardware_state function, as this is not yet possible (maybe a post action)
    def set_hardware_state(self, state, force=False):
        pass

    def _get_hardware_value(self):
        data = terrariumUtils.get_remote_data(self.device)
        if data is None:
            return None

        data = float(data)
        return data


class terrariumRelayDimmerRemote(terrariumRelayDimmer):
    HARDWARE = "remote-dimmer"
    NAME = "Remote dimmer (API)"

    def _load_hardware(self):
        if terrariumUtils.parse_url(self.address):
            return self.address

        raise terrariumRelayLoadingException(f"Invalid url for relay {self}")

    # Overrule the main set_hardware_state function, as this is not yet possible (maybe a post action)
    def set_hardware_state(self, state, force=False):
        pass

    def _get_hardware_value(self):
        data = terrariumUtils.get_remote_data(self.device)
        if data is None:
            return None

        data = float(data)
        return data
