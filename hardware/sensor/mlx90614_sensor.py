# -*- coding: utf-8 -*-
from . import terrariumI2CSensor

# pip install PyMLX90614
import mlx90614


class terrariumMLX90614Sensor(terrariumI2CSensor):
    HARDWARE = "mlx90614"
    TYPES = ["temperature"]
    NAME = "MLX90614 IR Thermometer sensor"

    __AMBIENT_MODE = "a"
    __OBJECT_MODE = "o"

    def _load_hardware(self):
        address = self._address
        try:
            address.remove(self.__AMBIENT_MODE)
        except ValueError:
            pass

        try:
            address.remove(self.__OBJECT_MODE)
        except ValueError:
            pass

        device = (address[0], self._open_hardware())
        return device

    def _get_data(self):
        data = None
        with self._open_hardware() as i2c_bus:
            mode = self.__AMBIENT_MODE if self.__AMBIENT_MODE in self._address else self.__OBJECT_MODE
            sensor = mlx90614.MLX90614(i2c_bus, address=self.device[0])
            data = {}
            if self.__AMBIENT_MODE == mode:
                data["temperature"] = sensor.get_amb_temp()
            elif self.__OBJECT_MODE == mode:
                # Seems like get_object_2 give a very low negative value... does not seems the one we need
                data["temperature"] = sensor.get_obj_temp()

        return data
