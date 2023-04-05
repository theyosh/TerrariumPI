---
title: AM2320 Sensor
categories: [Hardware, Sensor]
tags: [sensor, i2c]

image:
  path: /assets/img/am2320.webp
  src: /assets/img/am2320.webp
  alt: "AM2320 header image"

device_types: [temperature,humidity]
device_address: "&lt;I2C Address&gt;,[I2C Bus] where the [I2C bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `0x5c`"
device_url: http://www.pibits.net/code/am2320-temperature-and-humidity-sensor-and-raspberry-pi-example.php
---

## Information

This little sensor looks an awful lot like the popular DHT11/DHT22 temperature and humidity sensors, but unlike classic DHT sensors, it has an I2C interface! That's right, you do not need to use a bit-bang timing-specific protocol to talk to the AM2320, it uses plain-old-I2C. Whew, that makes things a little easier, doesn't it?

But! We'll let you know, this sensor is not well documented like our other, fancier I2C temperature & humidity sensors. The data sheet mentions it has 3% humidity accuracy and 0.5C temperature accuracy, but we're not very trusting of the specifications. So, while this sensor does seem to work, it's not recommended for anything where you care about any sort of guaranteed accuracy. Temperature is probably correct to 2-3 degrees Celsius. Humidity is probably within 5-10%.

![AM2320 schema](/assets/img/am2320-schema.webp)
_AM2320 schema_

{% include_relative _sensor_detail.md %}
