---
title: Script relay
categories: [Hardware, Relay]
tags: [relay, script]

image:
  path: /assets/img/Code.webp
  src: /assets/img/Code.webp
  alt: "Script relay (API)"

device_address: /home/user/location/executable/script
---

## Information

This is a script relay which can be used to support a not supported relay. TerrariumPI will execute this script with no parameters when it tries to read the current relay state. And when you change the dimmer in the GUI, the script will get an extra parameter which is a int from 0 - 100. Where 0 is off and 100 is fully on.

A single on/off relay will get the value 100 for on and 0 for off.

When for what reason the readout is not possible, return the value '-1' when requested. This will tell TerrariumPI to keep the last existing value.

And make sure your script is [executable](https://linuxhandbook.com/make-file-executable/). You can use the same Python libraries that are installed. See the `requirements.txt` for installed libraries.

An example can be found in the [contrib](https://github.com/theyosh/TerrariumPI/blob/main/contrib/external_switch.py) folder.

### Python scripts

In order to use the Python virtual environment with all its libraries, make sure you have the correct [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) line:

```bash
#!/usr/bin/env python
```


### Docker

When using docker, you can place them in the `scripts` volume that you have defined in the [docker-compose.yaml]({% link _tabs/install.md %}#docker) file. And then you can use the following address: `/TerrariumPI/scripts/[name_of_script].[extension]`

{% include_relative _relay_detail.md %}
