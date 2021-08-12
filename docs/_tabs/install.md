---
title: Install
icon: fas fa-tools
order: 4
toc: true
layout: post

# image:
#   src: ../assets/img/RaspberryPI_Logo.png
#   width: 400   # in pixels
#   height: 400   # in pixels
#  alt: Raspberry PI Logo
---

Here we will install Raspberry PI and TerrariumPI software step by step.

# Raspberry PI

![Raspberry PI Logo](/assets/img/RaspberryPI_Logo.webp){: .right width="200" }
In order to run TerrariumPI you first need a working Raspberry PI with the '[Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/)' image. This is very important, as the Desktop version will not work well with the GPIO pins.

## Creating SD Card

![Raspberry PI Imager](/assets/img/RPI_Imager.webp){: .right width="200" }
Download and instal the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to prepare your SD card. Make sure you have a SD card of at least 4GB of size. Bigger is better :)

When the SD card is written, you can read/write the 'boot' partition. Add a file called 'ssh' to it. This will [enable SSH on a headless Raspberry Pi (add file to SD card on another machine)](https://www.raspberrypi.org/documentation/remote-access/ssh/).

Put your SD card in the Pi and power it up.

# TerrariumPI

When the Raspberry PI is up and running, you should be able to SSH to it. On Linux and Mac you can use the terminal. For Windows, you can use Putty.

```console
ssh pi@[raspberrypi]
```

## Prerequisites

First we need to install Git. This is used to download the software from Github.com

```console
sudo apt -y install git
```

## Download

After Git is installed, we can download the Terrariumpi source code. We will only download the latest version.

```console
git clone --branch 4.x.y.z --depth 1 https://github.com/theyosh/TerrariumPI.git
```

## Installation

And the final step is to start the installer. This will guide you through the installation process.

The first time you run the installer, it will also update the Raspberry PI OS to the latest version. This can take some more time.

```console
cd TerrariumPI
sudo ./install.sh
```

After the installation is done, reboot once and you should be able to access TerrariumPI on the url `http://[raspberrypi]:8090`. [Continue with the setup]({{ 'setup' | relative_url}})

# Migration V3 to V4

If you have an existing version 3 running, and you want to upgrade/migrate to version 4, here are the steps that are needed.

1. First make sure you have an backup of files of the old V3 version:
  - settings.cfg
  - history.db

2. Then install V4 as describe above. Then setup the relays and sensors as you had on V3. The last step is to run a small script that will copy the relay history data from V3 to V4. This is the only data to migrate. As this will keep the total used power and water correct.