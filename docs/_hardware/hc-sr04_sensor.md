---
title: HC-SR04 ultrasonic ranging sensor
categories: [Hardware, Sensor]
tags: [sensor, distance]

image:
  src: /assets/img/hc-sr04.webp
  alt: "HC-SR04 ultrasonic ranging sensor header image"

device_types: [distance]
device_address: "Enter the [physical pin](/TerrariumPI/hardware/#gpio) number where the `trigger` and `echo` pins are connected in that order<br />Ex: `27,23`"
device_url: https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
---

## Information
This is the HC-SR04 ultrasonic distance sensor. This economical sensor provides 2cm to 400cm of non-contact measurement functionality with a ranging accuracy that can reach up to 3mm. Each HC-SR04 module includes an ultrasonic transmitter, a receiver and a control circuit.

There are only four pins that you need to worry about on the HC-SR04: VCC (Power), Trig (Trigger), Echo (Receive), and GND (Ground). You will find this sensor very easy to set up and use for your next range-finding project!

![SR04 Connect diagram](/assets/img/SR04-connect.webp){: .right width="200" }

This sensor has additional control circuitry that can prevent inconsistent "bouncy" data depending on the application.

For a Raspberry PI it needs resistors on the `ECHO` port.

{% include_relative _sensor_detail.md %}