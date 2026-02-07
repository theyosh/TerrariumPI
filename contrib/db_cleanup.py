#!/usr/bin/env python
"""
Run this script in the contrib folder with the same python version as TerrariumPI

./db_cleanup.py
"""

import sqlite3
from datetime import datetime, timedelta
from time import time
import shutil
import os
import requests


def humansize(nbytes):
    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


class HistoryCleanup:
    def __init__(self, database="../data/terrariumpi.db", period=timedelta(weeks=60), batch=10000):
        """
        Construct the database history clean up object

        Args:
            database (str, optional): The database location path. Defaults to '../data/terrariumpi.db'.
            period (_type_, optional): Period in weeks to keep. Defaults to 60 weeks.
            batch (int, optional): Amount of records to delete at once. Defaults to 10000.
        """

        print(
            f"This script will cleanup your terrariumpi.db file. We will keep {period.days} days of data from now. If you want to make a backup first, please enter no and make your backup."
        )

        self.cleanup_tables = ["Button","Sensor"]
        self.progress_amount = 100000
        self.total_to_keep = 0
        self.counter = 0

        self.database = database
        self.database_size = 0
        self.time_limit = f"{datetime.now() - period:%Y-%m-%d %H:%M:%S}"

        self.check_offline()

        self.db = sqlite3.connect(self.database)
        with self.db as db:
            db.set_progress_handler(self.__sql_progress, self.progress_amount)
            cur = db.cursor()
            cur.execute("PRAGMA journal_mode = OFF")
            cur.execute("PRAGMA temp_store = OFF")

        self.db.row_factory = sqlite3.Row
        self.get_current_db_version()

    def get_current_db_version(self):
        self.version = 0
        with self.db as db:
            cur = db.cursor()
            self.version = int(cur.execute("PRAGMA user_version").fetchall()[0][0])

    def check_free_storage(self):
        disk_stats = shutil.disk_usage(self.database)
        file_size = os.path.getsize(self.database)
        print(f"Database size: {humansize(file_size)}, free disk space: {humansize(disk_stats[2])}")
        if file_size > disk_stats[2]:
            print(f"Not enough disk space left for cleaning the database. We need at least {humansize(file_size)}")
            exit(1)

        if self.database_size == 0:
            self.database_size = file_size
        else:
            print(f"Cleaned up {humansize(self.database_size - file_size)}")

    def check_offline(self):
        try:
            data = requests.get("http://localhost:8090/api/system_status/")
            if data.status_code == 200:
                print("TerrariumPI is still running. Please shutdown first, else you will get data corruption.")
                exit(1)
        except requests.ConnectionError:
            pass

    def get_total_records(self, table, keep=False):
        self.counter = 0
        sql = f"SELECT count(*) as total, MIN(timestamp) as begin, MAX(timestamp) as end FROM `{table}`"
        parameters = ()
        if keep:
            sql += " WHERE timestamp < ?"
            parameters = (self.time_limit,)

        with self.db as db:
            for row in db.execute(sql, parameters):
                return (row["total"], row["begin"], row["end"])

    def get_records_to_delete(self, table):
        return self.get_total_records(table, True)

    def __sql_progress(self):
        self.counter += 1
        # f-string format not working here
        print("{}".format(['|','/','-','\\'][self.counter % 4]), end="\r")
        return 0  # Return 0 to continue, non-zero to abort

    def __vacuum(self):
        start = time()

        print(
            "Start reclaiming lost space. This will rebuild the database and give all the delete space back. This will take a lot of time"
        )
        print("  Vacuuming database ...", end="\r")
        self.counter = 0
        with self.db as db:
            cur = db.cursor()
            cur.execute("VACUUM")
            cur.execute("PRAGMA journal_mode = MEMORY")
            cur.execute("PRAGMA temp_store = MEMORY")
            cur.execute("PRAGMA user_version = {}".format(self.version))

        print(f"Vacuuming database done in {(time()-start):.2f} seconds")

    def get_space_back(self):
        self.__clean_up_by_deleting()
        self.__vacuum()

    def __clean_up_by_deleting(self):
        for table in self.cleanup_tables:
            table += "History"

            print(f"Start cleaning up table {table} ...")
            print("  Getting totals ...", end="\r")
            totals = self.get_total_records(table)
            print("  Getting records to delete ...", end="\r")
            cleanup = self.get_records_to_delete(table)
            print(f"Table {table} contains {totals[0]} records, of which being deleted {cleanup[0]} records {cleanup[0]/totals[0]*100:.2f}%.")

            sql = f"DELETE FROM `{table}` WHERE timestamp < ?"
            parameters = (self.time_limit,)
            print("  Deleting data ...", end="\r")
            start = time()
            self.counter = 0

            with self.db as db:
                cur = db.cursor()
                cur.execute(sql, parameters)

            print(f"Deleting data done in {(time()-start):.2f} seconds")


cleanup = HistoryCleanup()
cleanup.check_free_storage()

go = input("Would you like to continue? Enter yes to start. Anything else will abort.\n")
if go.lower() != "yes":
    exit(0)

cleanup.get_space_back()

print("Database is now cleaned and should be reduced in size. TerrariumPI can now be started.")
cleanup.check_free_storage()
