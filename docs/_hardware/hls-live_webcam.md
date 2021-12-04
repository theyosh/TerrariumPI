---
title: Live HLS Stream
categories: [Hardware, Webcam]
tags: [webcam, live, remote, streaming]

image:
  path: /assets/img/HLS_Livestream.webp
  src: /assets/img/HLS_Livestream.webp
  alt: "Live HLS Stream"

device_type: Live streaming
device_address: "A HLS live stream master playlist<br />Ex: `https://stream.server.com/camera/live.m3u8`"
device_url: https://en.wikipedia.org/wiki/HTTP_Live_Streaming

---

## Information
If you have already a live stream running which is of the format [HLS](https://en.wikipedia.org/wiki/HTTP_Live_Streaming), you can use that as a webcam source. Just enter the full url to the m3u8 master playlist.

**Multi bitrate streams are not supported at the moment.**

{% include_relative _webcam_detail.md %}