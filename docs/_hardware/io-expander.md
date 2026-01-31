---
title: IO Expander
categories: [Hardware, Button, I2C]
tags: [button, expander, pcf8574, pcf8575]
permalink: /hardware/io-expander/

image:
  path: /assets/img/pcf8574_IO_expander.webp
  src: /assets/img/pcf8574_IO_expander.webp
  alt: 'PCF8574 IO Expander'
---

With the IO expander pcf8574/5 you can add more GPIO
[relays]({% link _tabs/hardware.md %}#relays) and
[buttons]({% link _tabs/hardware.md %}#buttons) to TerrariumPI. This IO expander
does only support on/off actions. So it is not possible to use this IO expander
with a DHT sensor. You cannot read out the extra GPIO ports.

## PCF8575 Bug

At the moment it is **not** possible to use a pcf8575 IO expander to add more
buttons. Due to a
[bug in the used library](https://github.com/rp3tya/PCF8575/issues/5), we can
only support [relays]({% link _tabs/hardware.md %}#relays) with this IO
expander.

## Addressing

In order to use this IO expander, enter the following address in the GPIO relay
or button address field.\
`pcf857[4/5]-<IO expander port>,<I2C Address>,[I2C Bus number]`

`<IO expander port>` is mandatory and is a number from **1** till max ports.

`<I2C Address>` is mandatory and specified
[here]({% link _tabs/hardware.md %}#i2c-bus).
