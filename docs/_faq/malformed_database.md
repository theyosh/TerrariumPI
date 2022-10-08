---
title: "sqlite3.DatabaseError: database disk image is malformed"
categories: [Website, FAQ]
tags: [database, malformed]
---
It can happen that the database gets corrupted. The error message you will get is something like **sqlite3.DatabaseError: database disk image is malformed**

This can be fixed by replacing it with a backup database. If you do not have backup of that file or the backup is to old, you can try the following steps:

1. Make sure TerrariumPI 4 is not running: `sudo service terrariumpi stop`
2. Enter the TerrariumPI 4 folder and enable the Python environment:
   - `cd /home/pi/TerrariumPI`
   - `source venv/bin/activate`
3. Enter the `contrib` folder: `cd contrib`
4. Run the `fix_db.py` script and answer the questions: `./fix_db.py`. This will take some time.
5. When done, the database should be restored.
6. Start TerrariumPI 4: `sudo service terrariumpi start`

A backup of the broken database is left at `data/terrariumpi.db.broken`. You can delete this database when TerrariumPI is running again. `rm data/terrariumpi.db.broken`

If this happens a lot, you could look at the FAQ item: [Tune database settings]({% link _faq/tune_database.md %}) to improve the database storage.
