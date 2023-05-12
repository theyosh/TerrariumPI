---
title: USB camera
categories: [Hardware, Webcam]
tags: [webcam, live, picture]

image:
  path: /assets/img/USB_Webcam.webp
  src: /assets/img/USB_Webcam.webp
  alt: "USB camera"

device_type: Still picture
device_address: "Enter the device path<br />Ex: `/dev/video0`"
---

## Information

Use any USB webcam that is supported by Linux.

## Controls

As this is a Video4Linux device, you can use `v4l2-ctl` tools to control the focus, white balance and other options. This is not possible with the TerrariumPI software. [A good website with more information and how to use it](https://www.kurokesu.com/main/2016/01/16/manual-usb-camera-settings-in-linux/).

{% include_relative _webcam_detail.md %}
