---
title: IO Expander
categories: [Hardware, Button, I2C]
tags: [button, expander]
permalink: /hardware/io-expander/

image:
  path: /assets/img/pcf857X_IO_expander.webp
  src: /assets/img/pcf857X_IO_expander.webp
  alt: "PCF8574 IO Expander"

---

With the IO expander pcf8574 and pcf8575 you can add more GPIO [relays](/TerrariumPI/hardware/#relays) and [buttons](/TerrariumPI/hardware/#buttons) to TerrariumPI. This IO expander does only support on/off actions. So it is not possible to use this IO expander with a DHT sensor. You cannot read out the extra GPIO ports.

## Addressing

In order to use this IO expander, enter the following address in the GPIO relay or button address field.\
`pcf857<4/5>-<IO expander port>,<I2C Address>,[I2C Bus number]`

Either use pcf857**4** or pcf857**5** to select the used IO expander.

`<IO expander port>` is mandatory and is a number from 0 till max ports - 1.

`<I2C Address>` is mandatory and specified [here](/TerrariumPI/hardware/#i2c-bus).

## PCF8574

This is a 8 ports IO expander. The yellow on the image.

## PCF8575

This is a 16 ports IO expander. The right blue board on the image.
