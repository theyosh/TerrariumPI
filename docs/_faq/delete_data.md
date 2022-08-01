---
title: How to delete a sensor/relay/button TerrariumPI
categories: [Website, FAQ]
tags: [delete,manual]
---

When you want to delete a sensor/relay/button that has been used for more than 3 months, you should use the manual/debug way to delete the sensor through the GUI. This is due to the time it takes to delete the data from the Sqlite database. If this takes more then 2 minutes, the systemd watchdog will restart TerrariumPI and the delete will not succeed.

In order to not have the problem of the 2 minutes watchdog timeout, you have to run TerrariumPI in debug mode. You can [stop TerrariumPI]({% link _faq/systemd.md %}#stop) as follows.

When running in [debug mode]({% link _faq/debug.md %}), you can just go the sensor/relay/button and delete it. Now it does not matter how much time it takes. Just wait until done.

If the deleting is done, stop the debug version of TerrariumPI and [start normally]({% link _faq/systemd.md %}#start).
