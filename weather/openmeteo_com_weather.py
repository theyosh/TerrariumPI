# -*- coding: utf-8 -*-
# Created by GamingLPyt: (https://github.com/theyosh/TerrariumPI/issues/1043) Thanks!!!
# Rewritten by TheYOSH
import terrariumLogging

logger = terrariumLogging.logging.getLogger("Open-Meteo")

import re
from datetime import datetime, timedelta
from . import terrariumWeather
from terrariumUtils import terrariumUtils


class terrariumOpenmeteo(terrariumWeather):
    HARDWARE = "Open-Meteo.com"
    NAME = "Open-Meteo weather data"

    # Example URL format expected by the TerrariumPI GUI:
    #
    # https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41
    #
    # Basic regex validation for user-entered URLs
    VALID_SOURCE = r"^https?:\/\/api\.open-meteo\.com\/v1\/forecast\?latitude=(?P<lat>-?\d+(\.\d+)?)&longitude=(?P<long>-?\d+(\.\d+)?)(?:&.*)?$"

    # Shown in GUI as example
    INFO_SOURCE = "https://api.open-meteo.com/v1/forecast?latitude=[LAT]&longitude=[LON]"

    @staticmethod
    def _weathercode_to_description(code):
        """
        Simple human-readable translation for Open-Meteo weather codes.
        """
        mapping = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Light rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Light snowfall",
            73: "Moderate snowfall",
            75: "Heavy snowfall",
            80: "Light rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with light hail",
            99: "Thunderstorm with heavy hail",
        }
        return mapping.get(code, "Unknown")

    @staticmethod
    def _weathercode_to_icon(code):
        """
        Map Open-Meteo weather codes to OWM-style icons used by TerrariumPI.
        We always return the *day* variant (..d), TerrariumPI is fine with that.
        """
        if code is None:
            return ""

        if code == 0:
            return "01d"  # clear
        if code == 1:
            return "02d"  # mainly clear
        if code == 2:
            return "03d"  # partly cloudy
        if code == 3:
            return "04d"  # overcast

        if code in (45, 48):
            return "50d"  # fog

        if code in (51, 53, 55):
            return "09d"  # drizzle

        if code in (61, 63, 65):
            return "10d"  # rain

        if code in (71, 73, 75):
            return "13d"  # snow

        if code in (80, 81, 82):
            return "09d"  # showers

        if code == 95:
            return "11d"  # thunderstorm

        if code in (96, 99):
            return "11d"  # thunderstorm + hail

        return ""

    def _get_data(self):
        coordinates = re.search(terrariumOpenmeteo.VALID_SOURCE, self.address)
        self._device["geo"] = {"lat": float(coordinates.group("lat")), "long": float(coordinates.group("long"))}
        self._device["url"] = "https://open-meteo.com/"
        self._device["credits"] = "Open-Meteo.com weather data"

        return_data = {"forecast": {}, "history": {}}

        # The dates and times are in the timezone of the GEO location. And that is what we need!
        # Temperatures are in C, wind speed is in km/h

        # Get all hourly and daily data
        json_data = terrariumUtils.get_remote_data(
            f"{self.address}&daily=sunrise,sunset,weather_code,wind_direction_10m_dominant,relative_humidity_2m_mean,temperature_2m_mean,wind_speed_10m_mean&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,weather_code&timezone=auto&forecast_days=14&wind_speed_unit=ms&language={self._device['language']}"
        )

        # Hourly overrules daily. The data will be sorted later on
        return_data["forecast"] = {
            **self.__process_daily_data(json_data.get("daily", [])),
            **self.__process_hourly_data(json_data.get("hourly", [])),
        }

        # Get history data
        now = datetime.now()
        start_date = (now - timedelta(days=2)).strftime("%Y-%m-%d")
        end_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        json_data = terrariumUtils.get_remote_data(
            f"{self.address.replace('api.','archive-api.').replace('forecast','archive')}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&timezone=auto&wind_speed_unit=ms&language={self._device['language']}"
        )

        return_data["history"] = self.__process_history_data(json_data.get("hourly", []))

        return return_data

    def __process_hourly_data(self, data):
        hourly_data = {}
        for counter, time in enumerate(data["time"]):
            time = datetime.fromisoformat(time).replace(microsecond=0)

            hourly_data[time.isoformat()] = {
                "timestamp": time,
                "temperature": data["temperature_2m"][counter],
                "humidity": data["relative_humidity_2m"][counter],
                "wind": {
                    "speed": data["wind_speed_10m"][counter],
                    "direction": data["wind_direction_10m"][counter],
                },
                "weather": {
                    "description": terrariumOpenmeteo._weathercode_to_description(data["weather_code"][counter]),
                    "icon": terrariumOpenmeteo._weathercode_to_icon(data["weather_code"][counter]),
                },
            }

        return hourly_data

    def __process_daily_data(self, data):
        daily_data = {}
        for counter, time in enumerate(data["time"]):
            time = datetime.fromisoformat(time).replace(microsecond=0)

            daily_data[time.isoformat()] = {
                "timestamp": time,
                "temperature": data["temperature_2m_mean"][counter],
                "humidity": data["relative_humidity_2m_mean"][counter],
                "sun": {
                    "rise": datetime.fromisoformat(data["sunrise"][counter]),
                    "set": datetime.fromisoformat(data["sunset"][counter]),
                },
                "wind": {
                    "speed": data["wind_speed_10m_mean"][counter],
                    "direction": data["wind_direction_10m_dominant"][counter],
                },
                "weather": {
                    "description": terrariumOpenmeteo._weathercode_to_description(data["weather_code"][counter]),
                    "icon": terrariumOpenmeteo._weathercode_to_icon(data["weather_code"][counter]),
                },
            }

        return daily_data

    def __process_history_data(self, data):
        history_data = {}
        for counter, time in enumerate(data["time"]):
            time = datetime.fromisoformat(time).replace(microsecond=0)

            history_data[time.isoformat()] = {
                "timestamp": time,
                "temperature": data["temperature_2m"][counter],
                "humidity": data["relative_humidity_2m"][counter],
                "wind": {
                    "speed": data["wind_speed_10m"][counter],
                    "direction": data["wind_direction_10m"][counter],
                },
                "weather": {
                    "description": terrariumOpenmeteo._weathercode_to_description(data["weather_code"][counter]),
                    "icon": terrariumOpenmeteo._weathercode_to_icon(data["weather_code"][counter]),
                },
            }

        return history_data
