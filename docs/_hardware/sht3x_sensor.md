---
title: Sensirion SHT3X sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity]

image:
  path: /assets/img/SHT3X.webp
  src: /assets/img/SHT3X.webp
  alt: "Sensirion SHT3X sensor header image"

device_types: [temperature, humidity]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `0x44`"
device_url: http://www.pibits.net/code/raspberry-pi-sht31-sensor-example.php
---

## Information

SHT31 is the next generation of Sensirion's temperature and humidity sensors. It builds on a new CMOSens® sensor chip that is at the heart of Sensirion's new humidity and temperature platform.

The SHT3x-DIS has increased intelligence, reliability and improved accuracy specifications compared to its predecessor. Its functionality includes enhanced signal processing, two distinctive and user selectable I2C addresses and communication speeds of up to 1 MHz. The DFN package has a footprint of 2.5 x 2.5 mm2 while keeping a height of 0.9 mm.

This allows for integration of the SHT3x-DIS into a great variety of applications.

### Features

- Fully calibrated, linearized, and temperature compensated digital output
- Wide supply voltage range, from 2.4 V to 5.5 V
- I2C Interface with communication speeds up to 1 MHz and two user selectable addresses

{% include_relative _sensor_detail.md %}
