# -*- coding: utf-8 -*-

import time
import RPi.GPIO as gpio
import thread

import logging
terrarium_log = logging.getLogger('root')

class terrariumDoor:
  def __init__(self,pin):
    self.__pin = pin
    self.__door_open = False
    
    ## set GPIO mode to BCM
    ## this takes GPIO number instead of pin number
    gpio.setmode(gpio.BCM)

    ## use the built-in pull-up resistor
    gpio.setup(self.__pin,gpio.IN,pull_up_down=gpio.PUD_UP)  # activate input with PullUp

    thread.start_new_thread(self.__checker, ())

  def __checker(self):
    terrarium_log.debug('Started door sensor checker thread')
    while True:
      old_state = self.__door_open
      self.__door_open = gpio.input(self.__pin)
      if old_state != self.__door_open:
        terrarium_log.debug('Door status changed from %s to %s', ('open' if old_state else 'closed'),('open' if self.__door_open else 'closed'))
      time.sleep(1)

  def open(self):
    return self.__door_open == True

  def close(self):
    return not self.open()
