# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

import statistics
from hashlib import md5
from time import time, sleep
from func_timeout import func_timeout, FunctionTimedOut

# pip install retry
from retry import retry

# For analog sensors and GPIO power management
from gpiozero import MCP3008, LED

# For I2C sensors
import smbus2

# Bluetooth sensors
from bluepy.btle import Scanner

from terrariumUtils import terrariumUtils, terrariumCache, classproperty


class terrariumSensorException(Exception):
    pass


class terrariumSensorUnknownHardwareException(terrariumSensorException):
    pass


class terrariumSensorInvalidSensorTypeException(terrariumSensorException):
    pass


class terrariumSensorLoadingException(terrariumSensorException):
    pass


class terrariumSensorUpdateException(terrariumSensorException):
    pass


class terrariumSensor(object):
    HARDWARE = None
    TYPES = []
    NAME = None

    _CACHE_TIMEOUT = 30
    _UPDATE_TIME_OUT = 10

    @classproperty
    def available_hardware(__cls__):
        known_sensors = terrariumUtils.loadHardwareDrivers(__cls__, __name__, __file__, "*_sensor.py")

        # Filter out bluetooth sensors if bluetooth is disabled
        if not terrariumUtils.bluetooth_available():
            known_sensors = dict(
                filter(lambda key: not issubclass(key[1], terrariumBluetoothSensor), known_sensors.items())
            )

        # Update sensors that do not have a known type. Those are remote and scripts sensors
        # Using sum() for fastest way of flatten a list https://stackoverflow.com/a/716489
        all_types = list(set(sum([known_sensors[sensor].TYPES for sensor in known_sensors], [])))
        for hardware in known_sensors:
            if len(known_sensors[hardware].TYPES) == 0:
                known_sensors[hardware].TYPES = all_types

        return known_sensors

    # Return a list with type and names of supported switches
    @classproperty
    def available_sensors(__cls__):
        data = [
            {"hardware": hardware_type, "name": sensor.NAME, "types": sensor.TYPES}
            for hardware_type, sensor in __cls__.available_hardware.items()
            if sensor.NAME is not None
        ]
        # not sure why sum works here: https://stackoverflow.com/a/18114563
        all_types = list(set(sum([sensor["types"] for sensor in data], []))) + ["conductivity"]

        # Remote and script sensors can handle all the known types
        for sensor in data:
            if len(sensor["types"]) == 0:
                sensor["types"] = all_types

        return data

    @classproperty
    def sensor_types(__cls__):
        return list(set(sum([sensor["types"] for sensor in __cls__.available_sensors], [])))

    # Return polymorph sensor....
    def __new__(cls, _, hardware_type, sensor_type, address, name="", unit_value_callback=None, trigger_callback=None):
        known_sensors = terrariumSensor.available_hardware
        try:
            return super(terrariumSensor, cls).__new__(known_sensors[hardware_type])
        except:
            if hardware_type not in known_sensors:
                raise terrariumSensorUnknownHardwareException(
                    f"Trying to load an unknown sensor device {hardware_type} at address {address} with name {name}"
                )
            else:
                raise terrariumSensorInvalidSensorTypeException(
                    f"Hardware does not have a {sensor_type} sensor at address {address} with name {name}"
                )

    def __init__(self, sensor_id, _, sensor_type, address, name="", unit_value_callback=None, trigger_callback=None):
        self._device = {
            "id": None,
            "name": None,
            "address": None,
            "type": sensor_type,  # Readonly property
            "device": None,
            "cache_key": None,
            "power_mngt": None,
            "erratic_errors": 0,
            "last_update": 0,
            "value": None,
        }

        self._sensor_cache = terrariumCache()

        # Set the properties
        self.id = sensor_id
        self.name = name
        self.address = address

        # Load hardware can update the address value that is used for making a unique ID when not set
        self.load_hardware()
        # REMINDER: We do not take a measurement at this point. That is up to the developer to explicit request an update.

    def __power_management(self, on):
        # Some kind of 'power management' with the last gpio pin number :) https://raspberrypi.stackexchange.com/questions/68123/preventing-corrosion-on-yl-69
        if self._device["power_mngt"] is not None:
            logger.debug(f"Sensor {self} has power management enabled")
            if on:
                logger.debug("Enable power to the sensor {self} now.")
                self._device["power_mngt"].on()
                sleep(1)
            else:
                logger.debug("Close power to the sensor {self} now.")
                self._device["power_mngt"].off()

    @property
    def _sensor_cache_key(self):
        if self._device["cache_key"] is None:
            self._device["cache_key"] = md5(f"{self.HARDWARE}{self.address}".encode()).hexdigest()

        return self._device["cache_key"]

    @property
    def id(self):
        if self._device["id"] is None:
            self._device["id"] = md5(f"{self.HARDWARE}{self.address}{self.type}".encode()).hexdigest()

        return self._device["id"]

    @id.setter
    def id(self, value):
        if value is not None:
            self._device["id"] = value.strip()

    @property
    def hardware(self):
        return self.HARDWARE

    @property
    def name(self):
        return self._device["name"]

    @name.setter
    def name(self, value):
        if "" != value.strip():
            self._device["name"] = value.strip()

    @property
    def address(self):
        return self._device["address"]

    @property
    def _address(self):
        address = [part.strip() for part in self.address.split(",") if "" != part.strip()]
        return address

    @address.setter
    def address(self, value):
        value = terrariumUtils.clean_address(value)
        if value is not None and "" != value:
            self._device["address"] = value

    # Readonly property
    @property
    def device(self):
        return self._device["device"]

    # Readonly property
    @property
    def sensor_type(self):
        return self._device["type"]

    # Readonly property
    @property
    def type(self):
        return self._device["type"]

    @property
    def value(self):
        return self._device["value"]

    @property
    def last_update(self):
        return self._device["last_update"]

    @property
    def erratic(self):
        return self._device["erratic_errors"]

    @erratic.setter
    def erratic(self, value):
        self._device["erratic_errors"] = value

    def get_hardware_state(self):
        pass

    @retry(terrariumSensorLoadingException, tries=3, delay=0.5, max_delay=2, logger=logger)
    def load_hardware(self, reload=False):
        # Get hardware cache key based on the combination of hardware and address
        hardware_cache_key = md5(f"HW-{self.HARDWARE}-{self.address}".encode()).hexdigest()
        # Load hardware device from cache
        hardware = self._sensor_cache.get_data(hardware_cache_key)
        if reload or hardware is None:
            # Could not find valid hardware cache. So create a new hardware device
            try:
                hardware = func_timeout(self._UPDATE_TIME_OUT, self._load_hardware)
                if hardware is None:
                    # Raise error that hard is not loaded with an unknown message :(
                    raise terrariumSensorLoadingException(f"Unable to load sensor {self}: Did not return a device.")

                # Store the hardware in the cache for unlimited of time
                self._sensor_cache.set_data(hardware_cache_key, hardware, -1)

            except FunctionTimedOut:
                # What ever fails... does not matter, as the data is still None and will raise a terrariumSensorUpdateException and trigger the retry
                raise terrariumSensorLoadingException(
                    f"Unable to load sensor {self}: timed out ({self._UPDATE_TIME_OUT} seconds) during loading."
                )

            except Exception as ex:
                raise terrariumSensorLoadingException(f"Unable to load sensor {self}: {ex}")

        self._device["device"] = hardware
        # Check for power management features and enable it if set
        if self._device["power_mngt"] is not None:
            self._device["power_mngt"] = LED(terrariumUtils.to_BCM_port_number(self._device["power_mngt"]))

    # When we get Runtime errors retry up to 3 times
    @retry(terrariumSensorUpdateException, tries=3, delay=0.5, max_delay=2, logger=logger)
    def get_data(self):
        error_message = f"Error getting new data from sensor {self}"
        data = None

        try:
            self.__power_management(True)
            data = func_timeout(self._UPDATE_TIME_OUT, self._get_data)

        except FunctionTimedOut:
            raise terrariumSensorUpdateException(f"{error_message}: Timed out after {self._UPDATE_TIME_OUT} seconds")
        except Exception as ex:
            raise terrariumSensorUpdateException(f"{error_message}: {ex}")
        finally:
            self.__power_management(False)

        if data is None:
            raise terrariumSensorUpdateException(f"{error_message}: no data")

        return data

    def update(self, force=False):
        if self._device["device"] is None:
            raise terrariumSensorLoadingException(f"Sensor {self} is not loaded! Can not update!")

        starttime = time()
        data = self._sensor_cache.get_data(self._sensor_cache_key)

        if (data is None or force) and self._sensor_cache.set_running(self._sensor_cache_key):
            logger.debug(f"Start getting new data from  sensor {self}")
            try:
                data = self.get_data()
                self._sensor_cache.set_data(self._sensor_cache_key, data, self._CACHE_TIMEOUT)
            except Exception as ex:
                logger.error(f"Error updating sensor {self}. Check your hardware! {ex}")

            self._sensor_cache.clear_running(self._sensor_cache_key)

        current = None if data is None or self.sensor_type not in data else data[self.sensor_type]

        if current is None:
            self._sensor_cache.clear_data(self._sensor_cache_key)

        else:
            self._device["last_update"] = int(starttime)
            self._device["value"] = current
            return current

    def stop(self):
        pass

    def __repr__(self):
        return f"{self.NAME} {self.type} named '{self.name}' at address '{self.address}'"

    # Auto discovery of known and connected sensors
    @staticmethod
    def scan_sensors(unit_value_callback=None, trigger_callback=None, **kwargs):
        for sensor_device in terrariumSensor.available_hardware.values():
            try:
                for sensor in sensor_device._scan_sensors(unit_value_callback, trigger_callback, **kwargs):
                    yield sensor
            except AttributeError:
                # Scanning not supported, just ignore
                pass


