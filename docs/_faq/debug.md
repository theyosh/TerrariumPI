---
title: How to debug TerrariumPI
categories: [Website, FAQ]
tags: [debug]
permalink: /faq/:title/
---

1. Stop the terrariumpi service: `sudo service terrariumpi stop`.
2. Enter the TerrariumPI folder: `cd /home/pi/TerrariumPI/`
3. Enable Python3 virtual environment: `source venv/bin/activate`
4. Manual start TerrariumPI: `python terrariumPI.py`

This should start the TerrariumPI in console mode. So all errors should now be visible to the console.
