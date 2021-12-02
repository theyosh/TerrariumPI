---
title: Script relay
categories: [Hardware, Relay]
tags: [relay, script]

image:
  path: /assets/img/Code.webp
  src: /assets/img/Code.webp
  alt: "Script relay (API)"

device_address: /home/user/location/executable/script
---

## Information
This is a script relay which can be used to support a not supported relay. TerrariumPI will execute this script with no parameters when it tries to read the current relay state. And when you change the dimmer, the script will get an extra parameter which is a int from 0 - 100. Where 0 is off and 100 is fully on.

When for what reason the readout is not possible, return the value '-1' when requested. This will tell TerrariumPI to keep the last existing value.

An example can be found in the [contrib](https://github.com/theyosh/TerrariumPI/blob/4.x.y.z/contrib/external_switch.py) folder

{% include_relative _relay_detail.md %}