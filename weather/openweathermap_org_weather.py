# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from datetime import datetime
from time import time

from . import terrariumWeatherAbstract
from terrariumUtils import terrariumUtils


class terrariumOpenweathermap(terrariumWeatherAbstract):
    HARDWARE = "Openweathermap.org"
    NAME = "OpenWeatherMap weather data"
    VALID_SOURCE = "^https?://api\.openweathermap\.org/data/2\.5/weather\?q=(?P<city>[^,&]+),(?P<country>[^,&]{2,3})&appid=[a-z0-9]{32}"
    INFO_SOURCE = "https://api.openweathermap.org/data/2.5/weather?q=[CITY],[COUNTRY_2CHAR]&appid=[YOUR_API_KEY]"

    def __init__(self, address, unit_values, language):
        self.__history_day = None
        self.__one_call_version = None
        self.__appid = None
        super().__init__(address, unit_values, language)

    def __load_general_data(self):
        address = self.address + "&units=metric&lang=" + self._device["language"][0:2]
        logger.debug("Loading weather source {}".format(address))
        data = terrariumUtils.get_remote_data(address)
        if data:
            self._data["city"] = data["name"]
            self._data["country"] = data["sys"]["country"]
            self._data["geo"] = {"lat": float(data["coord"]["lat"]), "long": float(data["coord"]["lon"])}
            self._data["url"] = "https://openweathermap.org/city/{}".format(data["id"])
            self._data["credits"] = "OpenWeatherMap weather data"
            self._data["timezone"] = int(data["timezone"])

            address = terrariumUtils.parse_url(self.address.lower())
            self.__appid = address["query_params"]["appid"]

            return True

        logger.warning("Error loading online weather data from source {} !".format(address))
        return False

    def __load_minimal_forecast_data(self):
        data = terrariumUtils.get_remote_data(
            "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric&lang={}".format(
                self._data["geo"]["lat"], self._data["geo"]["long"], self.__appid, self._device["language"][0:2]
            )
        )

        if not data:
            return False

        # Reset data
        self._data["days"] = []
        self._data["forecast"] = []
        sunrise = int(data["city"]["sunrise"] + self._data["timezone"])
        sunset = int(data["city"]["sunset"] + self._data["timezone"])

        for forecast in data["list"]:
            timestamp = int(forecast["dt"] + self._data["timezone"])

            self._data["forecast"].append(
                {
                    "timestamp": timestamp,
                    "temperature": float(forecast["main"]["temp"]),
                    "humidity": float(forecast["main"]["humidity"]),
                }
            )

            if "12:00" in forecast["dt_txt"]:
                self._data["days"].append(
                    {
                        "timestamp": timestamp,
                        "rise": sunrise + (len(self._data["days"]) * 24 * 3600),
                        "set": sunset + (len(self._data["days"]) * 24 * 3600),
                        "temp": float(forecast["main"]["temp"]),
                        "humidity": float(forecast["main"]["humidity"]),
                        "wind": {
                            "speed": float(forecast["wind"]["speed"]),  # Speed is in meter per second
                            "direction": float(forecast["wind"]["deg"]),
                        },
                        "weather": {
                            "description": forecast["weather"][0].get("description", ""),
                            "icon": forecast["weather"][0].get("icon", ""),
                        },
                    }
                )

        logger.info("Using Openweathermap Free API")
        self.__one_call_version = "free"
        return True

    def __load_forecast_data_one_call(self):
        data = None
        if self.__one_call_version is None or self.__one_call_version == "3.0":
            data = terrariumUtils.get_remote_data(
                "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units=metric&exclude=minutely&appid={}&lang={}".format(
                    self._data["geo"]["lat"], self._data["geo"]["long"], self.__appid, self._device["language"][0:2]
                )
            )

        if (self.__one_call_version is None and not data) or self.__one_call_version == "2.5":
            data = terrariumUtils.get_remote_data(
                "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=minutely&appid={}&lang={}".format(
                    self._data["geo"]["lat"], self._data["geo"]["long"], self.__appid, self._device["language"][0:2]
                )
            )
            if data:
                self.__one_call_version = "2.5"
                logger.info(f"Using Openweathermap One Call API {self.__one_call_version}")

        elif self.__one_call_version is None:
            self.__one_call_version = "3.0"
            logger.info(f"Using Openweathermap One Call API {self.__one_call_version}")

        if not data:
            return False

        # Reset data
        self._data["days"] = []
        self._data["forecast"] = []

        for hourly in data["hourly"]:
            # Store all timestamp data as GMT+0000 in memory/database
            self._data["forecast"].append(
                {
                    "timestamp": int(hourly["dt"] + self._data["timezone"]),
                    "temperature": float(hourly["temp"]),
                    "humidity": float(hourly["humidity"]),
                }
            )

        day_periods = {"morn": -6 * 60 * 60, "day": 0, "eve": 6 * 60 * 60, "night": 12 * 60 * 60}
        for daily in data["daily"]:
            for period in day_periods:
                timestamp = int(daily["dt"] + self._data["timezone"] + day_periods[period])

                # Exclude already existing and pasted hourly forecasts
                if (
                    timestamp not in [item["timestamp"] for item in self._data["forecast"]]
                    and timestamp > self._data["forecast"][0]["timestamp"]
                ):
                    self._data["forecast"].append(
                        {
                            "timestamp": timestamp,
                            "temperature": float(daily["temp"][period]),
                            "humidity": float(daily["humidity"]),
                        }
                    )

                if "day" == period:
                    # Store day data for icons
                    day = daily
                    if len(self._data["days"]) == 0:
                        # First day, we use the current data
                        day = data["current"]
                        day["temp"] = {period: data["current"]["temp"]}

                    self._data["days"].append(
                        {
                            "timestamp": timestamp,
                            "rise": int(day["sunrise"] + self._data["timezone"]),
                            "set": int(day["sunset"] + self._data["timezone"]),
                            "temp": float(day["temp"][period]),
                            "humidity": float(day["humidity"]),
                            "wind": {
                                "speed": float(day["wind_speed"]),  # Speed is in meter per second
                                "direction": float(day["wind_deg"]),
                            },
                            "weather": {
                                "description": day["weather"][0].get("description", ""),
                                "icon": day["weather"][0].get("icon", ""),
                            },
                        }
                    )

        return True

    def __load_forecast_data(self):
        # Onecall API's are more expensive (max 1000 a day - 1 call per 2 minutes) so we update this at a lower frequency
        if not self.__load_forecast_data_one_call():
            if not self.__load_minimal_forecast_data():
                return False

        self._data["forecast"] = sorted(self._data["forecast"], key=lambda d: d["timestamp"])
        self._data["days"] = sorted(self._data["days"], key=lambda d: d["timestamp"])

        return True

    def __load_history_data(self):
        # Onecall API's are more expensive (max 1000 a day - 1 call per 2 minutes) so we update this at a lower frequency
        # Here we can do 1 hit a day. As the history is per hole full day at a time, and will not change anymore
        if self.__history_day is not None and self.__history_day == int(
            datetime.utcfromtimestamp(int(datetime.now().timestamp()) + self._data["timezone"]).strftime("%d")
        ):
            return True

        start = time()
        self._data["history"] = []
        self.__history_day = int(
            datetime.utcfromtimestamp(int(datetime.now().timestamp()) + self._data["timezone"]).strftime("%d")
        )

        if self.__one_call_version not in ["2.5", "3.0"]:
            # Use an empty history list... should disable the feature in the GUI...
            return True

        address = terrariumUtils.parse_url(self.address)
        for day in range(1, 3):
            now = int(datetime.now().timestamp()) + self._data["timezone"] - (day * 24 * 60 * 60)
            history_url = "https://api.openweathermap.org/data/{}/onecall/timemachine?lat={}&lon={}&units=metric&dt={}&appid={}&lang={}".format(
                self.__one_call_version,
                self._data["geo"]["lat"],
                self._data["geo"]["long"],
                now,
                address["query_params"]["appid"],
                self._device["language"][0:2],
            )
            data = terrariumUtils.get_remote_data(history_url)

            if data is None:
                continue

            for item in data["hourly"]:
                self._data["history"].append(
                    {
                        "timestamp": int(item["dt"] + self._data["timezone"]),
                        "temperature": float(item["temp"]),
                        "humidity": float(item["humidity"]),
                        "pressure": float(item["pressure"]),
                        "uvi": float(item["uvi"]),
                    }
                )

        self._data["history"] = sorted(self._data["history"], key=lambda d: d["timestamp"])
        self.__history_day = int(
            datetime.utcfromtimestamp(int(datetime.now().timestamp()) + self._data["timezone"]).strftime("%d")
        )

        logger.info(
            f'Loaded new historical weather data ({len(self._data["history"])} measurements) from {datetime.fromtimestamp(int(self._data["history"][0]["timestamp"]))} till {datetime.fromtimestamp(int(self._data["history"][len(self._data["history"])-1]["timestamp"]))} in {time()-start:.2f} seconds.'
        )
        return True

    def _load_data(self):
        if self.__load_general_data():
            if self.__load_forecast_data():
                return self.__load_history_data()

        return False
