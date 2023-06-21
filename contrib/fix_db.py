#!/usr/bin/env python
"""
 Run this script in the contrib folder with the same python version as TerrariumPI

 1. First enable python environment: source ../venv/bin/activate
 2. Run this script with the -h for more information: ./fix_db.py -h
"""

from pathlib import Path
import time
import psutil
import argparse
import os

DATABASE = "../data/terrariumpi.db"

# Shameless copy from: https://stackoverflow.com/a/63839503
from typing import List, Union


class HumanBytes:
    METRIC_LABELS: List[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    BINARY_LABELS: List[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    PRECISION_OFFSETS: List[float] = [0.5, 0.05, 0.005, 0.0005]  # PREDEFINED FOR SPEED.
    PRECISION_FORMATS: List[str] = ["{}{:.0f} {}", "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}"]  # PREDEFINED FOR SPEED.

    @staticmethod
    def format(num: Union[int, float], metric: bool = False, precision: int = 1) -> str:
        """
        Human-readable formatting of bytes, using binary (powers of 1024)
        or metric (powers of 1000) representation.
        """

        assert isinstance(num, (int, float)), "num must be an int or float"
        assert isinstance(metric, bool), "metric must be a bool"
        assert isinstance(precision, int) and precision >= 0 and precision <= 3, "precision must be an int (range 0-3)"

        unit_labels = HumanBytes.METRIC_LABELS if metric else HumanBytes.BINARY_LABELS
        last_label = unit_labels[-1]
        unit_step = 1000 if metric else 1024
        unit_step_thresh = unit_step - HumanBytes.PRECISION_OFFSETS[precision]

        is_negative = num < 0
        if is_negative:  # Faster than ternary assignment or always running abs().
            num = abs(num)

        for unit in unit_labels:
            if num < unit_step_thresh:
                # VERY IMPORTANT:
                # Only accepts the CURRENT unit if we're BELOW the threshold where
                # float rounding behavior would place us into the NEXT unit: F.ex.
                # when rounding a float to 1 decimal, any number ">= 1023.95" will
                # be rounded to "1024.0". Obviously we don't want ugly output such
                # as "1024.0 KiB", since the proper term for that is "1.0 MiB".
                break
            if unit != last_label:
                # We only shrink the number if we HAVEN'T reached the last unit.
                # NOTE: These looped divisions accumulate floating point rounding
                # errors, but each new division pushes the rounding errors further
                # and further down in the decimals, so it doesn't matter at all.
                num /= unit_step

        return HumanBytes.PRECISION_FORMATS[precision].format("-" if is_negative else "", num, unit)


def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == name:
            ls.append(p)
    return ls


def check_terrariumpi_stopped():
    running = len(find_procs_by_name("terrariumPI.py")) > 0
    if running:
        print("TerrariumPI is still running. Please shutdown first!")
        return False

    return True


def check_disk_space(path):
    if not path.is_file():
        print(f"File '{path}' does not exists!")
        return False

    disk_usage = psutil.disk_usage(path)
    min_space_needed = path.stat().st_size + 100 * 1024 * 1024

    if disk_usage.free - path.stat().st_size < 100 * 1024 * 1024:
        print(
            f"There is not enough disk space left. Found: {HumanBytes.format(disk_usage.free)}. Needing: {HumanBytes.format(path.stat().st_size)} (database) + {HumanBytes.format(100 * 1024 * 1024)} (spare) = {HumanBytes.format(min_space_needed)} total."
        )
        return False

    print(
        f"Found broken database at: {path.resolve()}. Size: {HumanBytes.format(path.stat().st_size)}. Remaining disk space: {HumanBytes.format(disk_usage.free)}"
    )
    return True


def check_sqlite3():
    installed = os.system("sqlite3 -version >/dev/null 2>/dev/null") == 0
    if not installed:
        print("Please install sqlite3 with the command: sudo apt install sqlite3")

    return installed


def fix_database(database):
    starttime = time.time()
    print("Running recovering database ... ")

    os.system(f'sqlite3 {database} .dump | sed "s/ROLLBACK;.*/COMMIT;/" | sqlite3 {database}.new')

    # # Delete broken db
    Path(str(database)).rename(f"{database}.broken")
    Path(f"{database}.new").rename(database)

    print(f"Recovery done in {time.time()-starttime:.2f} seconds. New database is located at: {database.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script will try to fix a broken TerrariumPI SQLite database.")
    parser.add_argument("-d", "--database", help="path to the broken database.", type=Path, default=Path(DATABASE))

    args = parser.parse_args()

    if not check_sqlite3():
        exit()

    if not check_terrariumpi_stopped():
        exit()

    if not check_disk_space(args.database):
        exit()

    go = input("Would you like to continue to fix your database? Enter 'yes' to start. Anything else will abort.\n")
    if go.lower() != "yes":
        exit(0)

    fix_database(args.database)
