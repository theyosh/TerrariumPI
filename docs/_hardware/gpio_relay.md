---
title: GPIO
categories: [Hardware, Relay]
tags: [relay, gpio]

image:
  path: /assets/img/GPIO_Relay.webp
  src: /assets/img/GPIO_Relay.webp
  alt: "GPIO Relays header image"

device_hardware : GPIO devices
device_address: "Enter the [physical pin](/TerrariumPI/hardware/#gpio) number on which the device is connected<br />Ex: `27`<br />Or when used with an [IO expander](/TerrariumPI/hardware/io-expander/) use format: pcf857[4/5]-[IO-expander-port],[I2C_address],[I2C_buss] where I2C_buss is optional<br />Ex:`pcf8575-9,0x4c,3`"
#device_url : https://shop.meross.com/collections/smart-power-strip
---

## Information

This 4-channel relay interface board can control various appliances and other equipments with high current. It can be controlled directly by any micro-controller.

{% include_relative _relay_detail.md %}
