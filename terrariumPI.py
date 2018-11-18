# -*- coding: utf-8 -*-
# https://untangle.readthedocs.io/en/latest/#encoding
try:
  # This is python2 only...
  import sys
  reload(sys) # just to be sure
  sys.setdefaultencoding('utf-8')
except Exception as ex:
  pass

'''
Install extra modules:
aptitude install python-dateutil python-ow python-rpi.gpio python-psutil python-pip
pip install gevent untangle uptime bottle bottle_websocket

'''
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from terrariumEngine import terrariumEngine
from terrariumWebserver import terrariumWebserver
logger.info('Starting terrariumPI')

if __name__  == "__main__":
  logger.debug('Starting terrariumPI engine')
  terrariumEngine = terrariumEngine()
  logger.debug('Started terrariumPI engine')
  logger.debug('Starting terrariumPI webserver')
  terrariumWebserver = terrariumWebserver(terrariumEngine)
  logger.debug('Started terrariumPI webserver')
  terrariumWebserver.start()
  logger.info('Stopping terrariumPI')
  terrariumEngine.stop()
  logger.info('Shutdown terrariumPI')
