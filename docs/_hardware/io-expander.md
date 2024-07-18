---
title: IO Expander
categories: [Hardware, Button, I2C]
tags: [button, expander, pcf8574]
permalink: /hardware/io-expander/

image:
  path: /assets/img/pcf8574_IO_expander.webp
  src: /assets/img/pcf8574_IO_expander.webp
  alt: 'PCF8574 IO Expander'
---

With the IO expander pcf8574 you can add more GPIO [relays](/TerrariumPI/hardware/#relays) and [buttons](/TerrariumPI/hardware/#buttons) to TerrariumPI. This IO expander does only support on/off actions. So it is not possible to use this IO expander with a DHT sensor. You cannot read out the extra GPIO ports.

## Addressing

In order to use this IO expander, enter the following address in the GPIO relay or button address field.\
`pcf8574-<IO expander port>,<I2C Address>,[I2C Bus number]`

`<IO expander port>` is mandatory and is a number from 1 till max ports.

`<I2C Address>` is mandatory and specified [here](/TerrariumPI/hardware/#i2c-bus).
