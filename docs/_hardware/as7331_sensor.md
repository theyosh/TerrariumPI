---
title: AS7331 UVA, UVB, UVC light and temperature sensor
categories: [Hardware, Sensor]
tags: [sensor, uva, uvb, uvi, temperature]

image:
  path: /assets/img/AS7331.webp
  src: /assets/img/AS7331.webp
  alt: 'AS7331 UVA, UVB, UVC light and temperature sensor header image'

device_types: [uva, uvb, uvc, uvi, temperature]
device_address:
  '&lt;I2C Address&gt;,[I2C Bus] where the [I2C
  bus](/TerrariumPI/hardware/#i2c-bus) is optional<br />Ex: `0x74`'
device_url: https://www.sparkfun.com/sparkfun-spectral-uv-sensor-as7331-qwiic.html
---

## Information

This SparkFun Qwiic Spectral UV Sensor features the AS7331 UV sensor from ams
OSRAM©. It measures UV radiation on three channels: UVA (320-400nm), UVB
(280-320nm), and UVC (200-280nm) with high sensitivity and accuracy. The three
channels on the AS7331 each have individual photodiodes with built-in
interference filters. The sensor has four operating modes: Single Measurement
(CMD), Continuous Measurement (CONT), SYNchronized Start (SYNS), and
SYNchronized Start & End (SYND), with an automatic power-down sequence between
measurements for low current consumption in all three modes.

The AS7331 communicates over I2C, so naturally, this breakout routes the I2C bus
pins (3.3V, GND, SDA, and SCL) to a pair of Qwiic connectors on each side of the
board for solderless assembly but also routes them to a 0.1in.-spaced
through-hole header on the bottom of the board for users who prefer a soldered
connection. This header also includes the sensor's Interrupt and Sync pins. The
AS7331 has four I2C addresses (default: 0x74) set by adjusting the A1 and A0
solder jumpers on the back of the board.

We've written an Arduino library to make it simple to quickly get started
configuring the AS7331 and receiving UV radiation data from the sensor. Download
it through the Arduino Library Manager tool by searching for 'SparkFun AS7331'
or download it from the GitHub repository linked in the Documents tab.

### Features

- Operating Voltage: 2.7V-3.6V
- Current Consumption:
  - Active Measurement: 1.42mA (Typ.)
  - Standby Mode: 970µA
  - Power Down Mode: 1µA
- Three UV Channels: UVA, UVB, & UVC
- Each with dedicated photodiode
- Four Operating Modes:
  - Single Measurement
  - Continuous Measurement
  - Synchronized Start Measurement
  - Synchronized Start/Stop Measurement
- High Dynamic Range: Up to 3.43E+10 (resolution multiplied by gain range)
- 2x Qwiic Connectors
- Four Adjustable I2C Addresses
- Set through A0 & A1 pins
- 0x74 (Default), 0x75, 0x76, & 0x77

{% include_relative _sensor_detail.md %}
