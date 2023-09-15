#!/usr/bin/env python
"""
 Run this script in the contrib folder with the same python version as TerrariumPI

 ./db_cleanup.py
"""

import sqlite3
from datetime import datetime, timedelta
import time
import math
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
            f"This script will cleanup your terrariumpi.db file. We will keep {period} of data from now. If you want to make a backup first, please enter no and make your backup."
        )

        self.check_offline()

        self.delete_batch = batch
        self.time_limit = f"{datetime.now() - period:%Y-%m-%d %H:%M:%S}"

        self.database = database
        self.new_database = self.database.replace(".db", ".new.db")

        self.db = sqlite3.connect(self.database)
        with self.db as db:
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
        diskstats = shutil.disk_usage(self.database)
        filesize = os.path.getsize(self.database)
        print("Database size: {}, free diskspace: {}".format(humansize(filesize), humansize(diskstats[2])))
        if filesize > diskstats[2]:
            print("Not enough space left for cleaning the database. We need at least {}".format(humansize(filesize)))
            exit(1)

    def check_offline(self):
        try:
            data = requests.get("http://localhost:8090/api/system_status/")
            if data.status_code == 200:
                print("TerrariumPI is still running. Please shutdown first, else you will get data corruption.")
                exit(1)
        except requests.ConnectionError:
            pass

    def get_total_records(self, table, period=None):
        sql = f"SELECT count(*) as total, MIN(timestamp) as begin, MAX(timestamp) as end FROM {table}"
        parameters = ()
        if period is not None:
            sql += " WHERE timestamp < ?"
            parameters = (self.time_limit,)

        with self.db as db:
            for row in db.execute(sql, parameters):
                return (row["total"], row["begin"], row["end"])

    def get_clean_up_records(self, table):
        return self.get_total_records(table, True)

    def get_orphan_records(self, table):
        if "SensorHistory" == table:
            table_source = "Sensor"
        if "ButtonHistory" == table:
            table_source = "Button"
        elif "RelayHistory" == table:
            table_source = "Relay"

        sql = f"SELECT count(*) as total, MIN(timestamp) as begin, MAX(timestamp) as end FROM {table} WHERE {table_source.lower()} NOT IN (SELECT id FROM {table_source})"

        with self.db as db:
            for row in db.execute(sql):
                return (row["total"], row["begin"], row["end"])

    def get_space_back(self):
        start = time.time()
        print(
            "Start reclaiming lost space. This will rebuild the database and give all the delete space back. This will take a lot of time"
        )

        self.db.execute(f"VACUUM INTO '{self.new_database}'")

        with sqlite3.connect(self.new_database) as db:
            cur = db.cursor()
            cur.execute("PRAGMA journal_mode = MEMORY")
            cur.execute("PRAGMA temp_store = MEMORY")
            cur.execute("PRAGMA user_version = {}".format(self.version))

        print(f"Done in {(time.time()-start):.2f} seconds")

    def __delete_orphan_records(self, table):
        if "SensorHistory" == table:
            table_source = "Sensor"
        if "ButtonHistory" == table:
            table_source = "Button"
        elif "RelayHistory" == table:
            table_source = "Relay"

        print(f"Starting cleaning up table '{table}' by deleting orphan records. This could take some time...")

        start = time.time()
        print("Analyzing total rows:      ", end="", flush=True)
        total_sensor_data = self.get_total_records(table)
        number_padding = len(str(total_sensor_data[0]))
        if total_sensor_data[0] == 0:
            print(
                " {}. Took {:.2f} seconds".format(
                    str(total_sensor_data[0]).rjust(number_padding),
                    time.time() - start,
                )
            )
            return

        print(
            " {} from {:%Y-%m-%d %H:%M} till {:%Y-%m-%d %H:%M}. Took {:.2f} seconds".format(
                str(total_sensor_data[0]).rjust(number_padding),
                datetime.fromisoformat(total_sensor_data[1]),
                datetime.fromisoformat(total_sensor_data[2]),
                time.time() - start,
            )
        )
        start = time.time()
        print("Analyzing rows to clean up:", end="", flush=True)
        total_cleanup_data = self.get_orphan_records(table)

        if total_cleanup_data[0] == 0:
            print(" No data, nothing to do!")
            return

        print(
            " {} from {:%Y-%m-%d %H:%M} till {:%Y-%m-%d %H:%M}. Took {:.2f} seconds".format(
                str(total_cleanup_data[0]).rjust(number_padding),
                datetime.fromisoformat(total_cleanup_data[1]),
                datetime.fromisoformat(total_cleanup_data[2]),
                time.time() - start,
            )
        )

        start = time.time()
        delete_steps = math.ceil(total_cleanup_data[0] / self.delete_batch)
        print(
            "Removing {} rows ({:.2f}%) of data in {} steps of {} rows.".format(
                total_cleanup_data[0],
                (total_cleanup_data[0] / total_sensor_data[0]) * 100,
                delete_steps,
                self.delete_batch,
            )
        )
        print("0%", end="", flush=True)
        new_percentage = 10

        sql = f"DELETE FROM {table} WHERE {table_source.lower()} NOT IN (SELECT id FROM {table_source}) LIMIT ?"
        parameters = (self.delete_batch,)

        with self.db as db:
            for step in range(delete_steps):
                if int((step / delete_steps) * 100) >= new_percentage:
                    print("{:.0f}%".format(new_percentage), end="", flush=True)
                    new_percentage += 10

                print(".", end="", flush=True)
                db.execute(sql, parameters)

        print("100%")
        print("Clean up is done in {:.2f} seconds".format(time.time() - start))

    def __clean_up(self, table):
        print(
            f"Starting cleaning up table '{table}'. Deleting data older then {self.time_limit} in batches of {self.delete_batch} records. This could take some time..."
        )

        start = time.time()
        print("Analyzing total rows:      ", end="", flush=True)
        total_sensor_data = self.get_total_records(table)
        number_padding = len(str(total_sensor_data[0]))
        if total_sensor_data[0] == 0:
            print(
                " {}. Took {:.2f} seconds".format(
                    str(total_sensor_data[0]).rjust(number_padding),
                    time.time() - start,
                )
            )
            return

        print(
            " {} from {:%Y-%m-%d %H:%M} till {:%Y-%m-%d %H:%M}. Took {:.2f} seconds".format(
                str(total_sensor_data[0]).rjust(number_padding),
                datetime.fromisoformat(total_sensor_data[1]),
                datetime.fromisoformat(total_sensor_data[2]),
                time.time() - start,
            )
        )
        start = time.time()
        print("Analyzing rows to clean up:", end="", flush=True)
        total_cleanup_data = self.get_clean_up_records(table)

        if total_cleanup_data[0] == 0:
            print(" No data, nothing to do!")
            return

        print(
            " {} from {:%Y-%m-%d %H:%M} till {:%Y-%m-%d %H:%M}. Took {:.2f} seconds".format(
                str(total_cleanup_data[0]).rjust(number_padding),
                datetime.fromisoformat(total_cleanup_data[1]),
                datetime.fromisoformat(total_cleanup_data[2]),
                time.time() - start,
            )
        )

        start = time.time()
        delete_steps = math.ceil(total_cleanup_data[0] / self.delete_batch)
        print(
            "Removing {} rows ({:.2f}%) of data in {} steps of {} rows.".format(
                total_cleanup_data[0],
                (total_cleanup_data[0] / total_sensor_data[0]) * 100,
                delete_steps,
                self.delete_batch,
            )
        )
        print("0%", end="", flush=True)
        new_percentage = 10

        sql = f"DELETE FROM {table} WHERE timestamp < ? LIMIT ?"
        parameters = (self.time_limit, self.delete_batch)

        with self.db as db:
            for step in range(delete_steps):
                if int((step / delete_steps) * 100) >= new_percentage:
                    print("{:.0f}%".format(new_percentage), end="", flush=True)
                    new_percentage += 10

                print(".", end="", flush=True)
                db.execute(sql, parameters)

        print("100%")
        print("Clean up is done in {:.2f} seconds".format(time.time() - start))

    def move_db(self):
        shutil.move(self.database, self.database.replace(".db", ".db.old"))
        shutil.move(self.new_database, self.database)

    def delete_orphan_sensors(self):
        self.__delete_orphan_records("SensorHistory")

    def delete_orphan_doors(self):
        self.__delete_orphan_records("ButtonHistory")

    def delete_orphan_relays(self):
        self.__delete_orphan_records("RelayHistory")

    def clean_up_sensors(self):
        self.__clean_up("SensorHistory")

    def clean_up_doors(self):
        self.__clean_up("ButtonHistory")


cleanup = HistoryCleanup()
cleanup.check_free_storage()

go = input("Would you like to continue? Enter yes to start. Anything else will abort.\n")
if go.lower() != "yes":
    exit(0)

cleanup.delete_orphan_doors()
cleanup.delete_orphan_relays()
cleanup.delete_orphan_sensors()

cleanup.clean_up_sensors()
cleanup.clean_up_doors()

cleanup.get_space_back()
cleanup.move_db()

print("Database is now cleaned and should be reduced in size:")
cleanup.check_free_storage()
print(
    "Restart TerrariumPI and check if the sensor graphs still working. If it is al working, remove the file {}".format(
        cleanup.database.replace(".db", ".db.old")
    )
)
