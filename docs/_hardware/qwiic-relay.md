---
title: Qwiic Relay
categories: [Hardware, Relay]
tags: [relay, i2c]

image:
  src: /assets/img/Qwiic_Relay.jpg
  alt: "Qwiic Relays header image"

device_address: "[relay_number],[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `1,0x3f`"
device_url : https://www.sparkfun.com/search/results?term=Qwiic+relay
---

## Information

Qwiic Relays are available in different configurations:

* Single relay
* Quad relay
* Dual Solid State relay
* Quad Solid State rekay

These relays are addressable through I2C and can be controlled by any micro-controller with I2C support.
This allows to control various appliances.

{% include_relative _relay_detail.md %}
