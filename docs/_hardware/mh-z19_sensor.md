---
title: MH-Z19 CO2 sensor
categories: [Hardware, Sensor]
tags: [sensor, co2, temperature]

image:
  path: /assets/img/mh-z19.webp
  src: /assets/img/mh-z19.webp
  alt: "MH-Z19 CO2 sensor header image"

device_types: [co2, temperature]
device_address: "Serial address and connect to GPIO pin 8 (TX) and 10 (RX). Ex: `/dev/ttyS0`"
device_url: https://gadget-freakz.com/product/mh-z19-air-co2-sensor/
---

## Information

The MH-Z19 is an indoor CO2 sensor. It is just a sensor, which means that you need to have separate system to read and control the data measured by the MH-Z19. This can for example be a wemos or nodemcu device that you need to have in place to control the MH-Z19 sensor. When you have this setup in place, you are able to send data from this sensor to your home automation or smart home platform.

### Features

- High sensitivity, high resolution.
- Output modes: UART and PWM wave.
- Anti-water vapor interference.No poisoning.
- Temperature compensation, excellent linear output.
- Low power consumption,good stability and long lifespan.
- It is widely used in the HVAC refrigeration and indoor air quality monitoring.

{% include_relative _sensor_detail.md %}
