---
title: Denkovi V2
categories: [Hardware]
tags: [relay]
permalink: /hardware/relay/:title/

image:
  src: /assets/img/Denkovi_V2_X_sockets.png
  width: 600   # in pixels
  height: 200   # in pixels
  alt: image alternative text

device_type : Denkovi Relay v2 (X sockets)
device_address: "Enter the relay number 1 - X. Optional you can enter the Serial address of the board if you have multiple relay boards like: 1,0035685"
---

## Information
The second version of our popular USB 4 Relay Board with several improvements. It comes with MCP2200 chipset, 4 SPDT Relays each rated with up to 10A, relays states saving in internal EEPROM and improved USB interference resistance. Suitable for home automation applications, hobby projects, industrial automation. The free DRM / DRMv3 software allows to control relays manually, create timers (weekly and calendar) and multivibrators, use date and time for alarms. We have developed and tool for control from command line. We provide various software examples.

[Denkovi Assembly Electronics ltd.](https://denkovi.com/usb-relay-board-four-channels-for-home-automation-v2)

## Installation
As the license of Denkovi does not allow to ship their command line tool with my software. Therefore you have to download and install it manually.

Make sure you have Java installed:
```console
sudo apt install openjdk-11-jre-headless
```

Download the Denkovi Command line tool from: [https://denkovi.com/denkovi-relay-command-line-tool](https://denkovi.com/denkovi-relay-command-line-tool) and unpack it into the directory `3rdparty/DenkoviRelayCommandLineTool/`.
Then either rename the jar file to DenkoviRelayCommandLineTool.jar or make a symlink to it.

The software expects the following file to exists: `3rdparty/DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar` from the root TerrariumPI directory.

{% include_relative _relay_detail.md %}