#!/usr/bin/env python
import sys

# This is just an example script to test the functionality for TerrariumPI. It is also a reference for implementing your own scripts

if len(sys.argv) == 1:
  raise SyntaxError('No arguments specified')

try:
  value = int(sys.argv[1])
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
