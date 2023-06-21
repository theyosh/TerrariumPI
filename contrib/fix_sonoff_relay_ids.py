#!/usr/bin/env python

import sqlite3
from pathlib import Path
import psutil
import shutil
from hashlib import md5
import json

DATABASE = Path("../data/terrariumpi.db")


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


# Check available disk space and database size.
available_disk_space = psutil.disk_usage("/").free
if available_disk_space < 2.5 * DATABASE.stat().st_size:
    exit(
        f"Not enough free space on disk. Found {sizeof_fmt(available_disk_space)}, needs at least {sizeof_fmt(2.5 * DATABASE.stat().st_size)}"
    )

# Backup existing database first
backup_files = ["terrariumpi.db", "terrariumpi.db-shm", "terrariumpi.db-wal"]
backup_folder = Path("../data/db_backup")
backup_folder.mkdir(exist_ok=True)

for backup_file in backup_files:
    backup_file = "../data/" + backup_file
    if Path(backup_file).exists():
        shutil.copy(backup_file, str(backup_folder))

# Connect to database
database = sqlite3.connect(DATABASE)
database.row_factory = sqlite3.Row

# Get all the sonoff relays
with database:
    relays = database.execute('SELECT id, hardware, name, address FROM Relay WHERE hardware = "sonoff"').fetchall()

    print(f"Found {len(relays)} sonoff relays which ID has to be checked and renumbered")
    for relay in relays:
        old_id = relay["id"]
        new_id = md5(f'{relay["hardware"]}{relay["address"]}'.encode()).hexdigest()
        if old_id != new_id:
            # Rename Relay ID
            database.execute("UPDATE Relay SET id = ? WHERE id = ?", (new_id, old_id))
            print(f'Renamed the ID for relay {relay["name"]}. Old ID {old_id} vs New ID {new_id}')

            print("Start updating Relay History")
            database.execute("UPDATE RelayHistory SET relay = ? WHERE relay = ?", (new_id, old_id))
            print("Done updating Relay History")

            areas = database.execute("SELECT id, name, setup FROM Area WHERE setup LIKE ?", (f"%{old_id}%",)).fetchall()
            print(f"Update {len(areas)} enclosure areas")
            for area in areas:
                print(f'Update enclosure area \'{area["name"]}\'')
                # Load enclosure data and try to update the JSON setup field
                setup = json.loads(area["setup"])

                area_parts = ["day", "night", "low", "high"]
                relay_tweaks = ["delay_off", "delay_on"]

                for area_part in area_parts:
                    try:
                        if old_id in setup[area_part]["relays"]:
                            # Fix relays in the area
                            setup[area_part]["relays"].remove(old_id)
                            setup[area_part]["relays"].append(new_id)

                            # Update relay tweaks
                            for relay_tweak in relay_tweaks:
                                if setup[area_part].get(f"relay_{relay_tweak}_{old_id}", None):
                                    setup[area_part][f"relay_{relay_tweak}_{new_id}"] = setup[area_part][
                                        f"relay_{relay_tweak}_{old_id}"
                                    ]
                                    del setup[area_part][f"relay_{relay_tweak}_{old_id}"]

                    except Exception as ex:
                        print(ex)

                database.execute("UPDATE Area SET setup = ? where id = ?", (json.dumps(setup), area["id"]))
                print(f'Area {area["name"]} is updated with new relay ids')

            # Done areas

        print(f'Done updating relay {relay["name"]}')

    print("Fully renumbered all Sonoff relays!")
