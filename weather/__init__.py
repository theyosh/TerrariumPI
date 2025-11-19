"""
Weather package to use in TerrariumPI

Raises:
    terrariumWeatherException: There is a general problem with a weather source

Returns:
    terrariumWeather: A working weather object
"""

# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger("terrariumWeather")

import re
import time
from datetime import datetime, timedelta
from hashlib import md5

# pip install retry
from retry import retry

from terrariumUtils import terrariumUtils, classproperty


class terrariumWeatherException(Exception):
    pass


class terrariumWeatherLoadingException(terrariumWeatherException):
    pass


class terrariumWeatherUpdateException(terrariumWeatherException):
    pass


# Weather data expects temperature in celsius degrees and wind speed in meters per second
# Factory class
class terrariumWeather(object):
    HARDWARE = None
    NAME = None
    VALID_SOURCE = None
    INFO_SOURCE = None

    __UPDATE_TIMEOUT = 15 * 60  # 15 minutes. The source updates every 10 minutes

    @classproperty
    def available_hardware(__cls__):
        return terrariumUtils.loadHardwareDrivers(__cls__, __name__, __file__, "*_weather.py")

    # Return a list with type and names of supported weather partners
    @staticmethod
    def get_available_types():
        data = []
        for hardware_type, weather_source in terrariumWeather.available_hardware.items():
            if weather_source.NAME is not None:
                data.append(
                    {
                        "hardware": hardware_type,
                        "name": weather_source.NAME,
                        "url": weather_source.INFO_SOURCE,
                        "validator": weather_source.VALID_SOURCE,
                    }
                )
        return data

    # Return polymorph weather....
    def __new__(cls, address, unit_values, language):
        for weather_source in terrariumWeather.available_hardware:
            if re.search(terrariumWeather.available_hardware[weather_source].VALID_SOURCE, address, re.IGNORECASE):
                return super(terrariumWeather, cls).__new__(terrariumWeather.available_hardware[weather_source])

        raise terrariumWeatherException(f"Weather url '{address}' is not valid! Please check your source")

    def __init__(self, address, unit_values, language):
        self._device = {
            "address": None,
            "unit_values": unit_values,
            "language": language,
            "last_update": None,
            "city": None,
            "country": None,
            "geo": {
                "lat": None,
                "long": None,
            },
            "hours": {},
            "forecast": {},
            "history": {},
        }

        # Trigger loading
        self.address = address

    def __repr__(self):
        """
        Returns readable weather name

        Returns:
            string: Weather type and name with address
        """
        return f"{self.NAME} using url '{self.address}'"

    def _get_data(self):
        pass

    def __convert_data(self):
        # Sort the data on timestamp keys
        self._device["hours"] = dict(sorted(self._device["hours"].items()))
        self._device["forecast"] = dict(sorted(self._device["forecast"].items()))
        self._device["history"] = dict(sorted(self._device["history"].items()))

        # Convert values to the right unit values
        # We expect values in C and m/s
        for day in self._device["hours"].keys():
            self._device["hours"][day]["temperature"] = terrariumUtils.convert_to_value(
                self._device["hours"][day]["temperature"], self._device["unit_values"]["temperature"]
            )
            self._device["hours"][day]["wind"]["speed"] = terrariumUtils.convert_to_value(
                self._device["hours"][day]["wind"]["speed"], self._device["unit_values"]["windspeed"]
            )

        for day in self._device["forecast"].keys():
            self._device["forecast"][day]["temperature"] = terrariumUtils.convert_to_value(
                self._device["forecast"][day]["temperature"], self._device["unit_values"]["temperature"]
            )

        for day in self._device["history"].keys():
            self._device["history"][day]["temperature"] = terrariumUtils.convert_to_value(
                self._device["history"][day]["temperature"], self._device["unit_values"]["temperature"]
            )

    def __get_current(self):
        today = datetime.now().replace(minute=0, second=0, microsecond=0)
        for _ in range(24):
            today_index = today.isoformat()
            today += timedelta(hours=1)
            if today_index in self._device["hours"]:
                return self._device["hours"][today_index]

    def __get_current_sunrise_sunset(self, next=False):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for _ in range(48):
            today_index = today.isoformat()
            today += timedelta(hours=1)
            if today_index in self._device["forecast"] and "sun" in self._device["forecast"][today_index]:
                shift_days = int((self._device["forecast"][today_index]["sun"]["rise"] - datetime.now()).days)
                if not next:
                    return {
                        "sunrise": self._device["forecast"][today_index]["sun"]["rise"] - timedelta(days=shift_days),
                        "sunset": self._device["forecast"][today_index]["sun"]["set"] - timedelta(days=shift_days),
                    }

                next = False

        return None

    @property
    def id(self):
        if self._device["id"] is None and self.address is not None:
            self._device["id"] = md5(f"{self.HARDWARE}{self.address}".encode()).hexdigest()

        return self._device["id"]

    @property
    def address(self):
        return self._device["address"]

    @address.setter
    def address(self, value):
        value = terrariumUtils.clean_address(value)
        if value not in [None, "", self.address]:
            logger.info(
                f"{'Loading' if self.address in [None, ''] else 'Reloading'} weather data due to changing weather source to: {value}"
            )
            self._device["address"] = value
            self._device["last_update"] = None
            self.update()

    @property
    def name(self):
        return self.NAME

    @property
    def location(self):
        return {"city": self._device["city"], "country": self._device["country"], "geo": self._device["geo"]}

    @property
    def credits(self):
        return {"text": self._device["credits"], "url": self._device["url"]}

    @retry(tries=3, delay=0.5, max_delay=2, logger=logger)
    def update(self):
        if (
            self._device["last_update"] is None
            or (datetime.now() - self._device["last_update"]).total_seconds() > self.__UPDATE_TIMEOUT
        ):
            start = time.time()
            logger.debug(f"Loading online weather data from source: {self.address}")

            if self._get_data():
                self.__convert_data()
                self._device["last_update"] = datetime.now()
                logger.info(f"Loaded {self} in: {time.time() - start:.2f} seconds")

            else:
                logger.error(f"Error loading online weather data! Please check your source address: {self.address}.")

    @property
    def sunrise(self):
        data = self.__get_current_sunrise_sunset()
        if data:
            return data["sunrise"]

        return datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    @property
    def sunset(self):
        data = self.__get_current_sunrise_sunset()
        if data:
            return data["sunset"]

        return datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)

    @property
    def next_sunrise(self):
        data = self.__get_current_sunrise_sunset(True)
        if data:
            return data["sunrise"]

        return self.sunrise + timedelta(days=1)

    @property
    def next_sunset(self):
        data = self.__get_current_sunrise_sunset(True)
        if data:
            return data["sunset"]

        return self.sunset + timedelta(days=1)

    @property
    def is_day(self):
        return self.sunrise < datetime.now() < self.sunset

    @property
    def current(self):
        return self.__get_current()

    @property
    def short_forecast(self, days=6):
        days = max(min(days, 14), 1)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for _ in range(days):
            today += timedelta(days=1)
            today_index = today.isoformat()
            if today_index in self._device["forecast"]:
                yield self._device["forecast"][today_index]

    @property
    def forecast(self):
        return list(self._device["forecast"].values())

    @property
    def history(self):
        return list(self._device["history"].values())
