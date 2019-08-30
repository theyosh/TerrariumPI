# -*- coding: utf-8 -*-
from gevent import monkey, sleep
monkey.patch_all()

import os
BASEDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASEDIR)

# https://untangle.readthedocs.io/en/latest/#encoding
try:
  # This is python2 only...
  import sys
  reload(sys) # just to be sure
  sys.setdefaultencoding('utf-8')
except Exception as ex:
  pass

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
  logger.info('Shutdown terrariumPI done. Bye bye ...')
