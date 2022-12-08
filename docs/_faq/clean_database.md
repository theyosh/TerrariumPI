---
title: Cleanup database
categories: [Website, FAQ]
tags: [database,cleanup,space]
---
If TerrariumPI is running for years it happens that the database get rather big and therefore slowing down the system. Also deleting the data will not give back the disk space. So there is a script which can cleanup the database and reclaim disk space by reducing the database.

In order to cleanup the database, make sure that TerrariumPI is stopped! Else there is a possibility on database corruption.

1. Enter the TerrariumPI folder: `cd /home/pi/TerrariumPI/`
2. Enable Python3 virtual environment: `source venv/bin/activate`
3. Go to the folder 'contrib': `cd contrib`
4. Run the command: `python db_cleanup.py`

This will start the script. It will first show some information about required disk space and how much data will be kept.

```console
This script will cleanup your terrariumpi.db file. We will keep 420 days, 0:00:00 of data from now. If you want to make a backup first, please enter no and make your backup.
Database size: 2.5 GB, free diskspace: 11.2 GB
Would you like to continue? Enter yes to start. Anything else will abort.
yes
Starting cleaning up table 'SensorHistory'. Deleting data older then 2021-10-14 19:51:53.022888 in batches of 1000 records. This could take some time...
Total rows: 13022217 from 2021-11-19 09:33:00 till 2022-12-05 23:31:00. Took (12.002253532409668)
Clean up rows: No data, nothing to do!
Starting cleaning up table 'ButtonHistory'. Deleting data older then 2021-10-14 19:52:05.026467 in batches of 1000 records. This could take some time...
Total rows: 407877 from 2021-11-19 09:34:23.432795 till 2022-12-05 23:28:51.271120. Took (0.4699835777282715)
Clean up rows: No data, nothing to do!
Start reclaming lost space. This will rebuild the database and give all the delete space back. This will take a lot of time
Done in 1011.5509634017944 seconds
Database is now cleaned and should be reduced in size:
Database size: 2.5 GB, free diskspace: 8.7 GB
Restart TerrariumPI and check if the sensor graphs still working. If it is al working, remove the file ../data/terrariumpi.db.old
```

When this done, you can restart TerrariumPI again. Check if all graphs are working. If that is the case, you can delete the backup database at the location 'data/terrariumpi.db.old': `rm ../data/terrariumpi.db.old`
