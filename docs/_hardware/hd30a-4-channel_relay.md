---
title: HD30A 4 Channel Electromagnetic I2C Relay 12V 30A
categories: [Hardware, Relay]
tags: [relay, HD30A]

image:
  path: /assets/img/HD30A_4_Channel_Electromagnetic_I2C_Relay_12V_30A.webp
  src: /assets/img/HD30A_4_Channel_Electromagnetic_I2C_Relay_12V_30A.webp
  alt: "HD30A 4 Channel Electromagnetic I2C Relay 12V 30A header image"

device_hardware : GPIO
device_address: "Enter the IO Expender type, the relay number (starting at 1), and then the I2C address with optional I2C bus number: `pcf8574-1,0x4c,3`"
---

## Information

HD30A 4CH/8CH Channel Electromagnetic relay modules with I2C controlling interface HD30A 4CH/8CH Channel electromagnetic relay boards has been designed for
easy inductive and resistive high current load switching via I2C communication protocol. For wiring this board is needed only 4 wires - 2 wires with data lines SCL (serial clock) and SDA (serial data) and 2 wires with power supply VCC and GND. On board is special I2C slave address switch, which help to select board slave address. Total available eight slave addresses, therefor on one I2C line can be connected 8 relays modules. That mean user can control up to 64 relays separately. Please note, can’t be connected two board with the same addresses on the I2C line. All I2C slave addresses should be different. For the all available I2C slave addresses watch table below.

This HD30A 4CH/8CH channel I2C electromagnetic relay modules are fully compatible with any microcontroller (AVR, PIC, ARM, STM32), popular platform of Arduino and Raspberry, Wi-Fi ESP8266 and ESP32, and with other microcontrollers witch was I2C interface. I2C communication speed is up to 100kHz. Module power supply is 12.0V DC with integrated linear voltage regulators 3.3V and 5.0V. Power supply current should be at least 1000mA @ 12V.

In this module are used high quality electromagnetic relays Rayex/ZETTLER. These relays have SPDT switching terminals and can switch load current up to 30 Amps. Switching load voltage up to 240 Volts. For safe switching load wires connection are used quality screw terminals KF-128-3P. Each relay is indicated with led (color red)

[HD30A 4CH/8CH Channel Electromagnetic relay](https://www.tindie.com/products/bugrovs2012/hd30a-4-channel-electromagnetic-i2c-relay-12v-30a/)

{% include_relative _relay_detail.md %}
