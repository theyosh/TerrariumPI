---
title: BME680 sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity, pressure, altitude]

image:
  path: /assets/img/bme680.webp
  src: /assets/img/bme680.webp
  alt: "BME680 sensor header image"

device_types: [temperature, humidity, pressure, altitude]
device_address: "&lt;I2C Address&gt;,[I2C Bus] where the [I2C bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `0x3f,3`"
device_url: https://shop.pimoroni.com/products/bme680-breakout?variant=12491552129107
---

## Information

The BME680 is the first gas sensor that integrates high-linearity and high-accuracy gas, pressure, humidity and temperature sensors. It is especially developed for mobile applications and wearables where size and low power consumption are critical requirements. The BME680 guarantees - depending on the specific operating mode - optimized consumption, long-term stability and high EMC robustness. In order to measure air quality for personal wellbeing the gas sensor within the BME680 can detect a broad range of gases such as volatile organic compounds (VOC).

{% include_relative _sensor_detail.md %}
