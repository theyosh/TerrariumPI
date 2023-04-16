---
title: Cleanup database
categories: [Website, FAQ]
tags: [database,cleanup,space]
---
If TerrariumPI is running for years it happens that the database get rather big and therefore slowing down the system. Also deleting the data will not give back the disk space. So there is a script which can cleanup the database and reclaim disk space by reducing the database.

In order to cleanup the database, make sure that TerrariumPI is **stopped**! Else there is a possibility on database corruption.

When you cleanup the database, we need at least the same amount of free space as the size of the database. The script will check this. Make sure you have enough free diskspace. If this is a problem, you can also try to download the database and run this on a desktop/laptop.

The cleanup can take up to **10 hours**!. So make sure your environment is stable and can survive for that period.

1. Enter the TerrariumPI folder: `cd /home/pi/TerrariumPI/`
2. Enable Python3 virtual environment: `source venv/bin/activate`
3. Go to the folder 'contrib': `cd contrib`
4. Run the command: `python db_cleanup.py`

This will start the script. It will first show some information about required disk space and how much data will be kept.

```console
This script will cleanup your terrariumpi.db file. We will keep 420 days, 0:00:00 of data from now. If you want to make a backup first, please enter no and make your backup.
Database size: 2.04 GB, free diskspace: 5.19 GB
Would you like to continue? Enter yes to start. Anything else will abort.
yes
Starting cleaning up table 'SensorHistory'. Deleting data older then 2022-02-20 18:27:17 in batches of 10000 records. This could take some time...
Analyzing total rows:       13542131 from 2022-02-20 18:14 till 2023-04-16 03:56. Took 1.43 seconds
Analyzing rows to clean up:      322 from 2022-02-20 18:14 till 2022-02-20 18:27. Took 1.12 seconds
Removing 322 rows (0.00%) of data in 1 steps of 10000 rows.
0%....10%....20%....30%....40%....50%....60%....70%....80%....90%....100%
Clean up is done in 1.20 seconds
Starting cleaning up table 'ButtonHistory'. Deleting data older then 2022-02-20 18:27:17 in batches of 10000 records. This could take some time...
Analyzing total rows:       23094 from 2022-02-20 19:00 till 2023-04-16 03:00. Took 0.01 seconds
Analyzing rows to clean up: No data, nothing to do!
Start reclaiming lost space. This will rebuild the database and give all the delete space back. This will take a lot of time
Done in 10.43 seconds
Database is now cleaned and should be reduced in size:
Database size: 2.04 GB, free diskspace: 172.71 GB
Restart TerrariumPI and check if the sensor graphs still working. If it is al working, remove the file ../data/terrariumpi.db.old
```

When this done, you can restart TerrariumPI again. Check if all graphs are working. If that is the case, you can delete the backup database at the location 'data/terrariumpi.db.old': `rm ../data/terrariumpi.db.old`
