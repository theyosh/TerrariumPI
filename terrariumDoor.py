# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import RPi.GPIO as GPIO
import thread

from gevent import monkey, sleep
monkey.patch_all()

class terrariumDoor():

  def __init__(self, gpio_pin, callback = None):
    ## set GPIO mode to BCM
    ## this takes GPIO number instead of pin number
    logger.debug('Setting terrariumPI GPIO Mode to %s' % (GPIO.BOARD,))
    GPIO.setmode(GPIO.BOARD)
    logger.debug('Done setting terrariumPI GPIO Mode to %s' % (GPIO.BOARD,))

    self.door_status = None
    self.callback = callback
    logger.debug('Setting terrariumPI door to pi %s' % (gpio_pin,))
    self.set_gpio_pin(gpio_pin)
    logger.debug('Done setting terrariumPI door to pi %s' % (gpio_pin,))

    # Add detetion with callback !!!!THIS WILL CRASH THE GEVENT LOOP SOMEHOW!!!!!!
    # GPIO.add_event_detect(gpio_pin, GPIO.BOTH, callback=callback, bouncetime=300)
    thread.start_new_thread(self.__checker, ())

  def __checker(self):
    logger.info('Start terrariumPI door checker')
    while True:
      current_status = 'open' if GPIO.input(self.gpio_pin) else 'closed'
      logger.debug('Current terrariumPI door status: %s' % (current_status,))
      if current_status != self.door_status:
        logger.info('Door terrariumPI changed from %s to %s' % (self.door_status, current_status))
        self.door_status = current_status
        self.callback(True)

      sleep(0.5)

  def set_gpio_pin(self,gpio_pin):
    self.gpio_pin = int(gpio_pin)
    ## use the built-in pull-up resistor
    GPIO.setup(self.gpio_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)  # activate input with PullUp

  def get_status(self):
    return self.door_status

  def is_open(self):
    return self.door_status == 'open'

  def is_closed(self):
    return self.door_status == 'closed'
