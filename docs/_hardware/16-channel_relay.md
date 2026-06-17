---
title: 16 Channel I2C Electromagnetic Relay Module IoT
categories: [Hardware, Relay]
tags: [relay, i2c, 16channel]

image:
  path: /assets/img/16 Channel I2C Electromagnetic Relay Module PCF8575.webp
  src: /assets/img/16 Channel I2C Electromagnetic Relay Module PCF8575.webp
  alt: '16 Channel I2C Electromagnetic Relay Module PCF8575 header image'

device_hardware: GPIO
device_address:
  'Enter the IO Expender type, the relay number (starting at 1), and then the
  I2C address with optional I2C bus number: `pcf8575-1,0x27,3`'
---

<!-- prettier-ignore-start -->
> In order to use this board with a Raspberry PI you need a logic level shifter! See [connecting topic](#connecting-to-the-pi)
{: .prompt-warning }
<!-- prettier-ignore-end -->

## Information

The IOT Electronic 16 Channel I2C Solid State Relay Module provides 16 isolated
channels for Arduino and Raspberry projects, supporting 100-240V AC control.

This IOT Electronic 16 Channel I2C Solid State Relay Module offers robust
control for your microcontroller projects. Designed for compatibility with
Arduino, Raspberry, and other microcontrollers, it provides 16 isolated solid
state relay channels.

### Key Features

- Control 16 independent channels using an I2C interface.
- Built around the efficient **PCF8575** I2C expander chip.
- Designed for compatibility with Arduino, Raspberry, and various
  microcontrollers.

### Device Specifications

- PCB Board Dimension: 210mm x 72mm
- Compatibility: DRG-01 DIN rail plastic holder
- Isolation: Full opto and air isolation from high voltage
- Operation DC Voltage: 3.3V and 5.0V
- Maximum Current @5.0V: 450mA
- AC Controlling Voltage Range: 100…240VAC
- AC Voltage Frequency Range: 50…60Hz
- Minimum AC Current per Channel: 30mA
- Maximum AC Current per Channel: 2A
- I2C Device Slave Address: Changeable
- Expandability: Connect up to 8 devices to one I2C bus, controlling up to 128
  channels
- Indicators: Red LED indicators for each SSR relay channel

This versatile relay module simplifies projects requiring multiple high-voltage
switching capabilities. Its I2C interface allows for easy integration and
expansion, enabling control of up to 128 channels with multiple modules. The
opto and air isolation ensure safety and reliability when dealing with AC loads
up to 240V, making the IOT Electronic 16 Channel I2C Solid State Relay Module an
excellent choice for demanding applications.

### Ideal for

- Makers and hobbyists working with Arduino and Raspberry Pi.
- Automation projects requiring multi-channel AC switching.
- Industrial control applications needing isolated relay outputs.
- Projects where space-saving and expandability are crucial.
- Electronics enthusiasts building custom control systems.

[16 Channel I2C Electromagnetic Relay Module PCF8575](https://www.tindie.com/products/bugrovs2012/16-channel-i2c-electromagnetic-relay-module-iot/#product-description)

### Connecting to the PI

![Logic level converter](/assets/img/logic-level-converter.webp){: .right
width="150" } In order to use this board stable, you need to use a
`logic level shifter`. Just search for it, and you will find some. As the
[3.3 volt bus](https://pinout.xyz/pinout/3v3_power) of the Raspberry PI is not
powerful enough the power the board.

1. Connect the I2C bus from the Pi to the lower voltage side of the level
   shifter by using 2 channels. And use the 3.3 volt from the Raspberry PI as LV
   of the lower voltage side and use any ground pin.
2. Than connect the relay board to the logic level shifter. Use the opposite
   connectors of the low side part. So that two channels are used on both sides.
   And connect the power and ground in the high voltage side.
3. The final step is to connect the board on the other side (green screw
   terminal) to a 5 volt power source. This can just be the
   [5 volt bus](https://pinout.xyz/pinout/5v_power) of the Raspberry PI. Or use
   an external power source. Without this, the board will fail after toggling 3
   relays on.

{% include_relative _relay_detail.md %}
