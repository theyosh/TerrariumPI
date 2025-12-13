---
title: Kasa Smart
categories: [Hardware, Relay]
tags: [relay, kasa]

image:
  path: /assets/img/Kasa_Smart.webp
  src: /assets/img/Kasa_Smart.webp
  alt: 'Kasa Smart header image'

device_address:
  'Enter the hostname or IP address and optional a relay number separated by a
  comma.<br />Ex: `192.168.1.15,1`'
device_auto_detect: true
device_url: https://www.kasasmart.com/
---

## Authentication

In order to make the Kasa hardware able to communicate with TerrariumPI, you
need to enable **Third-Party Compatibility** feature. Else you will get
authentication errors when trying to use the relays.

Read more about
[Third-Party Compatibility feature](https://www.tp-link.com/us/support/faq/4416/)
of Kasa and how to enable it.

## Information

{% include_relative _relay_detail.md %}
