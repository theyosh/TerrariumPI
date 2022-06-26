---
title: I2C Multiplexer
categories: [Hardware, I2C]
tags: [pca9548, i2c, multiplexer]
permalink: /hardware/i2c-multiplexer/

image:
  path: /assets/img/pca9548.webp
  src: /assets/img/pca9548.webp
  alt: "pca9548 I2C Multiplexer"

---

With this I2C multiplexer you can add multiple I2C buses that can hold multiple sensors and or relays. This makes it also possible to use multiple sensors with the same I2C address, but connecting them to different buses.

In order to use this multiplexer, you have to connect it to the first I2C bus, which is normally [GPIO pin 3 and 5](https://pinout.xyz/pinout/i2c#) and then add an extra config line to `/boot/config.txt`. Put the following line below the line: `dtparam=i2c_arm=on`:

`dtoverlay=i2c-mux,pca9548,addr=0x70` (addr defaults to 0x70 so can be omitted if using that address).

After rebooting, you should have up to 8 new I2C devices at the location: `/dev/i2c-*`. [You can then use the I2C address as normal but you need to add the I2C bus](/TerrariumPI/hardware/#i2c-bus).

This should work for **pca9542** (2 channel), **pca9545** (4 channel), and **pca9548** (8 channel) devices.

More info: [#705](https://github.com/theyosh/TerrariumPI/issues/705#issuecomment-1159766743) and thanks to [@Dragonfly-terra](https://github.com/Dragonfly-terra)
