---
title: Live Raspberry PI camera
categories: [Hardware, Webcam]
tags: [webcam, live, local, streaming]

image:
  path: /assets/img/RPI_webcam.webp
  src: /assets/img/RPI_webcam.webp
  alt: "Live Raspberry PI camera"

device_type: Live streaming
device_address: "Fixed to `rpicam`"
device_url: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera
---

## Information

You can use the official Raspberry PI camera module to setup a webcam.

Using as a live streaming webcam, the maximum resolution is: **1920** x **1080** pixels.

## Warning

You can only have **one** live streaming webcam. So when you add this type of webcam you **cannot** add another of this type. Also this will eliminate the use of the [USB live webcam]({% link _hardware/usb-live_webcam.md %}) as that is using the same hardware chip on the Raspberry PI.

{% include_relative _webcam_detail.md %}
