---
title: MLX90614 IR Thermometer sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature]

image:
  src: /assets/img/mlx90614.webp
  alt: "MLX90614 IR Thermometer sensor header image"

device_types: [temperature]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) followed by either `,o` for object or `,a` for ambient temperature <br />Ex: `0x3f,1,o`"
device_url: https://www.sparkfun.com/products/9570
---

## Information
MLX90614 sensor is manufactured by Melexis Microelectronics Integrated system, it has two devices embedded in it, one is the infrared thermopile detector (sensing unit) and the other is a signal conditioning DSP device (computational unit). It works based on Stefan-Boltzmann law which states that all objects emits IR energy and the intensity of this energy will be directly proportional to the temperature of that object. The sensing unit in the sensor measures how much IR energy is emitted by a targeted object and the computational unit converts it into temperature value using a 17-bit in-built ADC and outputs the data through I2C communication protocol. The sensor measures both the object temperature and ambient temperature to calibrate the object temperature value. The features of MLX90614 sensor is given below, for more details refer the MLX90614 Datasheet.

Features:
- Operating Voltage: 3.6V to 5V
- Object Temperature Range: -70°C to 382.2°C
- Ambient Temperature Range: -40°C to 125°C
- Resolution/Accuracy: 0.02°C


{% include_relative _sensor_detail.md %}