#!/usr/bin/env python
import requests

# Enter here the two sensors to measure the difference
# You can find the ID values in the settings.cfg file after you have added the individual sensors.
SENSORS=['dcd784579ab801750421dd3634d69fd5','176ba2cc660046a239e15b1f94ef8091']
# Enter the hostname for TerrariumPI. Should be working out of the box
TERRARIUMPI_SERVER='http://localhost:8090'

# !!! No changes below this line !!!
difference = None
if len(SENSORS) == 2:
  try:
    sensor1_value = requests.get('{}/api/sensors/{}'.format(TERRARIUMPI_SERVER,SENSORS[0]))
    if sensor1_value.status_code == 200:
      sensor1_value = sensor1_value.json()['sensors'][0]['current']

  except Exception as ex:
    sensor1_value = None

  if sensor1_value is not None:
    try:
      sensor2_value = requests.get('{}/api/sensors/{}'.format(TERRARIUMPI_SERVER,SENSORS[1]))
      if sensor2_value.status_code == 200:
        sensor2_value = sensor2_value.json()['sensors'][0]['current']
        difference = abs(sensor1_value - sensor2_value)

    except Exception as ex:
      sensor2_value = None

if difference is None:
  raise ValueError('No data available')

print(difference)