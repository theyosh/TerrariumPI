---
title: BH1750 LUX light sensor
categories: [Hardware, Sensor]
tags: [sensor, light]

image:
  src: /assets/img/bh1750.webp
  alt: "BH1750 LUX light sensor header image"

device_types: [light]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `0x3f`"
device_url: https://components101.com/sensors/bh1750-ambient-light-sensor
---

## Information
The BH1750 is a light intensity sensor that can be used to adjust the brightness of display in mobiles and LCD displays. It can also be used to turn the headlights of cars on/off based on the outdoor lighting. The sensor uses I2C communication protocol so that makes it super easy to use with microcontrollers. The SCL and SDA pins are for I2C.

There is no calculation needed to measure the LUX value because the sensor directly gives the lux value. Actually, it measures the intensity according to the amount of light hitting on it. It operates on voltage range of 2.4V-3.6V and consumes really small current of 0.12mA. The results of the sensor does not depends upon the light source used and the influence of IR radiation is very less. There are very less chances of any error because the variation in measurement is as low as +/-20%.

{% include_relative _sensor_detail.md %}