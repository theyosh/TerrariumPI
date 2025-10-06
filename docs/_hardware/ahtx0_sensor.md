---
title: AHTx0 Sensor
categories: [Hardware, Sensor]
tags: [sensor, i2c]

image:
  path: /assets/img/ahtX0-sensor.webp
  src: /assets/img/ahtX0-sensor.webp
  alt: 'AHTx0 header image'

device_types: [temperature, humidity]
device_address:
  '&lt;I2C Address&gt;,[I2C Bus] where the [I2C
  bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `0x38`'
device_power_management: false
---

## Information

The AHT20 is a nice but inexpensive temperature and humidity sensor from the
same folks that brought us the DHT22. You can take sensor readings as often as
you like, and it uses standard I2C so its super easy to use with any Arduino or
Linux/Raspberry Pi board.

This sensor has a typical accuracy of +- 2% relative humidity, and +-0.3 °C at
20-80% RH and 20-60 °C. There is only one I2C address so it's not a good option
when you need multiple humidity sensors.

Both AHT10 and AHT20 are supported.

### Specifications

- Use with 3.3V or 5V power/logic
- I2C address 0x38
- Operational Temperature range: -40 to 85 °C (+-1 °C typical accuracy over
  entire range)
- Operational Relative Humidity range: 0 to 100 RH% (+-3 % typical accuracy over
  entire range)

{% include_relative _sensor_detail.md %}
