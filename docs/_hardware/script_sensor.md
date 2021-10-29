---
title: Script Sensor
categories: [Hardware, Sensor]
tags: [sensor, script, temperature, humidity,fertility,ph,uva,moisture,uvb,altitude,co2,distance,uvi,pressure,light]

image:
  src: /assets/img/script_sensor.webp
  alt: "Script sensor header image"

device_types: [temperature, humidity,fertility,ph,uva,moisture,uvb,altitude,co2,distance,uvi,pressure,light]
device_address: "Enter the full path to the script."
device_url: https://github.com/theyosh/TerrariumPI/blob/4.x.y.z/contrib/script_sensor.py
---

## Information
With a script sensor you can make your own script/program that does a measurement and give back the current value.

For temperature, it needs to return the value in Celsius degrees.

{% include_relative _sensor_detail.md %}