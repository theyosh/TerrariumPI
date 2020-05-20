#!/usr/bin/env python

# DHT.py
# 2019-11-07
# Public Domain
# Source: http://abyz.me.uk/rpi/pigpio/examples.html#Python%20code / http://abyz.me.uk/rpi/pigpio/code/DHT.py

import time
import pigpio

DHTAUTO=0
DHT11=1
DHTXX=2

DHT_GOOD=0
DHT_BAD_CHECKSUM=1
DHT_BAD_DATA=2
DHT_TIMEOUT=3

class sensor:
   """
   A class to read the DHTXX temperature/humidity sensors.
   """
   def __init__(self, pi, gpio, model=DHTAUTO, callback=None):
      """
      Instantiate with the Pi and the GPIO connected to the
      DHT temperature and humidity sensor.

      Optionally the model of DHT may be specified.  It may be one
      of DHT11, DHTXX, or DHTAUTO.  It defaults to DHTAUTO in which
      case the model of DHT is automtically determined.

      Optionally a callback may be specified.  If specified the
      callback will be called whenever a new reading is available.

      The callback receives a tuple of timestamp, GPIO, status,
      temperature, and humidity.

      The timestamp will be the number of seconds since the epoch
      (start of 1970).

      The status will be one of:
      0 DHT_GOOD (a good reading)
      1 DHT_BAD_CHECKSUM (receieved data failed checksum check)
      2 DHT_BAD_DATA (data receieved had one or more invalid values)
      3 DHT_TIMEOUT (no response from sensor)
      """
      self._pi = pi
      self._gpio = gpio
      self._model = model
      self._callback = callback

      self._new_data = False
      self._in_code = False

      self._bits = 0
      self._code = 0

      self._status = DHT_TIMEOUT
      self._timestamp = time.time()
      self._temperature = 0.0
      self._humidity = 0.0

      pi.set_mode(gpio, pigpio.INPUT)
      self._last_edge_tick = pi.get_current_tick() - 10000
      self._cb_id = pi.callback(gpio, pigpio.RISING_EDGE, self._rising_edge)

   def _datum(self):
      return ((self._timestamp, self._gpio, self._status,
              self._temperature, self._humidity))

   def _validate_DHT11(self, b1, b2, b3, b4):
      t = b2
      h = b4
      if (b1 == 0) and (b3 == 0) and (t <= 60) and (h >= 9) and (h <= 90):
         valid = True
      else:
         valid = False
      return (valid, t, h)

   def _validate_DHTXX(self, b1, b2, b3, b4):
      if b2 & 128:
         div = -10.0
      else:
         div = 10.0
      t = float(((b2&127)<<8) + b1) / div
      h = float((b4<<8) + b3) / 10.0
      if (h <= 110.0) and (t >= -50.0) and (t <= 135.0):
         valid = True
      else:
         valid = False
      return (valid, t, h)

   def _decode_dhtxx(self):
      """
            +-------+-------+
            | DHT11 | DHTXX |
            +-------+-------+
      Temp C| 0-50  |-40-125|
            +-------+-------+
      RH%   | 20-80 | 0-100 |
            +-------+-------+

               0      1      2      3      4
            +------+------+------+------+------+
      DHT11 |check-| 0    | temp |  0   | RH%  |
            |sum   |      |      |      |      |
            +------+------+------+------+------+
      DHT21 |check-| temp | temp | RH%  | RH%  |
      DHT22 |sum   | LSB  | MSB  | LSB  | MSB  |
      DHT33 |      |      |      |      |      |
      DHT44 |      |      |      |      |      |
            +------+------+------+------+------+
      """
      b0 =  self._code        & 0xff
      b1 = (self._code >>  8) & 0xff
      b2 = (self._code >> 16) & 0xff
      b3 = (self._code >> 24) & 0xff
      b4 = (self._code >> 32) & 0xff
      
      chksum = (b1 + b2 + b3 + b4) & 0xFF

      if chksum == b0:
         if self._model == DHT11:
            valid, t, h = self._validate_DHT11(b1, b2, b3, b4)
         elif self._model == DHTXX:
            valid, t, h = self._validate_DHTXX(b1, b2, b3, b4)
         else: # AUTO
            # Try DHTXX first.
            valid, t, h = self._validate_DHTXX(b1, b2, b3, b4)
            if not valid:
               # try DHT11.
               valid, t, h = self._validate_DHT11(b1, b2, b3, b4)
         if valid:
            self._temperature = t
            self._humidity = h
            self._status = DHT_GOOD
         else:
            self._status = DHT_BAD_DATA
      else:
         self._status = DHT_BAD_CHECKSUM
      self._new_data = True

   def _rising_edge(self, gpio, level, tick):
      edge_len = pigpio.tickDiff(self._last_edge_tick, tick)
      self._last_edge_tick = tick
      if edge_len > 10000:
         self._in_code = True
         self._bits = -2
         self._code = 0
      elif self._in_code:
         self._bits += 1
         if self._bits >= 1:
            self._code <<= 1
            if (edge_len >= 60) and (edge_len <= 150):
               if edge_len > 100:
                  # 1 bit
                  self._code += 1
            else:
               # invalid bit
               self._in_code = False
         if self._in_code:
            if self._bits == 40:
               self._decode_dhtxx()
               self._in_code = False

   def _trigger(self):
      self._new_data = False
      self._timestamp = time.time()
      self._status = DHT_TIMEOUT
      self._pi.write(self._gpio, 0)
      if self._model != DHTXX:
         time.sleep(0.018)
      else:
         time.sleep(0.001)
      self._pi.set_mode(self._gpio, pigpio.INPUT)


   def cancel(self):
      """
      """
      if self._cb_id is not None:
         self._cb_id.cancel()
         self._cb_id = None

   def read(self):
      """
      This triggers a read of the sensor.

      The returned data is a tuple of timestamp, GPIO, status,
      temperature, and humidity.

      The timestamp will be the number of seconds since the epoch
      (start of 1970).

      The status will be one of:
      0 DHT_GOOD (a good reading)
      1 DHT_BAD_CHECKSUM (receieved data failed checksum check)
      2 DHT_BAD_DATA (data receieved had one or more invalid values)
      3 DHT_TIMEOUT (no response from sensor)
      """
      self._trigger()
      for i in range(5): # timeout after 0.25 seconds.
         time.sleep(0.05)
         if self._new_data:
            break
      datum = self._datum()
      if self._callback is not None:
          self._callback(datum)
      return datum

