---
title: AMG8833 Grid-Eye IR Thermometer sensor
categories: [Hardware, Sensor]
tags: [sensor, IR]

image:
  src: /assets/img/amg8833.webp
  alt: "AMG8833 Grid-Eye IR Thermometer sensor header image"

device_hardware : amg8833
device_types: [temperature]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `0x3f`"
device_url: https://makersportal.com/shop/amg8833-thermal-camera-infrared-array
---

## Information
The AMG8833 is a 64-pixel temperature sensor developed by Panasonic under the Grid-EYE® product line. The sensor contains an 8x8 array of infrared thermopiles, which approximate the temperature by measuring the infrared radiation being emitted from emissive bodies. The Grid-EYE communicates via the I2C bus, which also makes it compatible with Raspberry Pi and Arduino right out of the box.

The AMG8833 contains an onboard lens that limits the viewing angle of the sensor to 60-degrees, which results in a sensing region useful for objects in the mid-field (as opposed to far-field or near-field). It also operates at 3.3V and 5V, at a sample rate of 1Hz-10Hz, with an approximate temperature resolution of 0.25°C over a range of 0°C to 80°C.

The AMG8833 is useful for applications in thermal imaging, heat transfer analyses, human temperature monitoring, heating and air condition management, industrial control, and other applications in non-contact temperature measurement.

{% include_relative _sensor_detail.md %}