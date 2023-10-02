---
title: Hardware
icon: fas fa-microchip
order: 3

image:
  path: /assets/img/Hardware.webp
  src: /assets/img/Hardware.webp
  alt: Hardware header image
---
## GPIO

![Raspberry PI GPIO pins layout](/assets/img/GPIO-Pinout-Diagram.webp){: style="max-width: 200px" .right}
All the hardware that is connected through GPIO pins needs to use the **physical pin number** as address. This means a number from 1 - 40.

### Power saving

Some GPIO sensors can benefit from using power saving. A good example is the analog/digital moisture sensor [YTXX]({% link _hardware/ylxx-digital_sensor.md %})

Power management works that you connect the red (power) wire of the sensor to a GPIO pin, which will be put to high so that the sensor get powered. After 1.0 sec a measurement is taken, and afterwards the power to the sensor is shutdown.

When you want to enable power saving just enter an extra GPIO pin number, where the RED power cable is connected to, to the address separated by a comma.\
Ex: `[GPIO Readout pin],[GPIO power saving pin]`

**remark:** Not all sensors will work with power management.

### Analog sensors

![RaspIO Analog Zero](/assets/img/RasPiO-Analog-Zero.webp){: style="max-width: 200px" .right}
It is possible to add analog sensors to TerrariumPI. But as TerrariumPI only has digital GPIO ports, an extra add-on is needed to add analog ports. For now the [RaspIO Analog Zero](https://rasp.io/analogzero/) is known to work. But any MCP3008 based board should work. The downside is that you will miss some GPIO pins for other use.

## I2C bus

By default there is only 1 I2C bus available. [But it is possible to add more I2C busses to your Raspberry PI](https://www.instructables.com/id/Raspberry-PI-Multiple-I2c-Devices/). To select a different I2C bus then 1, use the following address notation:\
`<I2C Address>,[I2C Bus number]`

`<I2C Address>` is mandatory and you can use the number shown in the i2cdetect. Adding '**0x**' in front is allowed. So either **3c**, **3c,1**, **0x3c** and **0x3c,1** are valid and the same I2C addresses.

The `[I2C Bus number]` is optional and can be omitted. The default value is 1.

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

### I2C Multiplexer

With an [I2C multiplexer](/TerrariumPI/hardware/i2c-multiplexer/) you can add more I2C busses to TerrariumPI. Support for I2C multiplexers depends on the support in the OS. For now there is support for pca9542 (2 channel), pca9545 (4 channel), and pca9548 (8 channel) muxes.

### I2C IO Expander

There is support for two I2C IO Expanders so you can have extra GPIO relays or GPIO buttons if needed. This will update the GPIO address to:\
`pcf857<4/5>-<IO expander port>,<I2C Address>,[I2C Bus number]`

Either use [pcf857**4**](/TerrariumPI/hardware/io-expander/) or [pcf857**5**](/TerrariumPI/hardware/io-expander/) to select the used IO expander.

`<IO expander port>` is mandatory and is a number from 0 till max ports - 1.

`<I2C Address>` is mandatory and specified [here](#i2c-bus).

{% assign relays = site.hardware | where_exp: "hardware", "hardware.tags contains 'relay'" | sort_natural: "title" %}

## Relays

We currently support **{{ relays | size}}** types of relays. Relays which has a dial icon ![Dimmer icon](/assets/img/dimmer_icon.png){: style="height: 20px" .normal .is_dimmer} after their name are dimmers.

{% for relay in relays %}
  <h3 id="{{ relay.title| slugify }}">
    <a href="{{ relay.url | relative_url }}">{{ relay.title }}</a>
  {% if relay.tags contains 'dimmer' %}
    <img src="/assets/img/dimmer_icon.png" title="Relay is a dimmer" alt="Relay is a dimmer" style="height: 20px" class="ml-xl-3 is_dimmer">
  {% endif %}
  </h3>
{% endfor %}

{% assign sensors = site.hardware | where_exp: "hardware", "hardware.tags contains 'sensor'" | sort_natural: "title" %}
{% assign measurements = sensors | map: "device_types" | join: "," | split: "," | uniq | sort_natural | join: "`, `"  %}

## Sensors

We currently support **{{ sensors | size}}** hardware types of sensors, measuring `{{ measurements }}`:

{% for sensor in sensors %}
{% assign types = sensor.device_types | sort_natural | join: ", " %}
  <h3 style="margin-bottom: 0px"  id="{{ sensor.title| slugify }}">
    <a href="{{ sensor.url | relative_url }}">{{ sensor.title }}</a>
  </h3>
  {{ types }}

{% endfor %}

{% assign buttons = site.hardware | where_exp: "hardware", "hardware.tags contains 'button'" | sort_natural: "title" %}

## Buttons

We currently support **{{ buttons | size}}** types of buttons.

{% for button in buttons %}
  <h3 id="{{ button.title| slugify }}">
    <a href="{{ button.url | relative_url }}">{{ button.title }}</a>
  </h3>
{% endfor %}

{% assign webcams = site.hardware | where_exp: "hardware", "hardware.tags contains 'webcam'" | sort_natural: "title" %}

## Webcams

We currently support **{{ webcams | size}}** types of webcams.

{% for webcam in webcams %}
  <h3 style="margin-bottom: 0px" id="{{ webcam.title| slugify }}">
    <a href="{{ webcam.url | relative_url }}">{{ webcam.title }}</a>
  </h3>
  {{ webcam.device_type }}
{% endfor %}
