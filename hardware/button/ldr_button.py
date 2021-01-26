# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumButton, terrariumButtonException
from terrariumUtils import terrariumUtils

# pip install gpiozero
from gpiozero import LightSensor

class terrariumLDRSensor(terrariumButton):
  HARDWARE = 'ldr'
  NAME     = 'Light sensor'

  __CAPACITOR = 1 # in uF

  def calibrate(self,calibration_data):
    # Only (re)calibrate when the values are different
    if self.__CAPACITOR != int(calibration_data['ldr_capacitor']):
      self.stop()
      self.__CAPACITOR = int(calibration_data['ldr_capacitor'])
      self.load_hardware()

  def load_hardware(self):
    address = self._address
    self._device['device'] = LightSensor(terrariumUtils.to_BCM_port_number(address[0]), charge_time_limit=(self.__CAPACITOR * 0.001), partial=True)
    self._device['device'].when_light = self._pressed
    self._device['device'].when_dark  = self._released
    self._device['state'] = self.PRESSED if self._device['device'].wait_for_light(1) else self.RELEASED

  @property
  def is_light(self):
    return self.pressed

  @property
  def is_dark(self):
    return not self.is_light