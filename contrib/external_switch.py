#!/usr/bin/env python3

# This is just an example script to test the functionality for TerrariumPI. It is also a reference for implementing your own scripts
# All installed python libraries are available in this custom script

import sys
from pathlib import Path
from datetime import datetime

# Enable debug to see if the script is running correctly. The output will be at /tmp/terrariumpi_test_relay_script.txt
DEBUG = True

# When there is no extra arguments, TerrariumPI expect a float value above 0.0 to return the current state.
# Return -1.0 when not supported, or want to duplicate an existing relay
if len(sys.argv) == 1:
    # Call your readout or current state code here....
    # In this demo no read out option, return default value of -1.0
    print("-1.0")

# Here we start to set the relay to the requested state: Off (=0) or On (>0)
else:
    try:
        value = int(float(sys.argv[1]))
    except Exception as ex:
        raise ValueError(f"Invalid input value. Should be a number between 0 and 100 including. Error {ex}")

    if not (0 <= value <= 100):
        raise ValueError("Invalid input value. Should be a number between 0 and 100 including")

    if DEBUG:
        debug_file = Path("/tmp/terrariumpi_test_relay_script.txt")

    if value == 0:
        if DEBUG:
            debug_file.write_text(f"[{datetime.now()}] Toggle power switch to state OFF => {value}\n")

        # Call your code here to toggle the relay to OFF ....

    else:
        if DEBUG:
            debug_file.write_text(f"[{datetime.now()}] Toggle power switch to state ON or dimming value: => {value}\n")

        # Call your code here to toggle the relay to ON ....
        # Or when using it as a dimmer, use the `value` to set the dimmer

    # This is optional, and will not be used in TerrariumPI
    print(value)
