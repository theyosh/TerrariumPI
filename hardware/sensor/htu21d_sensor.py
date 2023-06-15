# -*- coding: utf-8 -*-
from . import terrariumI2CSensor, terrariumI2CSensorMixin


class terrariumHTU21DSensor(terrariumI2CSensor, terrariumI2CSensorMixin):
    HARDWARE = "htu21d"
    TYPES = ["temperature", "humidity"]
    NAME = "HTU21D sensor"

    # Datasheet - https://datasheet.octopart.com/HPP845E131R5-TE-Connectivity-datasheet-15137552.pdf
    TEMPERATURE_WAIT_TIME = 0.059  # (datasheet: typ=44, max=58 in ms)
    HUMIDITY_WAIT_TIME = 0.019  # (datasheet: typ=14, max=18 in ms)
    SOFTRESET_TIMEOUT = 0.016  # (datasheet: typ=??, max=15 in ms)
