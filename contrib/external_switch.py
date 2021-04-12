#!/usr/bin/env python

# This is just an example script to test the functionality for TerrariumPI. It is also a reference for implementing your own scripts

import sys
import random

# When there is no extra arguments, TerrariumPI expect a float value to return the current state.
# Return -1.0 when not supported.
if len(sys.argv) == 1:
  # Provide a fake dimmer readout...
  #print(random.randint(0,100))

  # Or no readout test
  print('-1.0')

else:

  try:
    value = int(float(sys.argv[1]))
  except Exception as ex:
    raise ValueError('Invalid input value. Should be a number between 0 and 100 including')

  if not (0 <= value <= 100):
    raise ValueError('Invalid input value. Should be a number between 0 and 100 including')

  if value == 0:
    print('Toggle power switch to state OFF')
    # Call your code here....
  else:
    print('Toggle power switch to state ON or dimming value: {}'.format(value))
    # Call your code here....