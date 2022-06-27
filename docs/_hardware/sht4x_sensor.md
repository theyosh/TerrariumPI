---
title: Sensirion SHT4X sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity]

image:
  path: /assets/img/SHT4X.webp
  src: /assets/img/SHT4X.webp
  alt: "Sensirion SHT4X sensor header image"

device_types: [temperature, humidity]
device_address: "&lt;I2C Address&gt;,[I2C Bus] where the [I2C bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `0x44`"
device_url: http://www.pibits.net/code/raspberry-pi-sht31-sensor-example.php
---

## Information

Sensirion Temperature/Humidity sensors are some of the finest & highest-accuracy devices you can get. And finally, we have some that have a true I2C interface for easy reading. The SHT40 sensor is the fourth generation (started at the SHT10 and worked its way up to the top!). The SHT40 has an excellent ±1.8% typical relative humidity accuracy from 25 to 75% and ±0.2 °C typical accuracy from 0 to 75 °C.

Unlike some earlier SHT sensors, this sensor has a true I2C interface for easy interfacing with only two wires (plus power and ground!). Thanks to the voltage regulator and level shifting circuitry we've included on the breakout It is also is 3V or 5V compliant, so you can power and communicate with it using any micro controller or microcomputer.

### Features

- Relative humidity accuracy: up to ±1.8 %RH
- Temperature accuracy: up to ±0.2 °C
- Breakout supply voltage: 3.3 to 5V
- Average bare sensor current: 0.4 μA (at meas. rate 1 Hz)
- Idle bare sensor current: 80 nA
- I2C fast mode plus, CRC checksum
- Operating range: 0..100 %RH, -40..125 °C
- Fully functional in condensing environment
- Variable power heater
- NIST traceability for sensor
- JEDEC JESD47 qualification for sensor
- Mature technology from global market leader Sensirion
- I2C address 0x44

{% include_relative _sensor_detail.md %}
