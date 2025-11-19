# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger("OpenWeatherMap")

import re
from datetime import datetime, timedelta
from . import terrariumWeather
from terrariumUtils import terrariumUtils


class terrariumOpenweathermap(terrariumWeather):
    HARDWARE = "Openweathermap.org"
    NAME = "OpenWeatherMap weather data"
    VALID_SOURCE = r"^https?:\/\/api\.openweathermap\.org\/data\/2\.5\/weather\?(q=(?P<city>[^,&]+),(?P<country>[^,&]{2,3})|id=(?P<id>\d+))&appid=(?P<appid>[a-z0-9]{32})$"
    INFO_SOURCE = "https://api.openweathermap.org/data/2.5/weather?q=[CITY],[COUNTRY_2CHAR]&appid=[YOUR_API_KEY]"

    def _get_data(self):
        if not hasattr(self, '__history_day'):
            self.__history_day = None

        if not hasattr(self, '__one_call_version'):
            self.__one_call_version = None

        self.__appid = None

        loaded = True
        loaded = loaded and self.__load_general_data()
        loaded = loaded and self.__load_forecast_data()
        loaded = loaded and self.__load_history_data()

        return loaded

    def __load_general_data(self):
        address = self.address + "&units=metric&lang=" + self._device["language"][0:2]
        data = terrariumUtils.get_remote_data(address)
        if data:
            self._device["city"] = data["name"]
            self._device["country"] = data["sys"]["country"]
            self._device["geo"] = {"lat": float(data["coord"]["lat"]), "long": float(data["coord"]["lon"])}
            self._device["url"] = "https://openweathermap.org/city/{}".format(data["id"])
            self._device["credits"] = "OpenWeatherMap weather data"

            # The data from OpenWeatherMap is in GMT. But we want the data in the timezone of the requested location
            self.__timezone_difference = int(data["timezone"]) - datetime.now().astimezone().utcoffset().seconds
            appid = re.search(terrariumOpenweathermap.VALID_SOURCE, self.address)
            self.__appid = appid.group("appid")

            return True

        return False

    def __load_minimal_forecast_data(self):
        url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric&lang={}".format(
            self._device["geo"]["lat"], self._device["geo"]["long"], self.__appid, self._device["language"][0:2]
        )
        data = terrariumUtils.get_remote_data(url)

        if not data:
            logger.error("Failed loading minimal weather forecast data. Make sure your source address is correct!")
            return False

        sunrise = datetime.fromtimestamp(int(data["city"]["sunrise"] + self.__timezone_difference))
        sunset = datetime.fromtimestamp(int(data["city"]["sunset"] + self.__timezone_difference))

        hourly_data = {}
        for forecast in data["list"]:
            time = datetime.fromtimestamp(forecast["dt"] + self.__timezone_difference).replace(microsecond=0)

            hourly_data[time.isoformat()] = {
                "timestamp": time,
                "temperature": float(forecast["main"]["temp"]),
                "humidity": float(forecast["main"]["humidity"]),
                "sun": {
                    "rise": sunrise,
                    "set": sunset,
                },
                "wind": {
                    "speed": float(forecast["wind"]["speed"]),
                    "direction": float(forecast["wind"]["deg"]),
                },
                "weather": {
                    "description": forecast["weather"][0].get("description", ""),
                    "icon": forecast["weather"][0].get("icon", ""),
                },
            }

        self._device["hours"] = hourly_data

        return True

    def __load_forecast_data_one_call(self):
        data = None
        if self.__one_call_version is None or self.__one_call_version == "3.0":
            data = terrariumUtils.get_remote_data(
                "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units=metric&exclude=minutely&appid={}&lang={}".format(
                    self._device["geo"]["lat"], self._device["geo"]["long"], self.__appid, self._device["language"][0:2]
                )
            )

        if (self.__one_call_version is None and not data) or self.__one_call_version == "2.5":
            data = terrariumUtils.get_remote_data(
                "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=minutely&appid={}&lang={}".format(
                    self._device["geo"]["lat"], self._device["geo"]["long"], self.__appid, self._device["language"][0:2]
                )
            )
            if data:
                self.__one_call_version = "2.5"

        elif self.__one_call_version is None:
            self.__one_call_version = "3.0"

        if not data:
            logger.error("Failed loaded forecast data!")
            return False

        sunrise = datetime.fromtimestamp(int(data["current"]["sunrise"] + self.__timezone_difference))
        sunset = datetime.fromtimestamp(int(data["current"]["sunset"] + self.__timezone_difference))

        hourly_data = {}
        for forecast in data["hourly"]:
            time = datetime.fromtimestamp(forecast["dt"] + self.__timezone_difference).replace(minute=0, microsecond=0)

            hourly_data[time.isoformat()] = {
                "timestamp": time,
                "temperature": float(forecast["temp"]),
                "humidity": float(forecast["humidity"]),
                "sun": {
                    "rise": sunrise,
                    "set": sunset,
                },
                "wind": {
                    "speed": float(forecast["wind_speed"]),
                    "direction": float(forecast["wind_deg"]),
                },
                "weather": {
                    "description": forecast["weather"][0].get("description", ""),
                    "icon": forecast["weather"][0].get("icon", ""),
                },
            }

        self._device["hours"] = hourly_data

        day_periods = {"night": 0 * 60 * 60, "morn": 6 * 60 * 60, "day": 12 * 60 * 60, "eve": 18 * 60 * 60}
        daily_data = {}
        for daily in data["daily"]:
            day_stamp = datetime.fromtimestamp(daily["dt"] + self.__timezone_difference).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            sunrise = datetime.fromtimestamp(int(daily["sunrise"] + self.__timezone_difference))
            sunset = datetime.fromtimestamp(int(daily["sunset"] + self.__timezone_difference))

            for period in day_periods:
                time = day_stamp + timedelta(seconds=day_periods[period])

                daily_data[time.isoformat()] = {
                    "timestamp": time,
                    "temperature": float(daily["temp"][period]),
                    "humidity": float(daily["humidity"]),
                    "sun": {
                        "rise": sunrise,
                        "set": sunset,
                    },
                    "wind": {
                        "speed": float(daily["wind_speed"]),
                        "direction": float(daily["wind_deg"]),
                    },
                    "weather": {
                        "description": daily["weather"][0].get("description", ""),
                        "icon": daily["weather"][0].get("icon", ""),
                    },
                }

        self._device["forecast"] = {**self._device["hours"], **daily_data}

        return True

    def __load_forecast_data(self):
        # Onecall API's are more expensive (max 1000 a day - 1 call per 2 minutes) so we update this at a lower frequency
        if not self.__load_forecast_data_one_call():
            if not self.__load_minimal_forecast_data():
                return False

        return True

    def __load_history_data(self):
        # Onecall API's are more expensive (max 1000 a day - 1 call per 2 minutes) so we update this at a lower frequency
        # Here we can do 1 hit a day. As the history is per hole full day at a time, and will not change anymore

        if self.__one_call_version not in ["2.5", "3.0"]:
            # Use an empty history list... should disable the feature in the GUI...
            return True

        now = datetime.now()
        if self.__history_day is not None and (now - self.__history_day).days < 1:
            return True

        self.__history_day = now
        history_data = {}
        for day in range(4):
            now = datetime.now() - timedelta(days=day)
            history_url = "https://api.openweathermap.org/data/{}/onecall/day_summary?lat={}&lon={}&units=metric&date={}&appid={}&lang={}".format(
                self.__one_call_version,
                self._device["geo"]["lat"],
                self._device["geo"]["long"],
                now.strftime("%Y-%m-%d"),
                self.__appid,
                self._device["language"][0:2],
            )
            data = terrariumUtils.get_remote_data(history_url)

            if data is None:
                continue

            day_stamp = now.replace(hour=0, minute=0, second=0, microsecond=0)
            day_periods = {
                "night": 0 * 60 * 60,
                "morning": 6 * 60 * 60,
                "afternoon": 12 * 60 * 60,
                "evening": 18 * 60 * 60,
            }

            history_data = {}
            for period in day_periods:
                time = day_stamp + timedelta(seconds=day_periods[period])

                history_data[time.isoformat()] = {
                    "timestamp": time,
                    "temperature": float(data["temperature"][period]),
                    "humidity": float(data["humidity"]["afternoon"]),
                }

            self._device["history"] = history_data

        return True
