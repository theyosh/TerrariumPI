---
title: Script Sensor
categories: [Hardware, Sensor]
tags: [sensor, script, temperature, humidity,fertility,ph,uva,moisture,uvb,altitude,co2,distance,uvi,pressure,light]

image:
  path: /assets/img/script_sensor.webp
  src: /assets/img/script_sensor.webp
  alt: "Script sensor header image"

device_types: [temperature, humidity,fertility,ph,uva,moisture,uvb,altitude,co2,distance,uvi,pressure,light]
device_address: "Enter the full path to the script."
device_url: https://github.com/theyosh/TerrariumPI/blob/4.x.y.z/contrib/script_sensor.py
---

## Information

With a script sensor you can make your own script/program that does a measurement and give back the current value.

For temperature, it needs to return the value in Celsius degrees.

You can use decimal/float values. But make sure you have only a numeric value output. No '%' of 'C' indicators.

### Python scripts

In order to use the Python virtual environment with all its libraries, make sure you have the correct [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) line:

```bash
#!/usr/bin/env python
```

### Docker

When using docker, you can place them in the `scripts` volume that you have defined in the [docker-compose.yaml]({% link _tabs/install.md %}#docker) file. And then you can use the following address: `/TerrariumPI/scripts/[name_of_script].[extension]`

{% include_relative _sensor_detail.md %}
