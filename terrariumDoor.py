# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

class terrariumDoor():
  
  def __init__(self, gpio_pin, callback = None):
    self.gpio_pin = int(gpio_pin)
    self.door_status = 'closed'
    self.callback = callback

    ## set GPIO mode to BCM
    ## this takes GPIO number instead of pin number
    GPIO.setmode(GPIO.BCM)
    
    ## use the built-in pull-up resistor
    GPIO.setup(self.gpio_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)  # activate input with PullUp
    
    # Add detetion with callback
    GPIO.add_event_detect(self.gpio_pin, GPIO.BOTH, callback=self.__update_status)

  def __update_status(self):
    current_status = 'open' if GPIO.input(self.__pin) else 'closed'
    if current_status != self.door_status and self.callback:
      self.callback(self.get_status())
    
    self.door_status = current_status

  def get_status(self):
    return self.door_status
  
  def is_open(self):
    return self.door_status == 'open'
  
  def is_closed(self):
    return self.door_status == 'closed'