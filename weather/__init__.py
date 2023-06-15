# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from abc import ABCMeta, abstractmethod
from pathlib import Path
import inspect
from importlib import import_module
import sys
import copy
import time

# pip install retry
from retry import retry

from datetime import datetime, timedelta
import re

from terrariumUtils import terrariumUtils


class terrariumWeatherException(TypeError):
    """There is a problem with loading a hardware switch. Invalid power switch action."""

    def __init__(self, message, *args):
        self.message = message
        super().__init__(message, *args)


# https://www.bnmetrics.com/blog/factory-pattern-in-python3-simple-version
class terrariumWeatherAbstract(metaclass=ABCMeta):
    HARDWARE = None
    NAME = None
    VALID_SOURCE = None
    INFO_SOURCE = None

    # Weather data expects temperature in celsius degrees and windspeed in meters per second
    __UPDATE_TIMEOUT = 15 * 60  # 15 minutes. The source updates every 10 minutes

    def __init__(self, address, unit_values, language):
        self._device = {
            "id": None,
            "address": None,
            "unit_values": unit_values,
            "language": language,
            "last_update": None,
        }

        self._data = {"days": [], "forecast": [], "history": []}
        self.address = address

    @retry(tries=3, delay=0.5, max_delay=2)
    def update(self):
        if (
            self._device["last_update"] is None
            or (datetime.now() - self._device["last_update"]).total_seconds() > self.__UPDATE_TIMEOUT
        ):
            start = time.time()
            logger.debug(f"Loading online weather data from source: {self.address}")

            if self._load_data():
                # Convert values to the right unit values
                for day in self._data["days"]:
                    day["temp"] = terrariumUtils.convert_to_value(
                        day["temp"], self._device["unit_values"]["temperature"]
                    )
                    day["wind"]["speed"] = terrariumUtils.convert_to_value(
                        day["wind"]["speed"], self._device["unit_values"]["windspeed"]
                    )

                # TODO: Change to list!!!!
                for forecast in self._data["forecast"]:
                    forecast["temperature"] = terrariumUtils.convert_to_value(
                        forecast["temperature"], self._device["unit_values"]["temperature"]
                    )

                for history in self._data["history"]:
                    history["temperature"] = terrariumUtils.convert_to_value(
                        history["temperature"], self._device["unit_values"]["temperature"]
                    )

                self._device["last_update"] = datetime.now()
                logger.info(
                    terrariumUtils.clean_log_line(f"Loaded new weather data in {time.time()-start:.3f} seconds.")
                )
            else:
                logger.error(
                    terrariumUtils.clean_log_line(
                        f"Error loading online weather data! Please check your source address: {self.address}."
                    )
                )

    def __get_today_data(self, offset=0):
        now = datetime.now()
        for forecast in self._data["days"]:
            if now.strftime("%d") == datetime.utcfromtimestamp(forecast["rise"] - offset).strftime("%d"):
                return forecast

        # There is no today data, as we load data with a timezone that is in the future
        today = copy.deepcopy(self._data["days"][0])
        today["rise"] -= 24 * 60 * 60
        today["set"] -= 24 * 60 * 60
        today["timestamp"] -= 24 * 60 * 60
        return today

    @property
    def today(self):
        return self.__get_today_data()

    @property
    def tomorrow(self):
        return self.__get_today_data(24 * 3600)

    @property
    def address(self):
        return self._device["address"]

    @property
    def _address(self):
        return [part.strip() for part in self.address.split(",")]

    @address.setter
    def address(self, value):
        if value is not None and "" != str(value).strip(", "):
            reload = self.address != str(value).strip(", ")
            self._device["address"] = str(value).strip(", ")
            if reload:
                logger.debug(f"Reloading weather data due to changing weather source to: {self.address}")
                self._device["last_update"] = None
                self.update()

    @property
    def name(self):
        return self._device["name"]

    @name.setter
    def name(self, value):
        if value is not None and "" != str(value).strip():
            self._device["name"] = str(value).strip()

    @property
    def sunrise(self):
        data = self.today
        if data is not None:
            return datetime.utcfromtimestamp(data["rise"])

        return datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    @property
    def sunset(self):
        data = self.today
        if data is not None:
            return datetime.utcfromtimestamp(data["set"])

        return datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)

    @property
    def next_sunrise(self):
        data = self.tomorrow
        if data is not None:
            return datetime.utcfromtimestamp(data["rise"])

        return datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    @property
    def next_sunset(self):
        data = self.tomorrow
        if data is not None:
            return datetime.utcfromtimestamp(data["set"])

        return datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)

    @property
    def is_day(self):
        now = datetime.now()
        if now < self.sunrise:
            now += timedelta(hours=24)

        return self.sunrise < now < self.sunset

    @property
    def current_temperature(self):
        return self._data["days"][0]["temperature"]

    @property
    def current_humidity(self):
        return self._data["days"][0]["humidity"]

    @property
    def short_forecast(self):
        return copy.deepcopy(self._data["days"])

    @property
    def forecast(self):
        return copy.deepcopy(self._data["forecast"])

    @property
    def history(self):
        return copy.deepcopy(self._data["history"])

    @property
    def location(self):
        return {"city": self._data["city"], "country": self._data["country"], "geo": self._data["geo"]}

    @property
    def credits(self):
        return {"text": self._data["credits"], "url": self._data["url"]}

    @abstractmethod
    def _load_data(self):
        pass


# Factory class
class terrariumWeather(object):
    SOURCES = {}

    # Start dynamically loading switches (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
    for file in sorted(Path(__file__).parent.glob("*_weather.py")):
        imported_module = import_module("." + file.stem, package="{}".format(__name__))

        for i in dir(imported_module):
            attribute = getattr(imported_module, i)

            if (
                inspect.isclass(attribute)
                and attribute != terrariumWeatherAbstract
                and issubclass(attribute, terrariumWeatherAbstract)
            ):
                setattr(sys.modules[__name__], file.stem, attribute)
                SOURCES[attribute.HARDWARE] = attribute

    # Return polymorph weather....
    def __new__(self, address, unit_values, language):
        for weather_source in terrariumWeather.SOURCES:
            if re.search(terrariumWeather.SOURCES[weather_source].VALID_SOURCE, address, re.IGNORECASE):
                return terrariumWeather.SOURCES[weather_source](address, unit_values, language)

        raise terrariumWeatherException("Weather url '{}' is not valid! Please check your source".format(address))

    # Return a list with type and names of supported switches
    @staticmethod
    def get_available_types():
        data = []
        for hardware_type, weather_source in terrariumWeather.SOURCES.items():
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
