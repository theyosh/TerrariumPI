---
title: IRF520 Dimmer
categories: [Hardware, Relay]
tags: [relay, dimmer]
permalink: /hardware/relay/:title/

image:
  src: /assets/img/Mosfet_Dimmer.png
  width: 1000   # in pixels
  height: 400   # in pixels
  alt: image alternative text

device_type : IRF520 Dimmer
device_address: Physical GPIO pin number 1 - 40
dimmer_frequency: 1000
---

## Information
This little module is a breakout board for the IFR520 MOSFET transistor. The module is designed to switch heavy DC loads from a single digital pin of your microcontroller. Its main purpose is to provide a low cost way to drive a DC motor for robotics applications, but the module can be used to control most high current DC loads. Screw terminals are provided to interface to your load and external power source. An LED indicator provides a visual indication of when your load is being switched.

[Please check our quick start and FAQ for more information.](https://hobbycomponents.com/motor-drivers/661-irf520-mosfet-driver-module)

{% include_relative _relay_detail.md %}