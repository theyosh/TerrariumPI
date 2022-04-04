---
title: Motion sensor
categories: [Hardware, Button]
tags: [button, motion]

image:
  path: /assets/img/motion.webp
  src: /assets/img/motion.webp
  alt: "Motion sensor header image"

device_address: "Enter the [physical pin](/TerrariumPI/hardware/#gpio) number on which the device is connected<br />Ex: `27`<br />Or when used with an [IO expander](/TerrariumPI/hardware/io-expander/) use format: pcf857[4/5]-[IO-expander-port],[I2C_address],[I2C_buss] where I2C_buss is optional<br />Ex:`pcf8575-9,0x4c,3`"
device_url: https://tutorials-raspberrypi.com/connect-and-control-raspberry-pi-motion-detector-pir/
---

## Information

Due to its design, the PIR motion sensor module is very easy to use because it already has the components installed. Raspberry Pi motion detectors in home automation and/or outdoor applications (as a classic outdoor motion detector) are easier than ever to implement.

This Arduino/Raspberry Pi motion sensor responds and moves, with the "strength" of movement controlled by an adjustable resistor (potentiometer). So you can set the motion sensor very sensitive, or try to avoid "noise". As soon as something moves, a signal is sent that can be received and responded by the Raspberry Pi.

{% include_relative _button_detail.md %}
