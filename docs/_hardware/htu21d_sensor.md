---
title: HTU21D sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity]

image:
  path: /assets/img/htu21d.webp
  src: /assets/img/htu21d.webp
  alt: "HTU21D sensor header image"

device_types: [temperature, humidity]
device_address: "&lt;I2C Address&gt;,[I2C Bus] where the [I2C bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `0x3f`"
device_url: https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor/overview
---

## Information

The HTU21D is a low-cost, easy to use, highly accurate, digital humidity and temperature sensor. This sensor is ideal for environmental sensing and data logging and perfect for a weather stations or humidor control systems. All you need is two lines for I2C communication and you’ll have relative humidity readings and very accurate temperature readings as a bonus!

There are only four pins that need to be hooked up in order to start using this sensor in a project. One for VCC, one for GND, and two data lines for I2C communication. This breakout board has built in 4.7k pull up resistors for I2C communications. If you’re hooking up multiple I2C devices on the same bus, you may want to disable these resistors.

Note: Full drops of water can damage the sensor. We recommend wrapping the board in Teflon/irrigation tape for extreme conditions where water droplets may find their way onto the sensor.

{% include_relative _sensor_detail.md %}
