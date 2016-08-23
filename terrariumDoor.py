# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import thread

from gevent import monkey, sleep
monkey.patch_all()

class terrariumDoor():

  def __init__(self, gpio_pin, callback = None):
    ## set GPIO mode to BCM
    ## this takes GPIO number instead of pin number
    GPIO.setmode(GPIO.BOARD)

    self.door_status = None
    self.callback = callback
    
    self.set_gpio_pin(gpio_pin)

    # Add detetion with callback !!!!THIS WILL CRASH THE GEVENT LOOP SOMEHOW!!!!!!
    # GPIO.add_event_detect(gpio_pin, GPIO.BOTH, callback=callback, bouncetime=300)
    thread.start_new_thread(self.__checker, ())

  def __checker(self):
    while True:
      current_status = 'open' if GPIO.input(self.gpio_pin) else 'closed'
      if current_status != self.door_status:
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
