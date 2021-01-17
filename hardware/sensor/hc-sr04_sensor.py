# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumSensor
from terrariumUtils import terrariumUtils

from gevent import sleep
from time import time

# pip install gpiozero
from gpiozero import OutputDevice, InputDevice # DistanceSensor is broken in Gevent...... :(
# pip install RPi.GPIO
import RPi.GPIO as GPIO

class terrariumHCSR04Sensor(terrariumSensor):
  HARDWARE = 'hc-sr04'
  TYPES    = ['distance']
  NAME     = 'HC-SR04 ultrasonic ranging sensor'

  def _load_hardware(self):
    address = self._address

    device = {'trigger' : terrariumUtils.to_BCM_port_number(address[0]),
              'echo'    : terrariumUtils.to_BCM_port_number(address[1])}

    GPIO.setup(device['trigger'], GPIO.OUT) # Trigger out
    GPIO.setup(device['echo']   , GPIO.IN)  # Data in

    return device

  def _get_data(self):
    GPIO.output(self.device['trigger'], False)
    sleep(0.1)
    GPIO.output(self.device['trigger'], True)
    sleep(0.00001)
    GPIO.output(self.device['trigger'], False)

    pulse_start = time()
    starttime = pulse_start
    while GPIO.input(self.device['echo']) == 0:
      pulse_start = time()
      # Somehow, sometimes this will end in an endless loop. The value will never go to '0' (zero). So wrong measurement and return none...
      if pulse_start - starttime > 2:
        logger.warning(f'Sensor {self} is failing to get in the right state. Abort!')
        return None

    pulse_end = time()
    while GPIO.input(self.device['echo']) == 1:
      pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    # Distance in cm
    data = { 'distance' : round(pulse_duration * 17150,5)}

    return data

  def stop(self):
    GPIO.cleanup(self.device['trigger'])
    GPIO.cleanup(self.device['echo'])


class terrariumHCSR04PSensor(terrariumHCSR04Sensor):
  HARDWARE = 'hc-sr04p'
  NAME     = 'HC-SR04P ultrasonic ranging sensor'