---
title: LED-Warrior18
categories: [Hardware, Relay]
tags: [relay, dimmer, LED-Warrior18, LED]

image:
  path: /assets/img/lw18.webp
  src: /assets/img/lw18.webp
  alt: "LED-Warrior18 dimmer header image"

device_address: "&lt;relay_number&gt;,&lt;I2C Address&gt;,[I2C Bus] where the [I2C bus](/TerrariumPI/hardware#i2c-bus) is optional<br />Ex: `1,0x70`"
dimmer_frequency: 65535
device_url : https://shop.codemercs.com/en/led-warrior18-module.html
---

## Information

The LED-Warrior18 is a LED driver with I2C interface and two separate channels that can be controlled independently.
Due to the I2C interface it can be controlled with all common I2C hosts (e.g. Arduino, ESP32 or Raspberry Pi). The power supply of the LED-Warrior18 is done via the I2C interface. The output side can be operated with a voltage between 5.5 and 40V DC and max. 4A per channel.

The LED-Warrior18 can be equipped with screw terminals on the output side as well as with a 1x4 pin header for the I2C interface (screw terminals and pin header not included).

All further information about the product can be found on the [product page](https://codemercs.com/en/led-lighting/driver-with-i2c-interface).
Software and sample programs for the LED-Warrior18 can be downloaded from our [Github repository](https://github.com/codemercs-com/lw18).

### Technical Details - LED-Warrior18

- I2C to dual PWM LED driver
- PWM output at 730 Hz
- 2 x 16 bit PWM ranging from 0.001% to 100%
- 8 Bit data to log mapping
- Synch mode for controlling multiple units
- Default power on status programmable
- Programmable period length for higher frequency/lower resolution
- Minimal external circuitry
- 5 V supply
- Measurement: 35mm x 25mm

{% include_relative _relay_detail.md %}
