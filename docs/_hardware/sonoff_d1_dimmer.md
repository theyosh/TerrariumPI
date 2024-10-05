---
title: Sonoff D1 Dimmer (Tasmota/DIY)
categories: [Hardware, Relay]
tags: [relay, dimmer, wifi, sonoff, tasmota, diy]

image:
  path: /assets/img/Sonoff-D1-Dimmer.webp
  src: /assets/img/Sonoff-D1-Dimmer.webp
  alt: 'Sonoff D1 Dimmer (Tasmota) header image'

device_address: 'Enter the hostname or IP address including port number.'
device_url: https://sonoff.tech/product/smart-lighting/d1/
---

## Information

This is a dimmer device which can be controlled through Wifi. It can dim normal
as led lights at 100-240 Volt.

The device needs either to be flashed with [Tasmota](#tasmota), or you need it
yo put in [DIY](#diy-mode) mode.

When you add the Sonoff D1 Dimmer, TerrariumPI will automatically detect which
mode it should run.

### Tasmota

Total local control with quick setup and updates. Control using MQTT, Web UI,
HTTP or serial. Automate using timers, rules or scripts. Integration with home
automation solutions. Incredibly expandable and flexible.

[It needs to be flashed with Tasmota firmware!](https://notenoughtech.com/home-automation/tasmotizer/)

### DIY Mode

With the D1 Dimmer it is also possible to use the
[DIY mode](https://sonoff.tech/sonoff-diy-developer-documentation-d1-http-api/)
so you do not need to flash your device. This can be done with the original
software on the hardware device. But you need a
[433Mhz remote controller](https://sonoff.tech/product/accessories/rm433/) to
put the device in AP mode to setup your wifi.

[Follow these steps to setup your Sonoff D1 Dimmer in DIY mode](https://theroamingworkshop.cloud/b/en/1989/sonoff-d1-dimmer/#internet-connection)

{% include_relative _relay_detail.md %}
