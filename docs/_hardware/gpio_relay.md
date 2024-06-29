---
title: GPIO
categories: [Hardware, Relay]
tags: [relay, gpio]

image:
  path: /assets/img/GPIO_Relay.webp
  src: /assets/img/GPIO_Relay.webp
  alt: "GPIO Relays header image"

device_hardware : GPIO devices
device_address: "Enter the [physical pin](/TerrariumPI/hardware/#gpio) number on which the device is connected<br />Ex: `27`<br />Or when used with an [IO expander](/TerrariumPI/hardware/io-expander/):<br />Ex:`pcf8574-9,0x4c,3`"
---

## Information

This X-channel relay interface board can control various appliances and other equipments with high current. It can be controlled directly by any micro-controller.

### Inverse mode

When the relay is working in **reverse** order, you can change this by toggling the `inverse` toggle in the `calibration` tab.

{% include_relative _relay_detail.md %}
