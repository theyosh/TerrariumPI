---
title: DimmerLink (I2C mode)
categories: [Hardware, Relay]
tags: [relay, dimmer, i2c, ac mains]

image:
  path: /assets/img/DimmerLink.webp
  src: /assets/img/DimmerLink.webp
  alt: 'I2C DimmerLink header image'

device_address:
  '&lt;relay_number&gt;,&lt;I2C Address&gt;,[I2C Bus] where the [I2C
  bus](/TerrariumPI/hardware/#i2c-bus) is optional<br />Ex: `1,0x70`'
device_url: https://www.rbdimmer.com/shop/dimmerlink-controller-uart-i2c-interface-for-ac-dimmers-48
---

<!-- prettier-ignore-start -->
> By default the DimmerLink comes in UART mode. You need to [switch to I2C](https://www.rbdimmer.com/blog/faq-9/dimmerlink-not-detected-on-i2c-uart-mode-default-issue-32) first!! Read carefully about how to connect, especially voltage!!
{: .prompt-warning }
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
> Only **1-channel** devices are supported!
{: .prompt-warning }
<!-- prettier-ignore-end -->

## Information

Stop fighting with dimmer libraries. DimmerLink is a tiny plug-and-play
controller that handles all the complex TRIAC timing for you. Just send simple
commands over UART or I2C — the DimmerLink controller does the rest.

Every maker knows the pain: you integrate an AC dimmer library into your
project, and suddenly your lights flicker, your timing breaks, and you spend
hours debugging interrupt conflicts. The DimmerLink eliminates this entirely by
offloading all timing-critical operations to a dedicated Cortex-M+ micro
controller.

## Works with

![Desktop View](https://www.rbdimmer.com/web/image/product.product/133/image_1024/AC%20Dimmer%20Module%204A%2C%201%20channel%2C%203.3V-5V%20logic%2C%20AC%20400V-4A%20%28Standard%20%28phase%20control%29%29?unique=9faff9b){:
width="200" .right} This module is tested with a single channel
[AC dimmer of RobotDyn](https://www.rbdimmer.com/shop/ac-dimmer-module-4a-1-channel-3-3v-5v-logic-ac-400v-4a-6)

## How it works

Connect DimmerLink between your MCU (Arduino, ESP32, Raspberry Pi, or any micro
controller) and your AC dimmer module. Send a 3-byte command like "SET 50%" over
UART or write to an I2C register. The controller handles zero-cross detection,
phase angle calculation, and TRIAC triggering with microsecond precision. No
libraries to install. No interrupts to configure. No conflicts with your
existing code.

## Key features

- Zero flickering - hardware-based timing, immune to software delays
- Universal interface - UART (115200 baud) or I2C (address 0x50)
- Wide voltage range - works with 1.8V, 3.3V, and 5V logic levels
- Ultra-compact - only 18×12mm, fits anywhere
- Multiple dimming curves - Linear, RMS, Logarithmic
- Auto frequency detection - works with 50Hz and 60Hz mains

{% include_relative _relay_detail.md %}
