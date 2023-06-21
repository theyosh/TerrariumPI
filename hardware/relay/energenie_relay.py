# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumRelay, terrariumRelayLoadingException, terrariumRelayUpdateException
from terrariumUtils import terrariumUtils, terrariumCache

import subprocess
import re
import sys
from pathlib import Path
from hashlib import md5

# Dirty hack to include someone his code... to lazy to make it myself :)
# https://github.com/perryflynn/energenie-connect0r
sys.path.insert(0, str((Path(__file__).parent / Path("../../3rdparty/energenie-connect0r")).resolve()))

import energenieconnector

# pip install gpiozero
from gpiozero import Energenie


class terrariumRelayEnergenieUSB(terrariumRelay):
    HARDWARE = "eg-pm-usb"
    NAME = "Energenie USB"

    __CMD = "/usr/local/bin/sispmctl" if Path("/usr/local/bin/sispmctl").exists() else "/usr/bin/sispmctl"
    __STATUS_REGEX = re.compile(r"(Status of|Switched) outlet\s*(?P<relay_nr>\d+):?\s*(?P<status>[0,1])", re.IGNORECASE)
    __SCAN_REGEX = re.compile(r"^(?P<option>[^:]+):\s*(?P<value>.*)$", re.IGNORECASE)

    def _load_hardware(self):
        if not Path(self.__CMD).exists():
            raise terrariumRelayLoadingException(
                "Please install tool 'sispmctl'. Can't controll EnergenieUSB relays without it."
            )

        address = self._address
        if len(address) == 1:
            address.append(1)
        elif address[1] is None or "" == address[1]:
            address[1] = 1

        mode = "-d" if terrariumUtils.is_float(address[1]) else "-D"
        device = " ".join([self.__CMD, mode, str(address[1] if "-D" == mode else int(address[1]) - 1)])

        # TEMP data. Will be overwritten by the return value later on
        self._device["device"] = device

        if self._get_hardware_value() in [self.ON, self.OFF]:
            return device

        raise terrariumRelayLoadingException(f"Could not find the relay {self}.")

    def _set_hardware_value(self, state):
        action = "-o" if state == self.ON else "-f"
        cmd = f"{self.device} -n {action} {self._address[0]}"
        data = terrariumUtils.get_script_data(cmd)
        if data is None:
            return False

        data = data.decode("utf-8").strip()
        relay_data = self.__STATUS_REGEX.search(data)
        if relay_data is not None and int(relay_data.group("relay_nr")) == int(self._address[0]):
            return state == (self.ON if terrariumUtils.is_true(relay_data.group("status")) else self.OFF)

        return False

    def _get_hardware_value(self):
        cmd = f"{self.device} -n -g {self._address[0]}"
        data = terrariumUtils.get_script_data(cmd)
        if data is None:
            return None

        data = data.decode("utf-8").strip()
        relay_data = self.__STATUS_REGEX.search(data)
        if relay_data is not None and int(relay_data.group("relay_nr")) == int(self._address[0]):
            return self.ON if terrariumUtils.is_true(relay_data.group("status")) else self.OFF

        return None

    @staticmethod
    def _scan_relays(callback=None, **kwargs):
        cmd = f"{terrariumRelayEnergenieUSB.__CMD} -s"

        data = []
        try:
            data = terrariumUtils.get_script_data(cmd).decode("utf-8").strip().split("\n")
        except subprocess.CalledProcessError:
            logger.info("No Energenie USB relays connected.")
            return False
        except FileNotFoundError:
            raise terrariumRelayLoadingException(
                "Please install tool 'sispmctl'. Can't control EnergenieUSB relays without it."
            )

        amount_sockets = 1
        serial = None
        device_nr = 0

        for line in data:
            line = terrariumRelayEnergenieUSB.__SCAN_REGEX.search(line)
            if line is None:
                continue

            if "device type" == line.group("option").strip().lower():
                # By default 1 socket (at least)
                amount_sockets = 1
                if "socket" in line.group("value").strip().lower():
                    amount_sockets = int(line.group("value").strip()[0])

            elif "serial number" == line.group("option").strip().lower():
                serial = line.group("value").strip()

            if serial is not None:
                # Add the relays
                device_nr += 1
                for x in range(amount_sockets):
                    yield terrariumRelay(
                        None,
                        terrariumRelayEnergenieUSB.HARDWARE,
                        f"{x+1},{serial}",
                        f"{terrariumRelayEnergenieUSB.NAME} device nr: {device_nr}({serial}), Socket: {x+1}",
                        callback=callback,
                    )

                # Reset for new device
                serial = None


