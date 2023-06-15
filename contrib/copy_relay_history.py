import argparse
import configparser
import sqlite3
from time import time
from pathlib import Path


def read_sensor_settings(config_file):
    settings = configparser.ConfigParser(interpolation=None)
    settings.read(config_file)

    relays = []
    for section in settings.sections():
        if not section.startswith("switch"):
            continue

        relays.append(
            {
                "id": settings[section]["id"],
                "type": settings[section]["hardwaretype"],
                "name": settings[section]["name"],
                "address": settings[section]["address"],
                "replacement": None
                if "last_replacement_date" not in settings[section]
                or "2019-01-01" == settings[section]["last_replacement_date"]
                else settings[section]["last_replacement_date"],
            }
        )

    return relays


def find_new_relays(relay_data, db):
    new_relays = []

    db = sqlite3.connect(db)
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    for relay in relay_data:
        relay["address"] = "%" + relay["address"] + "%"
        relay["type"] = relay["type"].replace("pwm-dimmer", "nextevo-dimmer")

        cur.execute(
            "select id, name, address, hardware from Relay where hardware = :type and address LIKE :address", relay
        )
        data = cur.fetchall()
        if len(data) == 1:
            # We are sure we have found the correct relay.
            new_relays.append(
                {
                    "old_id": relay["id"],
                    "new_id": data[0]["id"],
                    "name": data[0]["name"],
                    "type": data[0]["hardware"],
                    "address": data[0]["address"],
                    "replacement": relay["replacement"],
                }
            )

    return new_relays


def convert_data(relay_data, old_db, new_db):
    new_db = sqlite3.connect(new_db)
    new_db.row_factory = sqlite3.Row
    new_cur = new_db.cursor()

    # Attach old db as source for getting the old data
    new_cur.execute(f'attach "{old_db}" as source')

    for relay in relay_data:
        start = time()
        print(f'Relay \'{relay["name"]}\' of type \'{relay["type"]}\' at address \'{relay["address"]}\'', end=" ... ")

        # Set the last replacement date based on the old sstop-final-sigtermettings.cfg file
        if relay["replacement"] is not None:
            relay["replacement"] = f'{relay["replacement"]} 12:00:00.000000'
            new_cur.execute(
                "UPDATE Relay SET replacement = :replacement WHERE id = :id",
                {"replacement": relay["replacement"], "id": relay["new_id"]},
            )
            new_db.commit()

        # Copy the relay data records from old db into new db.
        new_cur.execute(
            f"""INSERT OR IGNORE INTO RelayHistory (relay, timestamp, value, wattage, flow)
                        SELECT '{relay["new_id"]}' as relay, datetime(timestamp, 'unixepoch'), state, power_wattage, water_flow FROM source.switch_data WHERE id = '{relay["old_id"]}' """
        )

        new_db.commit()

        print(f"Done in {time()-start:.2f} seconds. Copied {new_cur.rowcount} records.")

    print("All relay history data is copied. You can now start TerrariumPI again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TerrariumPI Relay history converter.")

    parser.add_argument("old_config", type=Path, help="The path to the TerrariumPI v3 settings.cfg file")
    parser.add_argument("old_database", type=Path, help="The path to the TerrariumPI v3 history.db file")
    parser.add_argument("new_database", type=Path, help="The path to the TerrariumPI v4 terrariumpi.db file")

    args = parser.parse_args()

    old_relays = read_sensor_settings(args.old_config)
    new_relays = find_new_relays(old_relays, args.new_database)

    missing_relays = len(new_relays) != len(old_relays)

    print(
        f"Found {len(new_relays)} out of {len(old_relays)} are found. Below is a summary of the founded relays that can converted.\n"
    )
    for relay in new_relays:
        print(
            f'Relay \'{relay["name"]}\' of type \'{relay["type"]}\' at address \'{relay["address"]}\'. Old ID: {relay["old_id"]} => New ID: {relay["new_id"]}'
        )

    if missing_relays:
        print("\nThe following relays could not be found:")

        new_keys = [relay["old_id"] for relay in new_relays]
        for relay in old_relays:
            if relay["id"] in new_keys:
                continue

            print(f'Relay \'{relay["name"]}\' of type \'{relay["type"]}\' at address \'{relay["address"][1:-1]}\'.')

    print("\nIf you are happy with this setup, you can continue with the conversion. This will take a lot of time....")
    yes = input("Enter 'yes' to continue. Anything else will abort.: ")

    if "yes" == yes.strip().lower():
        print("")
        convert_data(new_relays, args.old_database, args.new_database)

    else:
        print("Aborted!")
