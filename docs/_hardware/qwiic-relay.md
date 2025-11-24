---
title: Qwiic Relay
categories: [Hardware, Relay]
tags: [relay, i2c]

image:
  path: /assets/img/Qwiic_Relay.webp
  src: /assets/img/Qwiic_Relay.webp
  alt: "Qwiic Relays header image"

device_address: "&lt;I2C Address&gt;,[I2C Bus] where the [I2C
  bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `1,0x3f`"
device_url: https://www.sparkfun.com/search/results?term=Qwiic+relay
---

## Information

Qwiic Relays are available in different configurations:

- Single relay
- Quad relay
- Dual Solid State relay
- Quad Solid State relay

These relays are addressable through I2C and can be controlled by any
micro-controller with I2C support. This allows to control various appliances.

### Power issues

There are some reports that the Qwiic relays only works with a 5volt power
despite it should be able to run on 7-12 volt. So if the device is not working,
try switching to 5 volts.

{% include_relative _relay_detail.md %}