class terrariumRelayEnergenieLAN(terrariumRelay):
    HARDWARE = "eg-pm-lan"
    NAME = "Energenie LAN"

    __URL_REGEX = re.compile(
        r"^(?P<protocol>https?):\/\/(((?P<user>[^:]+):)?(?P<passwd>[^@]+)?@)?(?P<host>[^#\/]+)(\/)?(#(?P<nr>\d+))?$",
        re.IGNORECASE,
    )

    @property
    def _address(self):
        address = None
        data = self.__URL_REGEX.match(self.address)
        if data:
            address = data.groupdict()
            if "nr" not in address or address["nr"] is None or "" == address["nr"]:
                address["nr"] = 1

            address["nr"] = int(address["nr"])

        return address

    def __connect(self):
        status = self.device.getstatus()
        if status["login"] == 1:
            if self.device.login():
                status = self.device.getstatus()

        return status["login"] == 0

    def __logout(self):
        status = self.device.getstatus()
        if status["login"] == 0:
            self.device.logout()

    def _load_hardware(self):
        # Input format should be either:
        # - http://[HOST]#[POWER_SWITCH_NR]
        # - http://[HOST]/#[POWER_SWITCH_NR]
        # - http://[PASSWORD]@[HOST]#[POWER_SWITCH_NR]
        # - http://[PASSWORD]@[HOST]/#[POWER_SWITCH_NR]

        address = self._address
        # TEMP data. Will be overwritten by the return value later on
        self._device["device"] = energenieconnector.EnergenieConnector(
            f'{address["protocol"]}://{address["host"]}', address.get("passwd", "")
        )
        if not self.__connect():
            raise terrariumRelayLoadingException(f"Failed loading relay {self}. Unable to login")

        # Create the cache key for caching the relay states.
        # This is usefull when there are more then 1 relay per hardware device.
        self.__cache_key = md5(f'{self.HARDWARE}{address["host"]}'.encode()).hexdigest()
        self.__cache = terrariumCache()

        self.__logout()

        return self._device["device"]

    def _set_hardware_value(self, state):
        if not self.__connect():
            raise terrariumRelayUpdateException(f"Failed changing relay {self}. Unable to login")

        address = self._address
        toggle_ok = self.device.changesocket(address["nr"], (1 if state == self.ON else 0))
        self.__logout()

        return toggle_ok

    def _get_hardware_value(self):
        data = self.__cache.get_data(self.__cache_key)
        if data is None:
            # Cache is expired, so we update with new data
            # Get the overall state information
            if not self.__connect():
                raise terrariumRelayUpdateException(f"Failed updating relay {self}. Unable to login")

            data = self.device.getstatus()

            if data is None:
                return None

            self.__cache.set_data(self.__cache_key, data, self._CACHE_TIMEOUT)

        address = self._address
        status = self.ON if terrariumUtils.is_true(data["sockets"][address["nr"] - 1]) else self.OFF
        self.__logout()

        return status

    def stop(self):
        self.__logout()
        super().stop()


class terrariumRelayEnergenieRF(terrariumRelay):
    HARDWARE = "eg-pm-rf"
    NAME = "Energenie RF"

    def _load_hardware(self):
        return Energenie(int(self.address))

    def _set_hardware_value(self, state):
        if state == self.ON:
            self.device.on()
        else:
            self.device.off()

        return True

    def _get_hardware_value(self):
        return self.ON if terrariumUtils.is_true(self.device.value) else self.OFF

    def stop(self):
        self.device.close()
        super().stop()