class terrariumAnalogSensor(terrariumSensor):
    HARDWARE = None
    TYPES = []
    NAME = None

    __AMOUNT_OF_MEASUREMENTS = 5

    def _load_hardware(self):
        address = self._address
        # Load the analog converter here
        device = MCP3008(
            channel=int(address[0]), device=0 if len(address) == 1 or int(address[1]) < 0 else int(address[1])
        )
        return device

    def _get_data(self):
        # This will return the measured voltage of the analog device.
        values = []
        for _ in range(self.__AMOUNT_OF_MEASUREMENTS):
            value = self.device.value
            if terrariumUtils.is_float(value):
                values.append(float(value))
            sleep(0.2)

        # sort values from low to high
        values.sort()
        # Calculate average. Exclude the min and max value.
        return statistics.mean(values[1:-1])


class terrariumI2CSensor(terrariumSensor):
    @property
    def _address(self):
        return terrariumUtils.getI2CAddress(self.address)

    def _open_hardware(self):
        return smbus2.SMBus(self._address[1])

    def _load_hardware(self):
        device = (self._address[0], self._open_hardware())
        return device


class terrariumI2CSensorMixin:
    # control constants
    SOFTRESET = 0xFE
    SOFTRESET_TIMEOUT = 0.1

    TEMPERATURE_TRIGGER_NO_HOLD = 0xF3
    TEMPERATURE_WAIT_TIME = 0.1

    HUMIDITY_TRIGGER_NO_HOLD = 0xF5
    HUMIDITY_WAIT_TIME = 0.1

    def __soft_reset(self, i2c_bus):
        i2c_bus.write_byte(self.device[0], self.SOFTRESET)
        sleep(self.SOFTRESET_TIMEOUT)

    def __get_data(self, i2c_bus, trigger, timeout):
        data1 = data2 = None
        # Send request for data
        i2c_bus.write_byte(self.device[0], trigger)
        sleep(timeout)

        data1 = i2c_bus.read_byte(self.device[0])
        try:
            data2 = i2c_bus.read_byte(self.device[0])
        except Exception:
            data2 = data1

        return (data1, data2)

    def _get_data(self):
        data = {}
        with self._open_hardware() as i2c_bus:
            # Datasheet recommend do Soft Reset before measurement:
            self.__soft_reset(i2c_bus)
            if "temperature" in self.TYPES:
                bytedata = self.__get_data(i2c_bus, self.TEMPERATURE_TRIGGER_NO_HOLD, self.TEMPERATURE_WAIT_TIME)
                data["temperature"] = ((bytedata[0] * 256.0 + bytedata[1]) * 175.72 / 65536.0) - 46.85
            if "humidity" in self.TYPES:
                bytedata = self.__get_data(i2c_bus, self.HUMIDITY_TRIGGER_NO_HOLD, self.HUMIDITY_WAIT_TIME)
                data["humidity"] = ((bytedata[0] * 256.0 + bytedata[1]) * 125.0 / 65536.0) - 6.0

        return data


