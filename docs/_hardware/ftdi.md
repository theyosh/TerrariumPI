---
title: FTDI
categories: [Hardware, Relay]
tags: [relay, ftdi]
permalink: /hardware/relay/:title/

image:
  src: /assets/img/FTDI.webp
  width: 75%
  height: auto
  alt: "FTDI header image"

device_type : FTDI
device_address: "Enter the relay number from 1 - 4. Optional add the serial of the board seperated by a comma.<br />Ex: `1,A702JH8H`"
device_auto_detect: true
device_url : http://denkovi.com/usb-relay-board-four-channels-for-home-automation
---

## Information
This is Four Channel relay board controlled by computer USB port. The usb relay board is with 4 SPDT relays rated up to 10A each. You may control devices 220V / 120V (up to 4) directly with one such relay unit. It is fully powered by the computer USB port. Suitable for home automation applications, hobby projects, industrial automation. The free software DRM and DRMv3 allows to control relays manually, create timers (weekly and calendar) and multivibrators, use date and time for alarms. We developed also command line tool utility for controlling the relays. We provide software examples in Labview, .NET, Java, Borland C++, Python.

{% include_relative _relay_detail.md %}