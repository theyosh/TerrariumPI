---
title: Live RTSP camera
categories: [Hardware, Webcam]
tags: [webcam, live, streaming, rtsp]

image:
  path: /assets/img/rtspcam.webp
  src: /assets/img/rtspcam.webp
  alt: "RTSP Live camera"

device_type: Live streaming
device_address: "Enter the device rtsp url<br />Ex: `rtsp://server.lan/stream`"
---

## Information

Any RTSP camera can be used. It will try to transcode through the video GPU to a HLS live stream

{% include_relative _webcam_detail.md %}
