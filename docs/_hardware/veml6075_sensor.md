---
title: VEML6075 UVA and UVB light sensor
categories: [Hardware, Sensor]
tags: [sensor, uva, uvb, uvi]

image:
  src: /assets/img/VEML6075.webp
  alt: "VEML6075 UVA and UVB light sensor header image"

device_hardware : veml6075
device_types: [uva, uvb,uvi]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `0x44`"
device_url: https://pimylifeup.com/raspberry-pi-uv-sensor-veml6075/
---

## Information
This is a UV sensor module based on Vishay VEML6075 sensor, adopting individual UVA and UVB channel solution with 16-bit resolution. It can convert solar UV light intensity to digital data to provide an accurate measure of the signal strength.

VEML6075 UV sensor can give a reliable performance of UV radiation measurement under long time solar UV exposure. Furthermore, the sensor provides excellent temperature compensation capability within -40℃ to +85℃. VEML6075 features, low power consumption, and its minimum power can be as low as 800nA in shut-down mode. The operating voltage of the sensor ranges from 3.3V to 5V. It adopts IIC protocol, which can work well with any microcontroller that supports IIC.

Compatible with Arduino and Raspberry Pi, this sensor can be used in portable electronic product, wearable device, weather station, flame detecting and so on.

Specification
- Operating Voltage: 3.3V~5V
- Operating Current: 700uA
- Shut-down Mode: 10uA
- UV Chip: VEML6075
- Output: digital output
- Response Wavelength: UVB (λ0.5) within 315nm to 340nm; UVA (λ0.5) within 350nm to 375nm.
- Interface: PH2.0-4P
- IIC Address: 0x10
- Dimension: 22×30mm/0.87×1.18”
- Mount Hole Size: 3mm
- Mount Hole Pitch: 15mm
- Operating Temperature: -40℃~+85℃

**to get more accurate measurement, the sensor should direct to ultraviolet light source.**

{% include_relative _sensor_detail.md %}