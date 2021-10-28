---
title: Remote Sensor
categories: [Hardware, Sensor]
tags: [sensor, remote, json, temperature, humidity,fertility,ph,uva,moisture,uvb,altitude,co2,distance,uvi,pressure,light]

image:
  src: /assets/img/remote_sensor.webp
  alt: "Remote sensor header image"

device_hardware : Remote Sensor
device_types: [temperature, humidity,fertility,ph,uva,moisture,uvb,altitude,co2,distance,uvi,pressure,light]
device_address: "Enter the full url and json path traversal. More information at [remote hardware](/TerrariumPI/faq/how-to-use-remote-data/)."
device_url: /TerrariumPI/faq/how-to-use-remote-data/
---

## Information
With the remote sensor you can use an external source for measurements. This needs to be a [JSON](https://nl.wikipedia.org/wiki/JSON) source. And the remote source needs to be able to serve the data once every 30 seconds. So make sure you will not hit any rate limits on the remote source.

By using JSON path traversal in the url after the `#` sign, you can specifiy which value to use from the JSON data.


{% include_relative _sensor_detail.md %}