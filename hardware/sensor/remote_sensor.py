# -*- coding: utf-8 -*-
from . import terrariumSensor, terrariumSensorLoadingException
from terrariumUtils import terrariumUtils


class terrariumRemoteSensor(terrariumSensor):
    HARDWARE = "remote"
    # Empty TYPES list as this will be filled with all available hardware TYPES
    TYPES = []
    NAME = "Remote sensor (http/https)"

    def _load_hardware(self):
        self.__source_cache_key = None
        if terrariumUtils.is_valid_url(self.address):
            url = self.address
            self.__json_path = []
            if "#" in self.address:
                url = self.address[: self.address.index("#")]
                self.__json_path = self.address[self.address.index("#") + 1 :].split("/")

            self.__source_cache_key = url
            return url
        else:
            raise terrariumSensorLoadingException("Not a valid url.")

    def _get_data(self):
        value = None if self.__source_cache_key is None else self._sensor_cache.get_data(self.__source_cache_key)

        if value is None:
            value = terrariumUtils.get_remote_data(self.device)
            if value is None:
                return None

            if self.__source_cache_key is not None:
                self._sensor_cache.set_data(self.__source_cache_key, value, self._CACHE_TIMEOUT)

        for item in self.__json_path:
            # Dirty hack to process array data....
            try:
                item = int(item)
            except Exception:
                item = str(item)

            value = value[item]

        data = {self.sensor_type: value}
        return data
