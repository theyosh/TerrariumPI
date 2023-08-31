---
title: How to use a relay multiple times
categories: [Website, FAQ]
tags: [relay, duplicate]
---

A much asked question is how can a relay used in 2 or more areas. By default this is not possible, due to the **a relay can only be used once** policy. This made it a bit easier to make sure that relays stays in the correct state. Even after power failures.

But it is possible to make this possible by using [script relays]({% link _hardware/script_relay.md %}). You have to create a new script relay which controls the relay you want to duplicate. This means creating some small code. An example script relay can be found in the [contrib](https://github.com/theyosh/TerrariumPI/blob/main/contrib/external_switch.py) folder.

**Important**: The important thing here is that the return value (read out) of the script is always **-1**. This is very important. By returning a -1 as value, will instruct TerrariumPI to use the last state from the database. **Not** from the device.

When you relay script is ready, you need to create a second script with a different name, with the same code. This can be done by creating a `symlink`:

```sh
ln -s original_relay_script.py duplicate_relay_script.py
```

Now you have 2 relay scripts with the same code and logic, but with different names. Create 2 `script relays` in TerrariumPI with the 2 scripts. And do **not** add the original relay to the TerrariumPI, or at least, do not use it in any areas.

The two relay scripts can now be used in different areas and should not interfere with each other.

You can use all the python [libraries](https://github.com/theyosh/TerrariumPI/blob/main/requirements.txt) that are installed by TerrariumPI.

Or you can create a bash script or any executable that toggles the relay, and returns -1 as readout.
