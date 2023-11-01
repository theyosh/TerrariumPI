---
title: Reset webgui address
categories: [Website, FAQ]
tags: [database,gui,address,port,listening]
---
If you have configured a fixed IP as address and your PI has changed the IP due to a network change, the TerrariumPI software will not load the web gui. The system is still running, but you are unable to access the webgui.

The solution for this is to reset the IP address that was entered. Here are the steps to fix it.

1. Stop TerrariumPI: `sudo service terrariumpi stop`
2. Enter the TerrariumPI folder: `cd /home/pi/TerrariumPI/`
3. Open the database with sqlite: `sqlite3 data/terrariumpi.db`
4. Run the following query statement: `DELETE FROM Setting WHERE id = 'host';`
5. Run the following query statement: `DELETE FROM Setting WHERE id = 'port';`
6. Exit the database by pressing `CTRL+d`
7. Start TerrariumPI: `sudo service terrariumpi start`

The steps 3 - 6 are shown below.

```console
sqlite3 data/terrariumpi.db
SQLite version 3.27.2 2019-02-25 16:06:06
Enter ".help" for usage hints.
sqlite> DELETE FROM Setting WHERE id = 'host';
sqlite> DELETE FROM Setting WHERE id = 'port';
sqlite>
```

When TerrariumPI is started up, you should be able to access the web gui again on the new IP of the Raspberry PI
