---
title: BME280 sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity, pressure, altitude]

image:
  path: /assets/img/bme280.webp
  src: /assets/img/bme280.webp
  alt: "BME280 sensor header image"

device_types: [temperature, humidity, pressure, altitude]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `0x3f`"
device_url: https://www.adafruit.com/product/2652
---

## Information
Bosch has stepped up their game with their new BME280 sensor, an environmental sensor with temperature, barometric pressure and humidity! This sensor is great for all sorts of indoor environmental sensing and can even be used in both I2C and SPI!

This precision sensor from Bosch is the best low-cost sensing solution for measuring humidity with ±3% accuracy, barometric pressure with ±1 hPa absolute accuraccy, and temperature with ±1.0°C accuracy. Because pressure changes with altitude, and the pressure measurements are so good, you can also use it as an altimeter with  ±1 meter or better accuracy!

The BME280 is the next-generation of sensors from Bosch, and is the upgrade to the BMP085/BMP180/BMP183 - with a low altitude noise of 0.25m and the same fast conversion time. It has the same specifications, but can use either I2C or SPI. For simple easy wiring, go with I2C. If you want to connect a bunch of sensors without worrying about I2C address collisions, go with SPI.

{% include_relative _sensor_detail.md %}