---
title: How to debug TerrariumPI
categories: [Website, FAQ]
tags: [debug]
---

1. Stop the TerrariumPI service: `sudo service terrariumpi stop`.
2. Enter the TerrariumPI folder: `cd /home/pi/TerrariumPI/`
3. Enable Python3 virtual environment: `source venv/bin/activate`
4. Manual start TerrariumPI: `python terrariumPI.py`

This should start the TerrariumPI in console mode. So all errors should now be
visible to the console.

When the log line
`TerrariumPI 4.X.Y is up and running at address: http://0.0.0.0:8090 in XX.XX seconds`
appears, TerrariumPI is fully started and you can enter the web gui as normal.

When you are done debugging, you can press `Ctrl+C` once to stop TerrariumPI.

![TerrariumPI running in debug mode](/assets/img/TerrariumPIInDebugMode.webp)
