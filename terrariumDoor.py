# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import RPi.GPIO as GPIO
try:
  import thread as _thread
except ImportError as ex:
  import _thread
import time

from hashlib import md5
from gevent import sleep

from terrariumUtils import terrariumUtils

class terrariumDoor(object):
  VALID_HARDWARE_TYPES = ['gpio','remote']
  CHECKER_TIMEOUT = 0.25
  REMOTE_TIMEOUT = 30

  CLOSED = 'closed'
  OPEN = 'open'

  def __init__(self, id, hardware_type, address, name = '', callback = None):
    self.id = id
    self.callback = callback

    self.set_hardware_type(hardware_type)
    self.set_address(address)
    self.set_name(name)

    self.__last_check = 0
    self.__run = True

    if self.id is None:
      self.id = md5((self.get_hardware_type() + self.get_address()).encode()).hexdigest()

    # Set door closed
    self.set_status(terrariumDoor.CLOSED)

    logger.info('Loaded door \'%s\' on %s %s with status %s' % (self.get_name(),self.get_hardware_type(), self.get_address(), self.get_status()))

    try:
      # Add detetion with callback !!!!THIS WILL CRASH THE GEVENT LOOP SOMEHOW!!!!!!
      # New problem: SQLlite threads restrictions... :(
      # GPIO.add_event_detect(terrariumUtils.to_BCM_port_number(address), GPIO.BOTH, callback=self.__bla, bouncetime=300)
      _thread.start_new_thread(self.__checker, ())
    except Exception:
      logger.exception('Error in door \'%s\' with message:' % (self.get_name(),))
      self.set_status(terrariumDoor.CLOSED)
      if self.callback is not None:
        self.callback(self.get_data())

  def __checker(self):
    logger.info('Start terrariumPI door checker for door \'%s\'' % self.get_name())
    while self.__run:
      current_status = None
      if self.get_hardware_type() == 'gpio':
        current_status = terrariumDoor.OPEN if GPIO.input(terrariumUtils.to_BCM_port_number(self.get_address())) else terrariumDoor.CLOSED

      elif self.get_hardware_type() == 'remote' and (int(time.time()) - self.__last_check) >= terrariumDoor.REMOTE_TIMEOUT:
        current_status = None
        url_data = terrariumUtils.parse_url(self.get_address())
        if url_data is False:
          logger.error('Remote url \'%s\' for door \'%s\' is not a valid remote source url!' % (self.get_address(),self.get_name()))
        else:
          data = terrariumUtils.get_remote_data(self.get_address())
          if data is not None:
            current_status = terrariumDoor.OPEN if terrariumUtils.is_true(data) else terrariumDoor.CLOSED
          else:
            logger.warning('Remote door \'%s\' got error from remote source \'%s\'' % (self.get_name(),self.get_address()))

        self.__last_check = int(time.time())

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
    if self.get_hardware_type() == 'gpio':
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

  def stop(self):
    self.__run = False
    if self.get_hardware_type() == 'gpio':
      GPIO.cleanup(terrariumUtils.to_BCM_port_number(self.get_address()))

    logger.debug('Stopped door sensor {}'.format(self.get_name()))