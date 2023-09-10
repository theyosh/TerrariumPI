---
title: How to use a relay multiple times
categories: [Website, FAQ]
tags: [relay, duplicate]
---

A much asked question is how can a relay used in 2 or more areas. By default this is not possible, due to the **a relay can only be used once** policy. This made it a bit easier to make sure that relays stays in the correct state. Even after power failures.

But there is a solution. In this FAQ we explain how to setup a relay to used in multiple areas. This can either be a [relay]({% link _hardware/script_relay.md %}) or a [dimmer]({% link _hardware/script_dimmer.md %}). It should work for both.

### Add original relay

First add the original [relay]({% link _tabs/hardware.md %}#relays) to TerrariumPI and make sure it works. Enter the power usage and the water usage values. **But never use this original relay in any area**.

### Create script relay code

1. Create a scripts folder if not exists: `mkdir scripts`
2. Copy `duplicate_switch.py` to the `scripts` folder: `cp contrib/duplicate_switch.py scripts/`
3. Edit the new script to set some settings: `nano scripts/duplicate_switch.py`

   - Edit the variables `RELAY_ID`, `USERNAME`, `PASSWORD`. The RELAY_ID can be found on the page: http://[TerrariumPI_IP]:8090/api/relays/

When this is all done, you can test if it al works by running the command: `scripts/duplicate_switch.py 100` which should toggle on the original relay.

### Duplicate the relay

Now it is easy to duplicate this relay a couple of times. Make sure you are on the `scripts` folder where the file `duplicate_switch.py` is placed.

Now by running the following command we will create a symlink to the original file. Now you will have 2 files with the same contents and will the same original relay.

```sh
ln -s duplicate_switch.py duplicate_switch_2.py
```

This can be done multiple times. Make sure you have a unique name for every new symlink.

### Adding the new relays to TerrariumPI

Now add the new scripts as new [script relay]({% link _hardware/script_relay.md %}) to TerrariumPI. Use as address `/home/pi/TerrariumPI/scripts/duplicate_switch.py`.

But here, do not enter the power and water flow values. Else the amount of used power and water will be counted **double**. Which is not correct.

Now you can use the new script relay in an area.
