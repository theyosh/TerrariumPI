---
title: JSN-SR04T ultrasonic ranging sensor
categories: [Hardware, Sensor]
tags: [sensor, distance]

image:
  path: /assets/img/JSN-SR04T.webp
  src: /assets/img/JSN-SR04T.webp
  alt: "JSN-SR04T ultrasonic ranging sensor header image"

device_types: [distance]
device_address: "Enter the [physical pin](/TerrariumPI/hardware/#gpio) number where the `trigger` and `echo` pins are connected in that order<br />Ex: `27,23`"
device_url: https://raspberrypi.stackexchange.com/a/81793
---

## Information
This water proof ultrasonic sensor has good performance with almost the same usage as the HC-S04 module.

Features

- Small size, easy to use
- Low voltage, low power consumption
- High accuracy
- Strong anti-jamming
- Integrated with wire enclosed waterproof probe, suitable for wet, harsh measurement environments

![SR04 Connect diagram](/assets/img/SR04-connect.webp){: .right width="200" }

For a Raspberry PI it needs resistors on the `ECHO` port.

{% include_relative _sensor_detail.md %}