#!/usr/bin/env python3

# With this script, you can control an existing relay/dimmer as a new relay/dimmer. This allows to duplicate existing relays in order to use a single relay in multiple areas
# When using this script, do NOT use the original relay in areas! That will cause strange behavior
# Based on external_switch.py, and can be used as an 'script relay' - https://theyosh.github.io/TerrariumPI/hardware/relay/script-relay/

import sys
import requests

# Enter here the original relay ID from TP4.
# Can be found at http://127.0.0.1:8090/api/relays/
RELAY_ID="ebdf5ed1f4768d57c1bc999e410e6a33"
# Enter the username and password. If you change this in the GUI, also update it here!!!
USERNAME="admin"
PASSWORD="password"

# Should not be changed
TP_SERVER="http://127.0.0.1"

# !! --- NO CHANGES BELOW THIS LINE ---- !!
RELAY_URL=f'{TP_SERVER}/api/relays/{RELAY_ID}'

# For our purpose, we do not provide a readout. So always return -1.0
if len(sys.argv) == 1:
    print("-1.0")

# Here we start to set the relay to the requested state: Off (=0) or On (>0)
else:
    try:
        value = int(float(sys.argv[1]))
    except Exception as ex:
        raise ValueError(f"Invalid input value. Should be a number between 0 and 100 including. Error {ex}")

    if not (0 <= value <= 100):
        raise ValueError("Invalid input value. Should be a number between 0 and 100 including")

    if value == 0:
        requests.post(f'{RELAY_URL}/{value}/', data={}, auth=(USERNAME, PASSWORD))

    else:
        requests.post(f'{RELAY_URL}/{value}/', data={}, auth=(USERNAME, PASSWORD))
