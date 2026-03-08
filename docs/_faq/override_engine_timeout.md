---
title: Override engine timeout
categories: [Website, FAQ]
tags: [engine, override, advanced]
---

**Warning** This is an advanced setting override, and therefore make sure what
you are doing!! **Warning**

By default the TerrariumPI Engine is updating its state every 30 seconds. This
also means that relays are only triggered every 30 seconds. This can mean that a
relay is turned at max 29 seconds to late. As the previous run was 1 second
before the time schedule.

Keep in mind that sensor read outs will still be cached for 30 seconds. So new
sensor data will only available every 30 seconds.

This value can be overridden to set it at a lower value.

## Manual

1. Create the folder 'terrariumpi.service.d':
   `sudo mkdir -p /etc/systemd/system/terrariumpi.service.d/`
2. Create a file called 'override.conf' with the following contents:
   `sudo nano /etc/systemd/system/terrariumpi.service.d/override.conf` \

```
[Service]
Environment="TPI_ENGINE_TIMEOUT=15"
```

for a TerrariumPI Engine timeout of **15** seconds 3. Reload systemd daemon:
`sudo systemctl daemon-reload` 4. Restart TerrariumPI:
`sudo service terrariumpi restart`

## Docker

Edit the docker compose file and add the environment variable
`TPI_ENGINE_TIMEOUT: 15`

```
services:
  terrariumpi:
    environment:
      TPI_ENGINE_TIMEOUT: 15
```
