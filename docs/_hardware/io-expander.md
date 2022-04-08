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

With the IO expander pcf8574 and pcf8575 you can add more GPIO relays and buttons to TerrariumPI. The address will then be changed to first pcf857X where X is either 4 or 5. Then a dash and the port number. Make sure you do not go above the max number. Then a comma and the I2C address with optional the I2C bus.

## PCF8574

This is a 8 ports IO expander. The yellow on the image.

## PCF8575

This is a 16 ports IO expander. The right blue board on the image.