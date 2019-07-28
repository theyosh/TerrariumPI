# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from gpiozero import MCP3008
from gevent import sleep

from terrariumUtils import terrariumUtils
from terrariumSensor import terrariumSensorSource

class terrariumAnalogSensor(terrariumSensorSource):
  TYPE = None
  VALID_SENSOR_TYPES = []

  def load_data(self):
    data = None

    if self.get_address() is not None and len(self.get_address().split(',')) >= 1:
      address = self.get_address().split(',')
      data_pin = address[0]
      device = 0 if len(address[0]) == 1 else address[1]

      sensor = MCP3008(channel=int(data_pin), device=int(device))
      values = []
      for counter in range(5):
        value = sensor.value
        if terrariumUtils.is_float(value):
          values.append(float(value))
        sleep(0.2)

      sensor = None
      # sort values from low to high
      values.sort()
      # Calculate average. Exclude the min and max value. And therefore devide by 3
      data = round((sum(values[1:-1]) / (len(values)-2)),5)

    return data

class terrariumSKUSEN0161Sensor(terrariumAnalogSensor):
  TYPE = 'sku-sen0161'
  VALID_SENSOR_TYPES = ['ph']

  def load_data(self):
    data = super(terrariumSKUSEN0161Sensor,self).load_data()

    if data is None:
      return None

    # https://github.com/theyosh/TerrariumPI/issues/108
    # We measure the values in volts already, so no deviding by 1000 as original script does
    return { self.get_sensor_type() : ((float(data) * ( 5000.0 / 1024.0)) * 3.3 + 0.1614)}
