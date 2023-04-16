---
title: Which files to backup
categories: [Website, FAQ]
tags: [backup]
---
If you are running the software for a while, it is handy to backup some files in case of SD card corruption or any other reason that you have to reinstall the software. So here is a list of files that should be saved at a regular basis:

- data/* - Here is the database and calendar data stored
- log/logging.custom.cfg (optional)
- webcam/archive/* (optional) - Here you can find all the archived images of the used webcams

### Warning

Due to the nature of TerrariumPI, the database can get corrupted during creating a backup. This is due the fact that at least every 30 seconds the database is updated. And that could case that the latest data is not backup-ed correctly. This can be fixed by using the [database fix script]({% link _faq/malformed_database.md %}). After fixing you will probably miss about the last 30 seconds till 30 minutes of data. Which is mostly sensor data.
