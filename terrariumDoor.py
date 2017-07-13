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
  valid_hardware_types = ['gpio']

  CLOSED = 'closed'
  OPEN = 'open'

  def __init__(self, id, hardware_type, address, name = '', callback = None):
    ## set GPIO mode to BOARD
    ## this takes the pin number instead of GPIO mapping pin
    logger.debug('Setting terrariumPI GPIO Mode to %s' % (GPIO.BOARD,))
    GPIO.setmode(GPIO.BOARD)
    logger.debug('Done setting terrariumPI GPIO Mode to %s' % (GPIO.BOARD,))

    self.id = id
    self.callback = callback

    self.set_hardware_type(hardware_type)

    if self.get_hardware_type() == 'gpio':
      pass

    self.set_address(address)
    self.set_name(name)

    if self.id is None:
      self.id = md5(b'' + self.get_hardware_type() + self.get_address()).hexdigest()

    # Set door closed
    self.set_status(terrariumDoor.CLOSED)

    logger.info('Loaded door \'%s\' on %s %s with status %s' % (self.get_name(),self.get_hardware_type(), self.get_address(), self.get_status()))

    try:
      # Add detetion with callback !!!!THIS WILL CRASH THE GEVENT LOOP SOMEHOW!!!!!!
      # GPIO.add_event_detect(gpio_pin, GPIO.BOTH, callback=callback, bouncetime=300)
      thread.start_new_thread(self.__checker, ())
    except Exception, err:
      logger.error('Error in door \'%s\' with message: %s' % (self.get_name(),err))
      self.set_status(terrariumDoor.CLOSED)
      if self.callback is not None:
        self.callback(self.get_data(), True)

  def __checker(self):
    logger.info('Start terrariumPI door checker for door \'%s\'' % self.get_name())
    while True:
      current_status = terrariumDoor.OPEN if GPIO.input(int(self.get_address())) else terrariumDoor.CLOSED
      logger.debug('Current door \'%s\' status: %s' % (self.get_name(),current_status))
      if current_status != self.get_status():
        logger.info('Door \'%s\' changed from %s to %s' % (self.get_name(),self.get_status(), current_status))
        self.set_status(current_status)
        if self.callback is not None:
          self.callback(self.get_data(),True)

      sleep(0.5)

  def get_data(self):
    return {'id': self.get_id(),
            'hardwaretype': self.get_hardware_type(),
            'address': self.get_address(),
            'name': self.get_name(),
            'state': self.get_status()
            }

  def get_id(self):
    return self.id

  def get_hardware_type(self):
    return self.hardwaretype

  def set_hardware_type(self,type):
    if type in terrariumDoor.valid_hardware_types:
      self.hardwaretype = type

  def get_address(self):
    return self.address

  def set_address(self,address):
    self.address = address
    GPIO.setup(int(address),GPIO.IN,pull_up_down=GPIO.PUD_UP)  # activate input with PullUp

  def get_name(self):
    return self.name

  def set_name(self,name):
    self.name = name

  def get_status(self):
    return self.door_status

  def set_status(self,status):
    if status in [terrariumDoor.OPEN,terrariumDoor.CLOSED]:
      self.door_status = status

  def is_open(self):
    return self.door_status == terrariumDoor.OPEN

  def is_closed(self):
    return self.door_status == terrariumDoor.CLOSED
