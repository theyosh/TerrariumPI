---
title: AM2302
categories: [Hardware, Sensor]
tags: [sensor, gpio]
permalink: /hardware/sensor/:title/

image:
  src: /assets/img/am2302.webp
  alt: "AM2302 header image"

device_hardware : AM2302
device_types: [temperature,humidity]
device_address: "Enter the [physical pin](/hardware/#gpio) number where the data is connected<br />Ex: `27`"
device_power_management: true
---

## Information
The AM2302 is a wired version of the DHT22, in a large plastic body. It is a basic, low-cost digital temperature and humidity sensor. It uses a capacitive humidity sensor and a thermistor to measure the surrounding air, and spits out a digital signal on the data pin (no analog input pins needed). Its fairly simple to use, but requires careful timing to grab data. The only real downside of this sensor is you can only get new data from it once every 2 seconds, so when using our library, sensor readings can be up to 2 seconds old.

Simply connect the red 3-5V power, the yellow wire to your data input pin and the black wire to ground. Although it uses a single-wire to send data it is not Dallas One Wire compatible! If you want multiple sensors, each one must have its own data pin.

**There is a 5.1K resistor inside the sensor connecting VCC and DATA so you do not need any additional pullup resistors**

**remark:** From experience, this sensor is not very stable after a few days.

{% include_relative _sensor_detail.md %}