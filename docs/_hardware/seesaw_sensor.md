---
title: Seesaw soil sensor
categories: [Hardware, Sensor]
tags: [sensor, moisture, temperature]

image:
  path: /assets/img/seesaw_sensor.webp
  src: /assets/img/seesaw_sensor.webp
  alt: 'Seesaw soil sensor'

device_types: [moisture, temperature]
device_address:
  '&lt;I2C Address&gt;<br />Ex: `0x49`'
device_url: https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/overview
device_power_management: false
---

## Information

Most low cost soil sensors are resistive style, where there's two prongs and the
sensor measures the conductivity between the two. These work OK at first, but
eventually start to oxidize because of the exposed metal. Even if they're gold
plated! The resistivity measurement goes up and up, so you constantly have to
re-calibrate your code. Also, resistive measurements don't always work in loose
soil.

This design is superior with a capacitive measurement. Capacitive measurements
use only one probe, don't have any exposed metal, and don't introduce any DC
currents into your plants. We use the built in capacitive touch measurement
system built into the ATSAMD10 chip, which will give you a reading ranging from
about 200 (very dry) to 2000 (very wet). As a bonus, we also give you the
ambient temperature from the internal temperature sensor on the microcontroller,
it's not high precision, maybe good to + or - 2 degrees Celsius.

{% include_relative _sensor_detail.md %}
