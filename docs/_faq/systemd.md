---
title: How to start/stop/restart and disable/enable TerrariumPI
categories: [Website, FAQ]
tags: [systemd, service]
permalink: /faq/:title/
---
TerrariumPI is using systemd for startup. Here you can find the commands to manually start, stop or restart it. Also there is an option to disable or enable TerrariumPI at bootup.

### Start
run `sudo service terrariumpi start` to start TerrariumPI

### Stop
run `sudo service terrariumpi stop` to stop TerrariumPI

### Restart
run `sudo service terrariumpi restart` to restart TerrariumPI

### Eanble startup
run `sudo systemctl enable terrariumpi` to enable TerrariumPI at startup

### Disable startup
run `sudo systemctl disable terrariumpi` to disable TerrariumPI at startup