# TCA9548A I2C switch driver, Texas instruments
# 8 bidirectional translating switches
# I2C SMBus protocol
# Manual: tca9548.pdf
# Source: https://github.com/IRNAS/tca9548a-python/blob/master/tca9548a.py
# Added option for different I2C bus


class TCA9548A(object):
    def __init__(self, address, bus=1):
        """Init smbus channel and tca driver on specified address."""
        try:
            self.PORTS_COUNT = 8  # number of switches

            self.i2c_bus = smbus2.SMBus(bus)
            self.i2c_address = address
            if self.get_control_register() is None:
                raise ValueError
        except ValueError:
            logger.error("No device found on specified address!")
            self.i2c_bus = None
        except Exception:
            logger.error("Bus on channel {} is not available.".format(bus))
            logger.info("Available busses are listed as /dev/i2c*")
            self.i2c_bus = None

    def get_control_register(self):
        """Read value (length: 1 byte) from control register."""
        try:
            value = self.i2c_bus.read_byte(self.i2c_address)
            return value
        except Exception:
            return None

    def get_channel(self, ch_num):
        """Get channel state (specified with ch_num), return 0=disabled or 1=enabled."""
        if ch_num < 0 or ch_num > self.PORTS_COUNT - 1:
            return None
        register = self.get_control_register()
        if register is None:
            return None
        value = (register >> ch_num) & 1
        return value

    def set_control_register(self, value):
        """Write value (length: 1 byte) to control register."""
        try:
            if value < 0 or value > 255:
                return False
            self.i2c_bus.write_byte(self.i2c_address, value)
            return True
        except Exception:
            return False

    def set_channel(self, ch_num, state):
        """Change state (0=disable, 1=enable) of a channel specified in ch_num."""
        if ch_num < 0 or ch_num > self.PORTS_COUNT - 1:
            return False
        if state != 0 and state != 1:
            return False
        current_value = self.get_control_register()
        if current_value is None:
            return False
        if state:
            new_value = current_value | 1 << ch_num
        else:
            new_value = current_value & (255 - (1 << ch_num))
        return_value = self.set_control_register(new_value)
        return return_value

    def __del__(self):
        """Driver destructor."""
        self.i2c_bus = None


