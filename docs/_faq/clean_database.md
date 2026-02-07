---
title: Cleanup database
categories: [Website, FAQ]
tags: [database, cleanup, space]
---

If TerrariumPI is running for years it happens that the database get rather big
and therefore slowing down the system. Also deleting the data will not give back
the disk space. So there is a script which can cleanup the database and reclaim
disk space by reducing the database.

In order to cleanup the database, make sure that TerrariumPI is **stopped**!
Else there is a possibility on database corruption.

When you cleanup the database, we need at least the same amount of free space as
the size of the database. The script will check this. Make sure you have enough
free disk space. If this is a problem, you can also try to download the database
and run this on a desktop/laptop.

The cleanup can take up to **1 hour**!. So make sure your environment is stable
and can survive for that period.


1. Enter the TerrariumPI folder: `cd /home/pi/TerrariumPI/`
2. Enable Python3 virtual environment: `source venv/bin/activate`
3. Go to the folder 'contrib': `cd contrib`
4. Run the command: `python db_cleanup.py`

This will start the script. It will first show some information about required
disk space and how much data will be kept.

```console
This script will cleanup your terrariumpi.db file. We will keep 420 days of data from now. If you want to make a backup first, please enter no and make your backup.
Database size: 2.95 GB, free disk space: 6.45 GB
Would you like to continue? Enter yes to start. Anything else will abort.
yes
Start cleaning up table ButtonHistory ...
Table ButtonHistory contains 33573 records, of which being deleted 11119 records 33.12%.
Deleting data done in 0.46 seconds
Start cleaning up table SensorHistory ...
Table SensorHistory contains 18550092 records, of which being deleted 6187087 records 33.35%.
Deleting data done in 444.98 seconds
Start reclaiming lost space. This will rebuild the database and give all the delete space back. This will take a lot of time
Vacuuming database done in 1545.62 seconds
Database is now cleaned and should be reduced in size. TerrariumPI can now be started.
Database size: 1.95 GB, free disk space: 7.45 GB
Cleaned up 1 GB
```

When this done, you can restart TerrariumPI again.
