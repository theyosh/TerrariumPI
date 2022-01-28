---
title: LYWSD03MMC bluetooth sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity]

image:
  path: /assets/img/lywsd03mmc.webp
  src: /assets/img/lywsd03mmc.webp
  alt: "LYWSD03MMC bluetooth sensor header image"

device_types: [temperature, humidity]
device_address: "Bluetooth MAC address. Ex: `a4:c1:38:66:e3:52`"
device_auto_detect: true
device_url: https://www.adafruit.com/product/4881
---

## Information

This Bluetooth Temperature Humidity Sensor is a smart sensor with Bluetooth connectivity by using a free app which continuously displays your home or greenhouse indoor environment (temperature and humidity).

### Features

- Compact design.
- Constantly monitors and displays humidity (air moisture), temperature in Celsius or Fahrenheit, and battery life.
- Displays a happy face when conditions are right, and a displeased face when wrong.
- Suitable for indoor environments.
- Bluetooth connectivity and monitoring via BTLE.
- Adhesive mount and battery included.
- Low power consumption.
- Ideal for your home, greenhouse and more.
- User Manual in Japanese

**Warning:** Sometimes firmwares can be updated by the manufacturer via the app, which may cause this device to not communicate with TerrariumPI anymore. TerrariumPI doesn't need any app setup for this device, it will work out of the box.

Some command line tools support more detailed features for this sensor like configuring the zones for the emoticon, changing display temperature between Celsius and Fahrenheit, and other more complex interactions.

This is sometimes advertised as a "Mija" or a "Mi Temp" device, but the page will usually mention "LYWSD03MMC" specifically if it's one of these.

{% include_relative _sensor_detail.md %}
