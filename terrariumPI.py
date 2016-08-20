# -*- coding: utf-8 -*-
'''
Install extra modules:
aptitude install python-dateutil python-ow python-rpi.gpio python-psutil
pip install gevent untangle uptime bottle bottle_websocket

'''

from terrariumEngine import terrariumEngine
from terrariumWebserver import terrariumWebserver

if __name__  == "__main__":
  terrariumEngine = terrariumEngine()
  terrariumWebserver = terrariumWebserver(terrariumEngine)
  terrariumWebserver.start()