class terrariumBluetoothSensor(terrariumSensor):
    __MIN_DB = -90
    __SCAN_TIME = 3

    @property
    def _address(self):
        address = super()._address
        if len(address) == 1:
            address.append(0)
        elif len(address) == 2:
            address[1] = (
                int(address[1])
                if terrariumUtils.is_float(address[1]) and terrariumUtils.is_float(address[1]) > 0
                else 0
            )

        return address

    @staticmethod
    def _scan_bt_sensors(sensor_class, ids=[], unit_value_callback=None, trigger_callback=None):
        # Due to multiple bluetooth dongles, we are looping 10 times to see which devices can scan. Exit after first success
        ok = True
        for counter in range(10):
            try:
                devices = Scanner(counter).scan(terrariumBluetoothSensor.__SCAN_TIME)
                for device in devices:
                    if (
                        device.rssi > terrariumBluetoothSensor.__MIN_DB
                        and device.getValueText(9) is not None
                        and device.getValueText(9).lower() in ids
                    ):
                        for sensor_type in sensor_class.TYPES:
                            yield terrariumSensor(
                                None,
                                sensor_class.HARDWARE,
                                sensor_type,
                                device.addr + ("" if counter == 0 else f",{counter}"),
                                f"{sensor_class.NAME} measuring {sensor_type}",
                                unit_value_callback=unit_value_callback,
                                trigger_callback=trigger_callback,
                            )

                # we found devices, so this device is ok! Stop trying more bluetooth devices
                break

            except Exception as ex:
                logger.warning(f"Error during scanning {sensor_class.NAME}: {ex}")
                ok = False

        if not ok:
            logger.warning(
                "Bluetooth scanning is not enabled for normal users or there are zero Bluetooth LE devices available.... bluetooth is disabled!"
            )

        return []
