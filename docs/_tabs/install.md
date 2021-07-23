---
title: Install
icon: fas fa-tools
order: 4

image:
  src: RaspberryPI_Logo.png
  width: 400   # in pixels
  height: 400   # in pixels
  alt: Raspberry PI Logo
---

Raspberry PI
============
![Raspberry PI Logo](assets/img/RaspberryPI_Logo.png){: .right }
In order to run TerrariumPI you first need a working Raspberry PI with the '[Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/)' image. This is very important, as the Desktop version will not work well with the GPIO pins.

Creating SD Card
----------------
Download and instal the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to prepare your SD card. Make sure you have a SD card of at least 4GB of size. Bigger is better :)

When the SD card is written, you can read/write the 'boot' partition. Add a file called 'ssh' to it. This will [enable SSH on a headless Raspberry Pi (add file to SD card on another machine)](https://www.raspberrypi.org/documentation/remote-access/ssh/).

