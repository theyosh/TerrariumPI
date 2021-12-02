---
title: Custom logging
categories: [Website, FAQ]
tags: [logging]
---

By default all logging is done in the folder log where the actual log files are written to a temporary memory share. This is done to reduce the write wear on the SD card. A downside is that when the Pi reboots, all log info of that day is gone. During the night, the log file will be archived and that is stored on the SD card. So archived log files will survive reboots.

In order to change the default logging of TerrariumPI you only need to create your own custom logging configuration file with the name `logging.custom.cfg` and place that in the `log` folder. So start with:

`cp logging.cfg log/logging.custom.cfg`

And start editing the `log/logging.custom.cfg` file with an editor. After editing restart TerrariumPI and the new logging will be loaded.

### Enable debug

In order to enable debug messages add the `fileHandlerDebug` handler to the `handlers` in section `[logger_root]`

### Syslog (local and remote)

In order to enable (remote) syslog logging add the `syslogHandler` handler to the `handlers` in section `[logger_root]`. Then you have to configure to use either the local syslog server or a remote syslog server. By default it uses the local syslog. To use remote change:

`'/dev/log' to ('hostip',portnr)`

Local: `args=('/dev/log','local6')`
Remote: `args=(('192.168.1.1',514),'local6')`

Next you need to tell Syslog which facility it is using. The default is `LOCAL6`. To enable this, create a file in the folder `/etc/rsyslog.d` for example:

`/etc/rsyslog.d/terrariumpi.conf`

And add then:

`local6.* /var/log/terrariumpi.log`

Finally restart rsyslog and you should receive log messages from TerrariumPI
