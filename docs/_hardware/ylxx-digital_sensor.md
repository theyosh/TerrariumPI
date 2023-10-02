---
title: YL-69 sensor (digital)
categories: [Hardware, Sensor]
tags: [sensor, moisture]

image:
  path: /assets/img/YL-69.webp
  src: /assets/img/YL-69.webp
  alt: "YL-69 sensor (digital) header image"

device_types: [moisture]
device_address: "Enter the [physical pin](/TerrariumPI/hardware/#gpio) number on which the device is connected<br />Ex: `27`"
device_url: https://www.techcoil.com/blog/how-to-read-soil-moisture-level-with-raspberry-pi-and-a-yl-69-fc-28-moisture-sensor/
device_power_management: true
---

## Information

Soil moisture module is most sensitive to the ambient humidity is generally used to detect the moisture content of the soil. Module to reach the threshold value is set in the soil moisture, DO port output high, when the the soil humidity exceeds a set threshold value, the module D0 output low.

The digital output D0 can be connected directly with the micro-controller to detect high and low by the micro-controller to detect soil moisture.
The digital outputs DO shop relay module can directly drive the buzzer module, which can form a soil moisture alarm equipment.
Analog output AO and AD module connected through the AD converter, you can get more precise values of soil moisture.

This sensor can operate longer, when [Power management]({% link _tabs/hardware.md %}#power-saving). is used for this sensor.

### Features

- Brand new and high quality
- This is a simple water sensor, which can be used to detect soil moisture
- Dual output mode, analog output is accurate
- A fixed bolt hole for easy installation
- With power indicator (red) and digital switching output indicator (green)
- LM393 comparator chip, stable

### Specifications

- VCC: 3.3V-5V
- GND: GND
- DO: digital output interface(0 and 1)
- AO: analog output interface
- Panel PCB Dimension: 3 x 1.5 cm
- Soil Probe Dimension: 6 x 2 cm

{% include_relative _sensor_detail.md %}
