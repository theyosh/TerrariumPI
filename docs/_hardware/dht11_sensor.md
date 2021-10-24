---
title: DHT11 sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, humidity]
permalink: /hardware/sensor/:title/

image:
  src: /assets/img/dht11.webp
  alt: "DHT11 sensor header image"

device_hardware : dht11
device_types: [temperature, humidity]
device_address: "Enter the [physical pin](/TerrariumPI/hardware/#gpio) number where the data is connected<br />Ex: `27`"
device_url: https://www.adafruit.com/product/386
---

## Information
The DHT11 is a basic, ultra low-cost digital temperature and humidity sensor. It uses a capacitive humidity sensor and a thermistor to measure the surrounding air and spits out a digital signal on the data pin (no analog input pins needed). It's fairly simple to use but requires careful timing to grab data. The only real downside of this sensor is you can only get new data from it once every 2 seconds, so when using our library, sensor readings can be up to 2 seconds old.

Compared to the DHT22, this sensor is less precise, less accurate, and works in a smaller range of temperature/humidity, but its smaller and less expensive

It needs a 4.7K - 10K resistor, which you will want to use as a pullup from the data pin to VCC.

## Warning
As these sensors are cheap, they are not stable for 24/7 duty. After a few days they tend to give problems. Use at your own risk! [Using DHT11 / DHT11 on Raspberry Pi 4b #470](https://github.com/theyosh/TerrariumPI/issues/470)

{% include_relative _sensor_detail.md %}