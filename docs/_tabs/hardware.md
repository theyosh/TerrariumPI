---
title: Hardware
icon: fas fa-tools
order: 3
layout: post
toc: true

image:
  src: /assets/img/Hardware.webp
  width: 100%
  height: auto
  alt: Hardware header image
---

## GPIO
![Raspberry PI GPIO pins layout](/assets/img/GPIO-Pinout-Diagram.webp){: style="max-width: 200px" .right}
All the hardware that is connected through GPIO pins needs to use the physical pin number as address. This means a number from 1 - 40.

### Power saving
Some GPIO sensors can benefit from using power saving. A good example is the analog/digital moisture sensor YTXX - TODO: Make link to actual sensor

When you want to enable power saving, just enter an extra GPIO pin number to the address seperated by a comma.
<br />Ex: `[GPIO Readout pin],[GPIO power saving pin]`

### Analog sensors
![RaspIO Analog Zero](/assets/img/RasPiO-Analog-Zero.webp){: style="max-width: 200px" .right}
It is possible to add analog sensors to TerrariumPI. But as TerrariumPI only has digital GPIO ports, an extra add on is needed to add analog ports. For now the [RaspIO Analog Zero](https://rasp.io/analogzero/) is known to work. But any MCP3008 based board should work.

## I2C bus
By default there is only 1 I2C bus available. [But it is possible to add more I2C busses to your Raspberry PI](https://www.instructables.com/id/Raspberry-PI-Multiple-I2c-Devices/). To select a different I2C bus then 1, use the following address notation:<br />
`[I2C Address],[I2C Bus numer]`

For `[I2C Address]` you can use the number shown in the i2cdetect. Adding '**0x**' in front is allowed. So either **3c**, **3c,1**, **0x3c** and **0x3c,1** are valid and the same I2C addresses.

Run the command `i2cdetect -y 1` in order to see what is connected to your I2C bus. A correct working I2C bus should produce the following outcome:
```console
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: 70 -- -- -- -- -- -- --
```

## Relays
{% assign relays = site.hardware | where_exp: "relay", "relay.tags contains 'relay'" %}

We currently support <strong>{{ relays | size}}</strong> types of relays. Relays which has a dial icon ![Dimmer icon](/assets/img/dimmer_icon.png){: style="height: 20px" .normal} after their name are dimmers.

{% for relay in relays %}
  <h3>
    <a href="{{ relay.url | relative_url }}">{{ relay.title }}</a>
  {% if relay.tags contains 'dimmer' %}
    <img src="../assets/img/dimmer_icon.png" title="Relay is a dimmer" alt="Relay is a dimmer" style="height: 20px" class="ml-xl-3">
  {% endif %}
  </h3>
{% endfor %}


## Sensors

{% assign sensors = site.hardware | where_exp: "sensor", "sensor.tags contains 'sensor'" %}

We currently support <strong>{{ sensors | size}}</strong> types of sensors:
<br />

{% for sensor in sensors %}
  <h3>
    <a href="{{ sensor.url | relative_url }}">{{ sensor.title }}</a>
  </h3>
{% endfor %}
