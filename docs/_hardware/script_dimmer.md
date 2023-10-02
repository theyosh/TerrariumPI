---
title: Script dimmer
categories: [Hardware, Relay]
tags: [relay, dimmer, script]

image:
  path: /assets/img/Code.webp
  src: /assets/img/Code.webp
  alt: "Script dimmer (API)"

device_address: /home/user/location/executable/script
---

## Information

This is a script dimmer which can be used to support a not supported dimmer. TerrariumPI will execute this script with no parameters when it tries to read the current dimmer state. And when you change the dimmer, the script will get an extra parameter which is a int from 0 - 100. Where 0 is off and 100 is fully on.

When for what reason the readout is not possible, return the value '-1' when requested. This will tell TerrariumPI to keep the last existing value.

An example can be found in the [contrib](https://github.com/theyosh/TerrariumPI/blob/4.x.y.z/contrib/external_switch.py) folder.

### Python scripts

In order to use the Python virtual environment with all its libraries, make sure you have the correct [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) line:

```bash
#!/usr/bin/env python
```

### Docker

When using docker, you can place them in the `scripts` volume that you have defined in the [docker-compose.yaml]({% link _tabs/install.md %}#docker) file. And then you can use the following address: `/TerrariumPI/scripts/[name_of_script].[extension]`

{% include_relative _relay_detail.md %}
