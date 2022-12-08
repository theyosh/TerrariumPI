---
title: Remote Button
categories: [Hardware, Button]
tags: [button, remote, json, temperature, humidity,fertility,ph,uva,moisture,uvb,altitude,co2,distance,uvi,pressure,light]

image:
  path: /assets/img/remote_sensor.webp
  src: /assets/img/remote_sensor.webp
  alt: "Remote sensor header image"

device_types: [button, door]
device_address: "Enter the full url and json path traversal. More information at [remote hardware](/TerrariumPI/faq/how-to-use-remote-data/)."
device_url: /TerrariumPI/faq/how-to-use-remote-data/
---

## Information

With the remote button you can use an external source for button actions or door usage. This needs to be a [JSON](https://nl.wikipedia.org/wiki/JSON) source. As this is a button sensor, which is normally polled about 10 times a second, there is an extra timeout in requesting the data from the remote source. So these remote buttons will react slower than physical buttons.

By using JSON path traversal in the url after the `#` sign, you can specify which value to use from the JSON data.

The value `0` will be threated as off or door closed. Any other numeric value above 0 will threated as pressed or door open. If you cannot control the remote source there is an option to inverse the value in the calibration part.

### Calibration

At the calibration section you can set the timeout between checks in seconds and if the remote value needs to be reversed.

{% include_relative _button_detail.md %}
