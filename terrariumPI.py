# -*- coding: utf-8 -*-
__version__ = '4.6.1'

from gevent import monkey
monkey.patch_all()

import gettext
gettext.install('terrariumpi', 'locales/')

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from terrariumEngine import terrariumEngine

if __name__  == "__main__":
  terrariumEngine = terrariumEngine(__version__)
  # This keeps running until CTRL-C is entered or given
  terrariumEngine.stop()
