---
title: Sensirion SHT3X sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity]

image:
  path: /assets/img/SHT3X.webp
  src: /assets/img/SHT3X.webp
  alt: "Sensirion SHT3X sensor header image"

device_types: [temperature, humidity]
device_address: "&lt;I2C Address&gt;,[I2C Bus] where the [I2C bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `0x44`"
device_url: http://www.pibits.net/code/raspberry-pi-sht31-sensor-example.php
---

## Information

SHT31 is the next generation of Sensirion's temperature and humidity sensors. It builds on a new CMOSens® sensor chip that is at the heart of Sensirion's new humidity and temperature platform.

### Features

- Fully calibrated, linearized, and temperature compensated digital output
- Wide supply voltage range, from 2.4 V to 5.5 V
- I2C Interface with communication speeds up to 1 MHz and two user selectable addresses

{% include_relative _sensor_detail.md %}
