---
title: Sensirion SHT2X sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity]

image:
  src: /assets/img/SHT2X.webp
  alt: "Sensirion SHT2X sensor header image"

device_types: [temperature, humidity]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `0x3f`"
device_url: http://arduinolearning.com/amp/code/sht21-humidity-and-temperature-sensor-example.php
---

## Information
The SHT21 is a low cost humidity and temperature sensor. Its an I2C device so again is very simple to connect to any arduino

The digital SHT2x humidity sensor series is used in high volumes in a wide variety of applications and has today become the de facto industry standard. The SHT2x series consists of a low-cost version with the SHT20 humidity sensor, a standard version with the SHT21 humidity sensor, and a high-end version with the SHT25 humidity sensor. The open cavity mold package – which encapsulates the complete chip except for the humidity sensor area – protects the capacitive humidity sensor against external impact and facilitates excellent long-term stability.

The SHT2x provides calibrated, linearized sensor signals in digital, I2C format. The SHT2x humidity sensor series contains a capacitive-type humidity sensor, a band-gap temperature sensor, and specialized analog and digital integrated circuits ,the resolution of the SHT2x humidity sensor can be changed on command (8/12 bit up to 12/14 bit for RH/T) and a checksum helps to improve communication reliability

{% include_relative _sensor_detail.md %}