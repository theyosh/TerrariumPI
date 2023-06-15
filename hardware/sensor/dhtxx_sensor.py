# -*- coding: utf-8 -*-
from . import terrariumSensor
from terrariumUtils import terrariumUtils

# apt install pigpiod
# pip install pigpio-dht
from pigpio_dht import DHT11, DHT22


class terrariumDHTXXSensor(terrariumSensor):
    HARDWARE = None
    TYPES = ["temperature", "humidity"]
    NAME = None

    def _load_hardware(self):
        device = None
        address = self._address
        if len(address) >= 2 and terrariumUtils.is_float(address[1]):
            # Set / enable power management
            self._device["power_mngt"] = terrariumUtils.to_BCM_port_number(address[1])

        if self.HARDWARE == terrariumDHT11Sensor.HARDWARE:
            device = DHT11(terrariumUtils.to_BCM_port_number(address[0]))
        elif self.HARDWARE in [terrariumDHT22Sensor.HARDWARE, terrariumAM2302Sensor.HARDWARE]:
            device = DHT22(terrariumUtils.to_BCM_port_number(address[0]))

        return device

    def _get_data(self):
        result = self.device.read()
        if not terrariumUtils.is_true(result["valid"]):
            return None

        data = {}
        data["temperature"] = result["temp_c"]
        data["humidity"] = result["humidity"]
        return data


class terrariumDHT11Sensor(terrariumDHTXXSensor):
    HARDWARE = "dht11"
    NAME = "DHT11 sensor"


class terrariumDHT22Sensor(terrariumDHTXXSensor):
    HARDWARE = "dht22"
    NAME = "DHT22 sensor"


class terrariumAM2302Sensor(terrariumDHTXXSensor):
    HARDWARE = "am2302"
    NAME = "AM2302 sensor"
