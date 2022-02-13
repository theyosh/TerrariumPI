#!/usr/bin/env python3

# This is just an example script to test the functionality for TerrariumPI. It is also a reference for implementing your own scripts

import sys
from pathlib import Path
from datetime import datetime

# Enable debug to see if the script is running correctly. The output will be at /tmp/terrariumpi_test_relay_script.txt
DEBUG = True

# When there is no extra arguments, TerrariumPI expect a float value to return the current state.
# Return -1.0 when not supported.
if len(sys.argv) == 1:
  # Call your code here....
  # In this demo no read out option, return default value of -1.0
  print('-1.0')

else:

  try:
    value = int(float(sys.argv[1]))
  except Exception as ex:
    raise ValueError(f'Invalid input value. Should be a number between 0 and 100 including. Error {ex}')

  if not (0 <= value <= 100):
    raise ValueError('Invalid input value. Should be a number between 0 and 100 including')

  if DEBUG:
    debug_file = Path('/tmp/terrariumpi_test_relay_script.txt')

  if value == 0:
    if DEBUG:
      with debug_file as output:
        output.write_text(f'[{datetime.now()}] Toggle power switch to state OFF => {value}\n')

    # Call your code here....

  else:
    if DEBUG:
      with debug_file as output:
        output.write_text(f'[{datetime.now()}] Toggle power switch to state ON or dimming value: => {value}\n')

    # Call your code here....

  # This is optional, and will not be used in TerrariumPI
  print(value)