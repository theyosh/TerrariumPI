# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

import gettext
import re
import datetime
import requests
import subprocess
import threading
import bcrypt
import os
import sys
import math
import asyncio
import base64
import collections

from cryptography.fernet import Fernet

from math import log

import time
import uuid


# https://stackoverflow.com/a/6798042
# works in Python 2 & 3
class _Singleton(type):
    """A metaclass that creates a Singleton base class when called."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class terrariumSingleton(_Singleton("terrariumSingletonMeta", (object,), {})):
    pass


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class terrariumAsync(terrariumSingleton):
    def __init__(self):
        def __run():
            self.async_loop.run_until_complete(self._keep_running())
            self.async_loop.close()

        self.async_loop = asyncio.get_event_loop()
        process = threading.Thread(target=__run)
        process.start()

    def stop(self):
        self.__running = False

    async def _keep_running(self):
        self.__running = True
        while self.__running:
            await asyncio.sleep(1)


class terrariumCache(terrariumSingleton):
    def __init__(self):
        self.__cache = {}
        self.__running = {}
        logger.debug("Initialized cache")

    def __cleanup(self):
        now = int(time.time())
        for key in list(self.__cache.keys()):
            if self.__cache[key]["expire"] < now:
                logger.debug(
                    "Delete cache key {} with expire date {}".format(
                        key, datetime.datetime.fromtimestamp(self.__cache[key]["expire"])
                    )
                )
                del self.__cache[key]

    def set_data(self, hash_key, data, cache_timeout=30):
        # When cache value is negative, cache it for one year.... should be long enough.. ;)
        cache_timeout = cache_timeout if cache_timeout > 0 else int(datetime.timedelta(days=365).total_seconds())
        self.__cache[hash_key] = {"data": data, "expire": int(time.time()) + cache_timeout}
        logger.debug("Added new cache data with hash: {}. Total in cache: {}".format(hash_key, len(self.__cache)))
        self.__cleanup()

    def get_data(self, hash_key, default=None):
        if hash_key in self.__cache and self.__cache[hash_key]["expire"] > int(time.time()):
            return self.__cache[hash_key]["data"]

        return default

    def clear_data(self, hash_key):
        if hash_key in self.__cache:
            del self.__cache[hash_key]

    def set_running(self, hash_key):
        hash_key = f"running-{hash_key}"
        if not self.is_running(hash_key):
            self.set_data(f"running-{hash_key}", True)
            return True

        return False

    def is_running(self, hash_key):
        hash_key = f"running-{hash_key}"
        return self.get_data(hash_key) is not None

    def clear_running(self, hash_key):
        hash_key = f"running-{hash_key}"
        if hash_key in self.__cache:
            del self.__cache[hash_key]


class terrariumUtils:
    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def generate_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf8")

    @staticmethod
    def check_password(password, passwordhash):
        if password is None or passwordhash is None:
            return False

        return bcrypt.checkpw(password.encode(), passwordhash.encode())

    @staticmethod
    def __encryption_key():
        salt = os.environ["SALT"]
        salt = f"{salt:0>32}"
        salt = base64.urlsafe_b64encode(salt.encode("utf8"))
        return Fernet(salt)

    @staticmethod
    def encrypt(string):
        try:
            encryption = terrariumUtils.__encryption_key()
            return encryption.encrypt(string.encode()).decode()
        except Exception:
            return string

    @staticmethod
    def decrypt(string):
        try:
            encryption = terrariumUtils.__encryption_key()
            return encryption.decrypt(string.encode()).decode()
        except Exception:
            return string

    @staticmethod
    def to_fahrenheit(value):
        return 9.0 / 5.0 * float(value) + 32.0

    @staticmethod
    def to_celsius(value):
        return (float(value) - 32) * 5.0 / 9.0

    @staticmethod
    def to_kelvin(value):
        return float(value) + 273.15

    @staticmethod
    def to_inches(value):
        # https://www.convertunits.com/from/cm/to/inches , http://www.manuelsweb.com/in_cm.htm
        # Input value is in cm
        return (39.370078740157 / 100.0) * float(value)

    @staticmethod
    def to_us_gallons(value):
        # https://www.asknumbers.com/gallons-to-liters.aspx
        return float(value) / 3.7854118

    @staticmethod
    def to_uk_gallons(value):
        # https://www.asknumbers.com/gallons-to-liters.aspx
        return float(value) / 4.54609

    @staticmethod
    def to_kmh(value):
        return float(value) * 3.6

    @staticmethod
    def to_mph(value):
        return float(value) * 2.236936

    @staticmethod
    def to_fs(value):
        return float(value) * 3.2808399

    @staticmethod
    def to_beaufort(value):
        return math.ceil(math.pow(math.pow(value, 2), float(1) / 3))

    @staticmethod
    def convert_to_value(current, indicator):
        if not terrariumUtils.is_float(current):
            return None

        indicator = indicator.lower()
        if "f" == indicator:
            current = terrariumUtils.to_fahrenheit(current)
        elif "k" == indicator:
            current = terrariumUtils.to_kelvin(current)
        elif "km/h" == indicator:
            current = terrariumUtils.to_kmh(current)
        elif "m/h" == indicator:
            current = terrariumUtils.to_mph(current)
        elif "f/s" == indicator:
            current = terrariumUtils.to_fs(current)
        elif "bf" == indicator:
            current = terrariumUtils.to_beaufort(current)
        elif "inch" == indicator:
            current = terrariumUtils.to_inches(current)
        elif "usgall" == indicator:
            current = terrariumUtils.to_us_gallons(current)
        elif "ukgall" == indicator:
            current = terrariumUtils.to_uk_gallons(current)

        return float(current)

    @staticmethod
    def is_float(value):
        if value is None or "" == value:
            return False

        try:
            float(value)
            return True
        except Exception:
            return False

    @staticmethod
    def is_true(value):
        return str(value).lower() in ["true", "1", "on", "yes"]

    @staticmethod
    def to_BCM_port_number(value):
        pinout = {
            "gpio3": 2,
            "gpio5": 3,
            "gpio7": 4,
            "gpio8": 14,
            "gpio10": 15,
            "gpio11": 17,
            "gpio12": 18,
            "gpio13": 27,
            "gpio15": 22,
            "gpio16": 23,
            "gpio18": 24,
            "gpio19": 10,
            "gpio21": 9,
            "gpio22": 25,
            "gpio23": 11,
            "gpio24": 8,
            "gpio26": 7,
            "gpio27": 0,
            "gpio28": 1,
            "gpio29": 5,
            "gpio31": 6,
            "gpio32": 12,
            "gpio33": 13,
            "gpio35": 19,
            "gpio36": 16,
            "gpio37": 26,
            "gpio38": 20,
            "gpio40": 21,
        }

        index = "gpio" + str(value).strip()
        if index in pinout:
            return pinout[index]

        return False

    @staticmethod
    def to_BOARD_port_number(value):
        pinout = {
            "BCM2": 3,
            "BCM3": 5,
            "BCM4": 7,
            "BCM14": 8,
            "BCM15": 10,
            "BCM17": 11,
            "BCM18": 12,
            "BCM27": 13,
            "BCM22": 15,
            "BCM23": 16,
            "BCM24": 18,
            "BCM10": 19,
            "BCM9": 21,
            "BCM25": 22,
            "BCM11": 23,
            "BCM8": 24,
            "BCM7": 26,
            "BCM0": 27,
            "BCM1": 28,
            "BCM5": 29,
            "BCM6": 31,
            "BCM12": 32,
            "BCM13": 33,
            "BCM19": 35,
            "BCM16": 36,
            "BCM26": 37,
            "BCM20": 38,
            "BCM21": 40,
        }

        index = "BCM" + str(value).strip()
        if index in pinout:
            return pinout[index]

        return False

    @staticmethod
    def parse_url(url):
        if url is None or "" == url.strip():
            return False

        regex = r"^((?P<scheme>https?|ftp):\/)?\/?((?P<username>.*?)(:(?P<password>.*?)|)@)?(?P<hostname>[^:\/\s]+)(:(?P<port>(\d*))?)?(?P<path>(\/\w+)*\/)(?P<filename>[-\w.]+[^#?\s]*)?(?P<query>\?([^#]*))?(#(?P<fragment>(.*))?)?$"
        matches = re.search(regex, url.strip())
        if matches:
            data = matches.groupdict()
            if data["query"]:
                data["query_params"] = {}
                for query_param in data["query"][1:].split("&"):
                    query_param = query_param.split("=")
                    data["query_params"][query_param[0]] = query_param[1]
            return data

        return False

    @staticmethod
    def is_valid_url(url):
        return terrariumUtils.parse_url(url) is not False

    @staticmethod
    def parse_time(value):
        time = None
        if ":" in value:
            try:
                value = value.split(":")
                time = "{:0>2}:{:0>2}".format(int(value[0]) % 24, int(value[1]) % 60)
            except Exception as ex:
                logger.exception("Error parsing time value %s. Exception %s" % (value, ex))

        return time

    @staticmethod
    def get_remote_data(url, timeout=3, proxy=None, json=False):
        data = None
        try:
            url_data = terrariumUtils.parse_url(url)
            proxies = {"http": proxy, "https": proxy}
            headers = {}
            if json:
                headers["Accept"] = "application/json"

            if url_data["username"] is None:
                response = requests.get(url, headers=headers, timeout=timeout, proxies=proxies, stream=True)
            else:
                response = requests.get(
                    url,
                    auth=(url_data["username"], url_data["password"]),
                    headers=headers,
                    timeout=timeout,
                    proxies=proxies,
                    stream=True,
                )

            if response.status_code == 200:
                if "multipart/x-mixed-replace" in response.headers["content-type"]:
                    # Motion JPEG stream....
                    # https://stackoverflow.com/a/36675148
                    frame = bytes()
                    for chunk in response.iter_content(chunk_size=1024):
                        frame += chunk
                        a = frame.find(b"\xff\xd8")
                        b = frame.find(b"\xff\xd9")
                        if a != -1 and b != -1:
                            return frame[a : b + 2]

                elif "application/json" in response.headers["content-type"]:
                    data = response.json()
                    json_path = (
                        url_data["fragment"].split("/")
                        if "fragment" in url_data and url_data["fragment"] is not None
                        else []
                    )
                    for item in json_path:
                        # Dirty hack to process array data....
                        try:
                            item = int(item)
                        except Exception:
                            item = str(item)

                        data = data[item]
                elif "text" in response.headers["content-type"]:
                    data = response.text
                else:
                    data = response.content

            else:
                data = None

        except Exception as ex:
            print(ex)
            # logger.exception('Error parsing remote data at url %s. Exception %s' % (url, ex))

        return data

    @staticmethod
    def get_script_data(script):
        data = None
        try:
            logger.debug("Running script: %s." % (script))
            # Add python virtual env to PATH to make sure that venv is being used for python
            data = subprocess.check_output(script, shell=True, env={**os.environ, 'PATH': f'{sys.prefix}/bin:' + os.environ['PATH']})
            logger.debug("Output was: %s." % (data))
        except Exception as ex:
            logger.exception("Error parsing script data for script %s. Exception %s" % (script, ex))

        return data

    @staticmethod
    # https://stackoverflow.com/a/62186053
    def flatten_dict(dictionary, parent_key=False, separator="_"):
        items = []
        for key, value in dictionary.items():
            new_key = str(parent_key) + separator + key if parent_key else key
            if isinstance(value, collections.MutableMapping):
                items.extend(terrariumUtils.flatten_dict(value, new_key, separator).items())
            elif isinstance(value, list):
                for k, v in enumerate(value):
                    items.extend(terrariumUtils.flatten_dict({str(k): v}, new_key, separator).items())
            else:
                items.append((new_key, value))

        return dict(items)

    @staticmethod
    def format_uptime(value):
        return str(datetime.timedelta(seconds=int(value)))

    @staticmethod
    def format_filesize(n, power=0, b=1024, u="B", pre=[""] + [p + "i" for p in "KMGTPEZY"]):
        power, n = min(int(log(max(n * b**power, 1), b)), len(pre) - 1), n * b**power
        return "%%.%if %%s%%s" % abs(power % (-power - 1)) % (n / b ** float(power), pre[power], u)

    @staticmethod
    def clean_log_line(logline):
        # Some regex replacement to keep passwords/tokens out off the logging
        search = [r"(:\/\/)([^@]+)(@[^ ]+)", r"(appid=)([^ ]+)"]

        replace = ["\\1*********\\3", "\\1*********"]

        for index in range(len(search)):
            try:
                logline = re.sub(search[index], replace[index], logline)
            except Exception as ex:
                logger.debug(f"Could not clear with regex: {ex}")

        return logline

    @staticmethod
    def clean_address(address):
        if address is None:
            return None

        strip_regex = r"[ ,]+$"
        return re.sub(strip_regex, "", str(address), 0, re.MULTILINE)

    @staticmethod
    def get_translator(lang="en-US"):
        # Load language
        trans = gettext.translation("terrariumpi", "locales/", languages=(lang.replace("-", "_"),))
        return trans.gettext

    @staticmethod
    def is_docker():
        path = "/proc/self/cgroup"
        return os.path.exists("/.dockerenv") or os.path.isfile(path) and any("docker" in line for line in open(path))
