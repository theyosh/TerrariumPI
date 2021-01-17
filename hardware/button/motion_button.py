# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumButton, terrariumButtonException
from terrariumUtils import terrariumUtils

# pip install gpiozero
from gpiozero import MotionSensor

class terrariumMotionSensor(terrariumButton):
  HARDWARE = 'motion'
  NAME     = 'Motion sensor'

  def load_hardware(self):
    address = self._address
    self._device['device'] = MotionSensor(terrariumUtils.to_BCM_port_number(address[0]))
    self._device['device'].when_motion = self._pressed
    self._device['device'].when_no_motion  = self._released
    self._device['state'] = self.PRESSED if self._device['device'].wait_for_motion(1) else self.RELEASED

  @property
  def motion(self):
    return self.pressed

  @property
  def no_motion(self):
    return not self.motion