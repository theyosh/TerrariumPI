# -*- coding: utf-8 -*-
'''
Install extra modules:
aptitude install python-dateutil python-ow python-rpi.gpio python-psutil python-pip
pip install gevent untangle uptime bottle bottle_websocket

'''
import logging
import logging.config
logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('terrariumPI')

logger.info('Starting terrariumPI')
from terrariumEngine import terrariumEngine
from terrariumWebserver import terrariumWebserver

if __name__  == "__main__":
  logger.debug('Starting terrariumPI engine')
  terrariumEngine = terrariumEngine()
  logger.debug('Started terrariumPI engine')

  logger.debug('Starting terrariumPI webserver')
  terrariumWebserver = terrariumWebserver(terrariumEngine)
  logger.debug('Started terrariumPI webserver')
  terrariumWebserver.start()
  logger.info('Stopping terrariumPI')
