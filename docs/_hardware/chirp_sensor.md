---
title: Chirp sensor
categories: [Hardware, Sensor]
tags: [sensor, temperature, moisture]

image:
  path: /assets/img/chirp.webp
  src: /assets/img/chirp.webp
  alt: "Chirp sensor header image"

device_types: [temperature, moisture]
device_address: "[I2C Address](/TerrariumPI/hardware#i2c-bus) <br />Ex: `0x3f`"
device_url: https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/
---

## Information

Chirp is a plant watering alarm - as simple as that. You put it into the soil near a plant and it emits a tiny chirp when the soil is dry, reminding you to water the plant. Chirp uses capacitive humidity sensing as opposed to resistive humidity sensing, this means, it does not make an electric contact with the soil, avoiding electrode corrosion and soil electrolysis and resulting in better accuracy and longer battery life.

## Calibration

To be able to retrieve the moisture in percent you need to calibrate the sensor. The minimum moist and maximum moist values need to be defined. If these values are not adjusted properly for every individual sensor, the value for moisture might go below 0% and above 100%

You can use chirp.py to help calibrating your sensors.

```bash
cd /home/pi/TerrariumPI
source venv/bin/activate
cd 3rdparty/chirp-rpi
python chirpy.py
```

Leave the dry sensor in dry air for a while so that the lowest value is recorded.

Then put the sensor in water so that it records the highest value.

The chirp.py program will automatically print out the highest and lowest value recorded when Ctrl-C is pressed.

Use these values for **minimum moist value** and **maximum moist value** in the calibration settings.

Please note that these values might drift a little with temperature changes. Make the calibration in the environment that you intend to use the sensor.

{% include_relative _sensor_detail.md %}
