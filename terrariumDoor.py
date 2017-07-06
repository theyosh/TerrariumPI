# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import RPi.GPIO as GPIO
import thread

from time import time
from hashlib import md5
from gevent import monkey, sleep
monkey.patch_all()

class terrariumDoor():

  def __init__(self, id = None, gpio_pin = 0, name = '', callback = None):
    ## set GPIO mode to BCM
    ## this takes GPIO number instead of pin number
    logger.debug('Setting terrariumPI GPIO Mode to %s' % (GPIO.BOARD,))
    GPIO.setmode(GPIO.BOARD)
    logger.debug('Done setting terrariumPI GPIO Mode to %s' % (GPIO.BOARD,))

    self.id = None
    self.name = None
    self.gpio_pin = None
    self.callback = callback
    self.door_status = None

    logger.debug('Setting terrariumPI door to pin %s' % (gpio_pin,))
    try:
      if id is None:
        self.id = md5(b'' + str(int(gpio_pin))).hexdigest()
      else:
        self.id = id

      self.set_gpio_pin(gpio_pin)
      self.set_name(name)
      logger.debug('Done setting terrariumPI door (%s) to pin %s' % (name,gpio_pin,))
      # Add detetion with callback !!!!THIS WILL CRASH THE GEVENT LOOP SOMEHOW!!!!!!
      # GPIO.add_event_detect(gpio_pin, GPIO.BOTH, callback=callback, bouncetime=300)
      thread.start_new_thread(self.__checker, ())
    except Exception:
      logger.error('Door pin %s for %s is not available. Doorsensor is disabled' % (gpio_pin,name))
      self.door_status = 'closed'
      if self.callback is not None:
        self.callback(self.get_data(), True)

  def __checker(self):
    logger.info('Start terrariumPI door checker')
    while True:
      current_status = 'open' if GPIO.input(self.gpio_pin) else 'closed'
      logger.debug('Current terrariumPI door status: %s' % (current_status,))
      if current_status != self.door_status:
        logger.info('Door terrariumPI changed from %s to %s' % (self.door_status, current_status))
        self.door_status = current_status
        if self.callback is not None:
          self.callback(self.get_data(),True)

      sleep(0.5)

  def set_gpio_pin(self,gpio_pin):
    self.gpio_pin = int(gpio_pin)
    ## use the built-in pull-up resistor
    GPIO.setup(self.gpio_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)  # activate input with PullUp

  def get_data(self):
    return {'id': self.get_id(),
            'gpiopin': self.get_gpio_pin(),
            'name': self.get_name(),
            'state': self.get_status()
            }

  def get_id(self):
    return self.id

  def get_name(self):
    return self.name

  def set_name(self,name):
    self.name = name

  def get_gpio_pin(self):
    return self.gpio_pin

  def get_status(self):
    return self.door_status

  def is_open(self):
    return self.door_status == 'open'

  def is_closed(self):
    return self.door_status == 'closed'
