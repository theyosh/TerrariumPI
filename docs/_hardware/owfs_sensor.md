---
title: One-Wire File System (OWFS)
categories: [Hardware, Sensor]
tags: [sensor, 1-wire, temperature, humidity]

image:
  path: /assets/img/owfs.webp
  src: /assets/img/owfs.webp
  alt: "One-Wire File System (OWFS) header image"

device_types: [temperature,humidity]
device_address: "Enter the sensors address <br />Ex: `280115b231f3ff`"
device_auto_detect: true
device_url: https://www.sheepwalkelectronics.co.uk/product_info.php?cPath=22&products_id=30
---

## Information

I2C to 1-Wire host adapter for your Raspberry Pi. This device is compatible with all variants of Raspberry Pi including the new Raspberry Pi 2. If you have anything other than an early Raspberry Pi model A or B (i.e. the models with the 26pin GPIO header) we would suggest you look at the RPI2v2 instead of this module.

This module provides an easy way to connect 1-Wire devices to your Raspberry Pi without using up one of the USB ports. It is based around a DS2482-100 I2C to 1-Wire IC.

Connection to your 1-Wire network is either by the RJ45 socket or the screw terminals. The RJ45 socket is wired to the same standard as all our modules to allow the easy assembly of a network using standard ethernet cables. It includes +5V on pin 2 for any modules that require it.

It is available as an assembled module, kit of parts or bare PCB. Please note that if you buy the kit or PCB that there are three surface mount ICs on the board so it is not really suitable for anyone inexperienced at soldering.

### DS18B20

An easy to use temperature sensor is the [DS18B20 sensor](https://components101.com/sensors/ds18b20-temperature-sensor)

{% include_relative _sensor_detail.md %}
