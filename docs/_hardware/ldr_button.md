---
title: Light sensor
categories: [Hardware, Button]
tags: [button, ldr, light]

image:
  path: /assets/img/ldr.webp
  src: /assets/img/ldr.webp
  alt: "Light sensor header image"

calibration: true
device_address: "Enter the [physical pin](/TerrariumPI/hardware/#gpio) number where the data is connected<br />Ex: `27`"
device_url: https://www.ryansouthgate.com/2015/08/10/raspberry-pi-door-sensor/
---

## Information
LDR is a sensor that lets electrons flow through it when it is exposed to enough light. When there is enough light, the electrons start flowing into the capacitor. The capacitor will start charging, and when the voltage across the capacitor goes above 2.1 V, the input pin of the GPIO will read HIGH. At that point, the program will set the output pin to LOW, which will turn the LED OFF. On the other hand, when there is not enough light out, the electrons stop flowing through the LDR, and the capacitor starts discharging. When the voltage across the capacitor drops below 2.1 V, the input pin reads LOW.

It is possible to use different [capacitors](https://qkzeetech.com/wp-content/uploads/2019/02/1uF-50V.jpg). The value can be entered in the calibration part of the button. A lower value means faster response.

{% include_relative _button_detail.md %}