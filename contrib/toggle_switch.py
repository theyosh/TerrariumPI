#!/usr/bin/env python
import sys
import requests
import time

# Run this script as:
# without parameters, it will toggle the power state and leave in manual mode
# with paramterer on or off, it will toggle to the selected state and leave in manual mode
# with parameter on or off and a numeric value, will toggle the switch to selected state for the selected amount of seconds. Will clean manual mode

# Enter the values below.
# You can find the ID value in the settings.cfg file after you have added the individual power switch.
POWER_SWITCH_ID="1562348376"
ADMIN_NAME="admin"
ADMIN_PASSWORD="password"
TERRARIUMPI_SERVER='http://localhost:8090'

# !!! No changes below this line !!!
action = 'auto'
timeout = 0.0

if len(sys.argv) >= 2:
  if sys.argv[1] in [1,'1','On','on','true','True']:
    action = 'on'
  else:
    action = 'off'

if len(sys.argv) == 3:
  try:
    timeout = float(sys.argv[2])
  except Exception as ex:
    raise ValueError('Invalid timeout specified')

if action in ['auto','on','off']:

  power_switch_state = requests.get('{}/api/switches/{}'.format(TERRARIUMPI_SERVER,POWER_SWITCH_ID),auth=(ADMIN_NAME,ADMIN_PASSWORD))
  if power_switch_state.status_code != 200:
    raise RuntimeError('Not able to read power switch data...')

  if len(power_switch_state.json()['switches']) == 0:
    raise RuntimeError('Power switch has no data or invalid ID...')

  power_switch_state = power_switch_state.json()['switches'][0]

  # This script will break into the normal power switch state, so we need to put it in 'manual mode' despite the action is on or off.
  # Also this will leave the system in manual mode as well... :(
  if not power_switch_state['manual_mode']:
    manual_mode = requests.post('{}/api/switch/manual_mode/{}'.format(TERRARIUMPI_SERVER,POWER_SWITCH_ID),auth=(ADMIN_NAME,ADMIN_PASSWORD))
    if manual_mode.status_code != 200:
      raise RuntimeError('Not able to put switch in manual mode...')
    power_switch_state['manual_mode'] = True

  if 'auto' == action:
    # Just toggle the state.....
    switch_action = requests.post('{}/api/switch/toggle/{}'.format(TERRARIUMPI_SERVER,POWER_SWITCH_ID),auth=(ADMIN_NAME,ADMIN_PASSWORD))
  else:
    # Switch to specified sate
    switch_action = requests.post('{}/api/switch/state/{}/{}'.format(TERRARIUMPI_SERVER,POWER_SWITCH_ID,('0' if 'off' == action else '100')),auth=(ADMIN_NAME,ADMIN_PASSWORD))

  if switch_action.status_code != 200:
    raise RuntimeError('Not able to change the power switch state...')

  # If we want the state go back to what it was, specify a timeout
  if timeout > 0.0:
    # Wait the specified time in seconds.... yes, will just sleep the script
    time.sleep(timeout)

    if 'auto' == action:
      switch_action = requests.post('{}/api/switch/toggle/{}'.format(TERRARIUMPI_SERVER,POWER_SWITCH_ID),auth=(ADMIN_NAME,ADMIN_PASSWORD))
    else:
      switch_action = requests.post('{}/api/switch/state/{}/{}'.format(TERRARIUMPI_SERVER,POWER_SWITCH_ID,('100' if 'off' == action else '0')),auth=(ADMIN_NAME,ADMIN_PASSWORD))

    if switch_action.status_code != 200:
      raise RuntimeError('Not able to change the power switch state...')

    # Put manual mode to off... if it was off when we started
    # This is only done when a timeout is specified
    if power_switch_state['manual_mode']:
      #put out off manual mode
      manual_mode = requests.post('{}/api/switch/manual_mode/{}'.format(TERRARIUMPI_SERVER,POWER_SWITCH_ID),auth=(ADMIN_NAME,ADMIN_PASSWORD))
      if manual_mode.status_code != 200:
        raise RuntimeError('Not able to put switch out of manual mode...')