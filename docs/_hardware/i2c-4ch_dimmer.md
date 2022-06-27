---
title: I2C 4Channels LED AC dimmer
categories: [Hardware, Relay]
tags: [relay, dimmer, i2c, ac mains]

image:
  path: /assets/img/i2c_4ch-dimmer.webp
  src: /assets/img/i2c_4ch-dimmer.webp
  alt: "I2C 4Channels LED AC Dimmer header image"

device_address: "&lt;relay_number&gt;,&lt;I2C Address&gt;,[I2C Bus] where the [I2C bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `1,0x70`"
device_url : https://www.tindie.com/products/bugrovs2012/i2c-4ch-ac-led-dimmer-module/
---

## Information

Only 4 wires are needed to control this board !

With this module, you can control the intensity of incandescent lamps, LED dimmable bulbs, power heating elements or fan speed controlled through a micro controller or Arduino/Raspberry boards.

Compatible with any Arduino, Raspberry or micro controller.

- Dimming method - leading edge
- Working voltage - 110 or 240 VAC
- Current per channel - up to 3A
- Compatible with 50Hz and 60Hz AC Line
- AC Line autodetect function
- PCB dimensions - 140mm x 60mm
- Distance between holes: vertical 51mm, horizontal 131mm
- Mounting holes diameter: 3.2mm
- 100kHz I2C bus interface
- I2C bus pull up switch on board
- I2C device address select switch on board
- Can be connected up to 8 devices on I2C bus (8 devices x 4 = 32 channels!!!)
- 50HZ LED - show detected AC 50HZ Line
- 60HZ LED - show detected AC 60HZ Line
- BOTH LED Flashing - AC Line not detected

{% include_relative _relay_detail.md %}
