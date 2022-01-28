---
title: 1-Wire sensor
categories: [Hardware, Sensor]
tags: [sensor, 1-wire, waterproof, temperature, humidity]

image:
  path: /assets/img/1-Wire.webp
  src: /assets/img/1-Wire.webp
  alt: "1-Wire header image"

device_types: [temperature,humidity]
device_address: "Enter the symlink folder name that are available at `/sys/bus/w1/devices/`<br />Ex: `28-0115b231f3ff`"
device_auto_detect: true
device_url: https://pinout.xyz/pinout/1_wire#
---

## Information

Using the 1-Wire bus is an easy way to add multiple sensors. This can be temperature or humidity sensors. During the startup of TerrariumPI all the sensors that are connected to the 1-Wire bus will be auto detected.

The 1-Wire bus is enabled by the installer and therefore, it will work out of the box. Use physical pin 7 (GPIO 4) for the data wire.

### DS18B20

![1-Wire schema](/assets/img/1-wire-temp.webp){: .right width="300" }

An easy to use temperature sensor is the [DS18B20 sensor](https://components101.com/sensors/ds18b20-temperature-sensor) Make sure you use a 4.7K resistor when connecting 1 or more DS18B20 sensors.

{% include_relative _sensor_detail.md %}
