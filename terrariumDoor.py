# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import RPi.GPIO as GPIO
import thread
from hashlib import md5
from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumDoor():
  VALID_HARDWARE_TYPES = ['gpio']
  CHECKER_TIMEOUT = 0.5

  CLOSED = 'closed'
  OPEN = 'open'

  def __init__(self, id, hardware_type, address, name = '', callback = None):
    self.id = id
    self.callback = callback

    self.set_hardware_type(hardware_type)
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
    except Exception:
      logger.exception('Error in door \'%s\' with message:' % (self.get_name(),))
      self.set_status(terrariumDoor.CLOSED)
      if self.callback is not None:
        self.callback(self.get_data())

  def __checker(self):
    logger.info('Start terrariumPI door checker for door \'%s\'' % self.get_name())
    while True:
      if self.get_hardware_type() == 'gpio':
        current_status = terrariumDoor.OPEN if GPIO.input(terrariumUtils.to_BCM_port_number(self.get_address())) else terrariumDoor.CLOSED

      logger.debug('Current door \'%s\' status: %s' % (self.get_name(),current_status))
      if current_status != self.get_status():
        logger.info('Door \'%s\' changed from %s to %s' % (self.get_name(),self.get_status(), current_status))
        self.set_status(current_status)
        if self.callback is not None:
          self.callback(self.get_data())

      sleep(terrariumDoor.CHECKER_TIMEOUT)

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
    if type in terrariumDoor.VALID_HARDWARE_TYPES:
      self.hardwaretype = type

  def get_address(self):
    return self.address

  def set_address(self,address):
    self.address = address
    GPIO.setup(terrariumUtils.to_BCM_port_number(address),GPIO.IN,pull_up_down=GPIO.PUD_UP)  # activate input with PullUp

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