if __name__== "__main__":
   import sys
   import pigpio
   import DHT

   def callback(data):
      print("{:.3f} {:2d} {} {:3.1f} {:3.1f} *".
         format(data[0], data[1], data[2], data[3], data[4]))

   argc = len(sys.argv) # get number of command line arguments

   if argc < 2:
      print("Need to specify at least one GPIO")
      exit()

   pi = pigpio.pi()
   if not pi.connected:
      exit()

   # Instantiate a class for each GPIO
   # for testing use a GPIO+100 to mean use the callback
   S = []
   for i in range(1, argc): # ignore first argument which is command name
      g = int(sys.argv[i])
      if (g >= 100):
         s = DHT.sensor(pi, g-100, callback=callback)
      else:
         s = DHT.sensor(pi, g)
      S.append((g,s)) # store GPIO and class

   while True:
      try:
         for s in S:
            if s[0] >= 100:
               s[1].read() # values displayed by callback
            else:
               d = s[1].read()
               print("{:.3f} {:2d} {} {:3.1f} {:3.1f}".
                  format(d[0], d[1], d[2], d[3], d[4]))
         time.sleep(2)
      except KeyboardInterrupt:
         break

   for s in S:
      s[1].cancel()
      print("cancelling {}".format(s[0]))
   pi.stop()


