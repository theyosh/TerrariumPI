# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumButton, terrariumButtonException
from terrariumUtils import terrariumUtils

# pip install gpiozero
from gpiozero import Button

class terrariumMagneticSensor(terrariumButton):
  HARDWARE = 'magnetic'
  NAME     = 'Magnetic (door) sensor'

  def load_hardware(self):
    address = self._address
    self._device['device'] = Button(terrariumUtils.to_BCM_port_number(address[0]))
    # Here we inverse the signal. So high means that the door is closed (released). And low means door is open (pressed)
    self._device['device'].when_released = self._released
    self._device['device'].when_pressed  = self._pressed

    # Invert the initial value
    self._device['state'] = self.RELEASED if self._device['device'].wait_for_release(1) else self.PRESSED

  @property
  def is_open(self):
    # Inverse the pressed state
    return not self.pressed

  @property
  def is_closed(self):
    return not self.is_open