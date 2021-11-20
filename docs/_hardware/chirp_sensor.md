---
title: Chirp sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, moisture]

image:
  path: /assets/img/chirp.webp
  src: /assets/img/chirp.webp
  alt: "Chirp sensor header image"

device_types: [temperature, moisture]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `0x3f`"
device_url: https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/
---

## Information
Chirp is a plant watering alarm - as simple as that. You put it into the soil near a plant and it emits a tiny chirp when the soil is dry, reminding you to water the plant. Chirp uses capacitive humidity sensing as opposed to resistive humidity sensing, this means, it does not make an electric contact with the soil, avoiding electrode corrosion and soil electrolysis and resulting in better accuracy and longer battery life.

{% include_relative _sensor_detail.md %}