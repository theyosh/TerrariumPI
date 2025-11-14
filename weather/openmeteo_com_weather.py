# -*- coding: utf-8 -*-
# Created by GamingLPyt: (https://github.com/theyosh/TerrariumPI/issues/1043)
import terrariumLogging

from datetime import datetime, timedelta, timezone
from time import time

from . import terrariumWeatherAbstract
from terrariumUtils import terrariumUtils


logger = terrariumLogging.logging.getLogger("Open-Meteo")


class terrariumOpenmeteo(terrariumWeatherAbstract):
    HARDWARE = "Open-Meteo.com"
    NAME = "Open-Meteo weather data"

    # Example URL format expected by the TerrariumPI GUI:
    #
    # https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41
    #
    # Basic regex validation for user-entered URLs
    VALID_SOURCE = (
        r"^https?:\/\/api\.open-meteo\.com\/v1\/forecast\?"
        r"latitude=(?P<lat>-?\d+(\.\d+)?)&longitude=(?P<long>-?\d+(\.\d+)?)(?:&.*)?$"
    )

    # Shown in GUI as example
    INFO_SOURCE = "https://api.open-meteo.com/v1/forecast?" "latitude=[LAT]&longitude=[LON]"

    def __init__(self, address, unit_values, language):
        # No API key required
        super().__init__(address, unit_values, language)

    # -------------------------------------------------------------
    # Helper functions
    # -------------------------------------------------------------
    @staticmethod
    def _parse_iso_time(value, utc_offset_seconds):
        """
        Open-Meteo timestamps are provided as ISO strings.
        Convert them into UNIX timestamps using the location's UTC offset.
        """
        if value is None:
            return None

        formats = ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d")

        dt = None
        for fmt in formats:
            try:
                dt = datetime.strptime(value, fmt)
                break
            except ValueError:
                pass

        if dt is None:
            return None

        offset = timezone(timedelta(seconds=int(utc_offset_seconds)))
        dt = dt.replace(tzinfo=offset)

        return int(dt.timestamp())

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

    # -------------------------------------------------------------
    # Open-Meteo API calls
    # -------------------------------------------------------------
    def __build_base_coordinates(self):
        """Extract latitude & longitude from the configured URL."""
        parsed = terrariumUtils.parse_url(self.address)
        query = parsed.get("query_params", {})

        try:
            lat = float(query.get("latitude"))
            lon = float(query.get("longitude"))
        except (TypeError, ValueError):
            logger.error("Invalid Open-Meteo URL. Latitude and longitude required.")
            return None, None

        return lat, lon

    def __load_forecast_and_current(self):
        """
        Fetch current weather and forecast data from Open-Meteo.

        Fills TerrariumPI structures:
          - city
          - country
          - geo
          - url
          - credits
          - timezone
          - forecast (hourly)
          - days (daily)
        """
        start = time()

        lat, lon = self.__build_base_coordinates()
        if lat is None or lon is None:
            return False

        lang = self._device.get("language", "en")[0:2]

        # One combined API call for all relevant data. Temperatures are in C, wind speed is in km/h
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current_weather=true"
            "&hourly=temperature_2m,relative_humidity_2m"
            "&daily=weathercode,sunrise,sunset,temperature_2m_max,"
            "temperature_2m_min,windspeed_10m_max,winddirection_10m_dominant"
            f"&timezone={datetime.now().astimezone().tzinfo}&language={lang}"
        )

        data = terrariumUtils.get_remote_data(url)
        if not data:
            logger.error("Failed loading Open-Meteo forecast data.")
            return False

        # Basic metadata
        self._data["geo"] = {"lat": float(lat), "long": float(lon)}
        self._data["url"] = "https://open-meteo.com/"
        self._data["credits"] = "Open-Meteo.com weather data"
        self._data["timezone"] = 0
        self._data.setdefault("city", "")
        self._data.setdefault("country", "")

        # -------------------------
        # Hourly forecast
        # -------------------------
        self._data["forecast"] = []
        hourly = data.get("hourly", {})
        h_times = hourly.get("time", [])
        h_temp = hourly.get("temperature_2m", [])
        h_hum = hourly.get("relative_humidity_2m", [])

        for t, temp, hum in zip(h_times, h_temp, h_hum):
            ts = self._parse_iso_time(t, self._data["timezone"])
            if ts is None:
                continue

            self._data["forecast"].append(
                {
                    "timestamp": ts,
                    "temperature": float(temp),
                    "humidity": float(hum),
                }
            )

        # -------------------------
        # Daily data
        # -------------------------
        self._data["days"] = []
        daily = data.get("daily", {})

        d_time = daily.get("time", [])
        d_sunrise = daily.get("sunrise", [])
        d_sunset = daily.get("sunset", [])
        d_tmax = daily.get("temperature_2m_max", [])
        d_tmin = daily.get("temperature_2m_min", [])
        d_wspeed = daily.get("windspeed_10m_max", [])
        d_wdir = daily.get("winddirection_10m_dominant", [])
        d_code = daily.get("weathercode", [])

        for i in range(len(d_time)):
            day_ts = self._parse_iso_time(d_time[i], self._data["timezone"])
            sunrise_ts = self._parse_iso_time(d_sunrise[i] if i < len(d_sunrise) else None, self._data["timezone"])
            sunset_ts = self._parse_iso_time(d_sunset[i] if i < len(d_sunset) else None, self._data["timezone"])

            tmax = float(d_tmax[i]) if i < len(d_tmax) else None
            tmin = float(d_tmin[i]) if i < len(d_tmin) else None

            if tmax is not None and tmin is not None:
                tavg = (tmax + tmin) / 2.0
            else:
                tavg = tmax or tmin or 0.0

            # Convert to m/s
            wind_speed = (float(d_wspeed[i]) if i < len(d_wspeed) else 0.0) / 3.6
            wind_dir = float(d_wdir[i]) if i < len(d_wdir) else 0.0
            code = int(d_code[i]) if i < len(d_code) else None

            description = self._weathercode_to_description(code)
            icon = self._weathercode_to_icon(code)

            self._data["days"].append(
                {
                    "timestamp": day_ts or 0,
                    "rise": sunrise_ts or 0,
                    "set": sunset_ts or 0,
                    "temp": float(tavg),
                    "humidity": 0.0,  # No daily humidity in API
                    "wind": {
                        "speed": wind_speed,
                        "direction": wind_dir,
                    },
                    "weather": {
                        "description": description,
                        "icon": icon,
                    },
                }
            )

        self._data["forecast"].sort(key=lambda d: d["timestamp"])
        self._data["days"].sort(key=lambda d: d["timestamp"])

        logger.info(f"Loaded Open-Meteo weather data in {time() - start:.2f} seconds.")
        return True

    def __load_history_data(self):
        """
        Load historical temperature, humidity, pressure and UV data.
        If this fails, history is simply disabled.
        """
        start = time()

        lat, lon = self.__build_base_coordinates()
        if lat is None or lon is None:
            self._data["history"] = []
            return True

        now = datetime.utcnow().date()
        start_date = (now - timedelta(days=2)).strftime("%Y-%m-%d")
        end_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")

        # Temperatures are in C, wind speed is in km/h
        url = (
            "https://historical-forecast-api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={start_date}&end_date={end_date}"
            "&hourly=temperature_2m,relative_humidity_2m,pressure_msl,uv_index"
            f"&timezone={datetime.now().astimezone().tzinfo}"
        )

        data = terrariumUtils.get_remote_data(url)
        if not data:
            logger.warning("Failed loading Open-Meteo historical data. History disabled.")
            self._data["history"] = []
            return True

        hourly = data.get("hourly", {})

        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        hums = hourly.get("relative_humidity_2m", [])
        press = hourly.get("pressure_msl", [])
        uvi = hourly.get("uv_index", [])

        self._data["history"] = []

        for t, temp, hum, p, index in zip(times, temps, hums, press, uvi):
            ts = self._parse_iso_time(t, self._data["timezone"])
            if ts is None:
                continue

            self._data["history"].append(
                {
                    "timestamp": ts,
                    "temperature": float(temp),
                    "humidity": float(hum),
                    "pressure": float(p),
                    "uvi": float(index),
                }
            )

        self._data["history"].sort(key=lambda d: d["timestamp"])

        logger.info(
            f"Loaded Open-Meteo historical data "
            f'({len(self._data["history"])} entries) in {time() - start:.2f} seconds.'
        )

        return True

    # -------------------------------------------------------------
    # Required by TerrariumPI
    # -------------------------------------------------------------
    def _load_data(self):
        """
        Entry point used by TerrariumPI:
        - Load forecast and current data
        - Load history (optional)
        """
        if not self.__load_forecast_and_current():
            return False

        self.__load_history_data()
        return True
