# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pony import orm
from yoyo import read_migrations
from yoyo import get_backend
from dotenv import dotenv_values
from pathlib import Path
from terrariumUtils import terrariumUtils

import copy
import re
import sqlite3
import time

DATABASE = "data/terrariumpi.db"
ADVANCED_SETTINGS_FILE = "data/.database-env"

db = orm.Database()


@db.on_connect(provider="sqlite")
def sqlite_speedups(db, connection):
    settings = {
        "auto_vacuum": "NONE",
        "cache_size": -10000,
        "journal_mode": "WAL",
        "synchronous": "OFF",
        "temp_store": "MEMORY",
    }

    settings = {**settings, **load_advanced_settings()}
    cursor = connection.cursor()
    for key, value in settings.items():
        cursor.execute(f"PRAGMA {key}  = {value}")


def init(version):
    backend = get_backend(f"sqlite:///{DATABASE}")
    migrations = read_migrations("migrations")

    with backend.lock():
        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))

    db.bind(provider="sqlite", filename=DATABASE)
    db.generate_mapping()
    create_defaults(version)


@orm.db_session
def create_defaults(version):
    setting_defaults = [
        {"id": "version", "value": f"{version}"},
        {"id": "host", "value": "0.0.0.0"},
        {"id": "port", "value": "8090"},
        {"id": "pi_wattage", "value": "5"},
        {"id": "username", "value": "admin"},
        {"id": "password", "value": terrariumUtils.generate_password("password")},
        {"id": "profile_image", "value": "img/terrariumpi.jpg"},
        {"id": "always_authenticate", "value": "0"},
        {"id": "weather_source", "value": ""},
        {"id": "language", "value": "en_US"},
        {"id": "currency", "value": "eur"},
        {"id": "title", "value": "TerrariumPI"},
        {"id": "exclude_ids", "value": ""},
        {"id": "power_price", "value": "0"},
        {"id": "water_price", "value": "0"},
        {"id": "meross_cloud_username", "value": ""},
        {"id": "meross_cloud_password", "value": ""},
        {"id": "wind_speed_indicator", "value": "km/h"},
        {"id": "temperature_indicator", "value": "celsius"},
        {"id": "distance_indicator", "value": "cm"},
        {"id": "water_volume_indicator", "value": "l"},
        {"id": "show_min_max_gauge", "value": "false"},
        {"id": "dashboard_mode", "value": "0"},
        {"id": "all_gauges_on_single_page", "value": "false"},
        {"id": "graph_smooth_value", "value": "0"},
        {"id": "auto_dark_mode", "value": "0"},
    ]

    for setting in setting_defaults:
        try:
            Setting(**setting)
            orm.commit()
        except orm.core.TransactionIntegrityError:
            # Setting is already in the database. Ignore
            pass


def load_advanced_settings():
    if Path(ADVANCED_SETTINGS_FILE).exists():
        return dotenv_values(ADVANCED_SETTINGS_FILE)

    return {}


def recover():
    starttime = time.time()

    # Based on: http://www.dosomethinghere.com/2013/02/20/fixing-the-sqlite-error-the-database-disk-image-is-malformed/
    def progress(status, remaining, total):
        status = ((total - remaining) / total) * 100

        print(f"Copied {total-remaining}({status:.2f}%) of {total} pages...")

    broken_db = sqlite3.connect(DATABASE)
    new_db = sqlite3.connect(f"{DATABASE}.new")

    with new_db:
        broken_db.backup(new_db, pages=10, progress=progress)

    new_db.close()
    broken_db.close()

    # Delete broken db
    Path(DATABASE).unlink()
    Path(f"{DATABASE}.new").rename(DATABASE)

    print(f"Recovery done in {time.time()-starttime:.2f} seconds")

    # Reinitialize the new database
    # init(version)
    return True


class Area(db.Entity):
    __VALID_TYPES = ["lights", "watertank"]  # + All sensor types....

    id = orm.PrimaryKey(str, default=terrariumUtils.generate_uuid)
    enclosure = orm.Required(lambda: Enclosure)
    name = orm.Required(str)
    type = orm.Required(str)
    mode = orm.Required(str)
    setup = orm.Required(orm.Json)

    state = orm.Optional(orm.Json)

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False):
        return copy.deepcopy(super().to_dict(only, exclude, with_collections, with_lazy, related_objects))

    def __repr__(self):
        return f"Area {self.type} {self.name} in {self.mode} mode, part of {self.enclosure}"


class Audiofile(db.Entity):
    id = orm.PrimaryKey(str)
    name = orm.Required(str)
    filename = orm.Required(str, unique=True)
    duration = orm.Required(float)
    filesize = orm.Required(float)

    playlists = orm.Set(lambda: Playlist)

    def before_delete(self):
        filename = Path(self.filename)
        if filename.exists():
            filename.unlink()

    def __repr__(self):
        return f"Audio file {self.name}"


class Button(db.Entity):
    __MAX_VALUE_AGE = 65 * 60  # Max age of the last measurement in minutes

    id = orm.PrimaryKey(str)
    hardware = orm.Required(str)
    name = orm.Required(str)
    address = orm.Required(str)

    calibration = orm.Optional(orm.Json)

    history = orm.Set("ButtonHistory")

    enclosure = orm.Optional(lambda: Enclosure)

    @property
    def value(self):
        timestamp_limit = datetime.now() - timedelta(seconds=Button.__MAX_VALUE_AGE)
        value = (
            self.history.filter(lambda h: h.timestamp >= timestamp_limit)
            .order_by(orm.desc(ButtonHistory.timestamp))
            .first()
        )
        if value:
            return value.value

        return None

    @property
    def error(self):
        return True if self.value is None else False

    def update(self, new_value, force=False):
        if new_value is None:
            return

        if force or new_value != self.value:
            button_data = ButtonHistory(button=self, timestamp=datetime.now(), value=new_value)

            return button_data

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False):
        data = copy.deepcopy(super().to_dict(only, exclude, with_collections, with_lazy, related_objects))
        # Add extra fields
        data["value"] = self.value
        data["error"] = self.error

        return data

    def __repr__(self):
        return f"{self.hardware} button '{self.name}' at address '{self.address}'"


class ButtonHistory(db.Entity):
    button = orm.Required("Button")
    timestamp = orm.Required(datetime)
    value = orm.Required(float)

    orm.PrimaryKey(button, timestamp)


class Enclosure(db.Entity):
    id = orm.PrimaryKey(str, default=terrariumUtils.generate_uuid)
    name = orm.Required(str)

    image = orm.Optional(str)
    description = orm.Optional(str)

    areas = orm.Set(lambda: Area)
    doors = orm.Set(lambda: Button)
    webcams = orm.Set(lambda: Webcam)

    def __rename_image(self):
        regex = re.compile(f"{self.id}\.(jpg|jpeg|gif|png)$", re.IGNORECASE)
        if "" != self.image and not regex.search(self.image):
            image = Path(self.image)
            image_name = f"{image.parent}/{self.id}{image.suffix}"
            image.rename(image_name)
            self.image = str(image_name)

    def delete_image(self):
        image = Path(self.image)
        if image.exists() and image.is_file():
            image.unlink()

    # Pony DB Hooks
    def before_insert(self):
        self.__rename_image()

    def before_update(self):
        self.__rename_image()

    def before_delete(self):
        self.delete_image()

    def __repr__(self):
        return f"Enclosure {self.name} with {len(self.areas)} areas"


class NotificationMessage(db.Entity):
    id = orm.PrimaryKey(str)
    type = orm.Required(str)
    title = orm.Required(str)
    message = orm.Required(str)
    rate_limit = orm.Optional(int, default=0)
    enabled = orm.Required(bool, default=True)
    services = orm.Set(lambda: NotificationService)


class NotificationService(db.Entity):
    id = orm.PrimaryKey(str, default=terrariumUtils.generate_uuid)
    type = orm.Required(str)
    name = orm.Required(str)
    rate_limit = orm.Optional(int, default=0)
    enabled = orm.Required(bool, default=True)
    setup = orm.Required(orm.Json)
    messages = orm.Set(lambda: NotificationMessage)

    def __encrypt_sensitive_fields(self):
        # Encrypt sensitive fields
        for field in ["username", "password", "user_key", "access_secret"]:
            if field in self.setup:
                self.setup[field] = terrariumUtils.encrypt(self.setup[field])

    def before_insert(self):
        self.__encrypt_sensitive_fields()

    def before_update(self):
        self.__encrypt_sensitive_fields()

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False):
        data = copy.deepcopy(super().to_dict(only, exclude, with_collections, with_lazy, related_objects))
        # Encrypt sensitive fields
        for field in ["username", "password", "user_key", "access_secret"]:
            if field in data["setup"]:
                data["setup"][field] = terrariumUtils.decrypt(data["setup"][field])

        return data

    def __repr__(self):
        return f"Notification service {self.type} {self.name}"


class Playlist(db.Entity):
    id = orm.PrimaryKey(str, default=terrariumUtils.generate_uuid)
    name = orm.Required(str)

    volume = orm.Optional(float, default=80)

    shuffle = orm.Optional(bool, default=False)
    repeat = orm.Optional(bool, default=False)

    files = orm.Set(lambda: Audiofile)

    @property
    def length(self):
        return self.files.count()

    @property
    def duration(self):
        return orm.sum(audiofile.duration for audiofile in self.files)

    def __repr__(self):
        return f"Playlist {self.name} with {len(self.files)} files"


class Relay(db.Entity):
    __MAX_VALUE_AGE = 65 * 60  # Max age of the last measurement in minutes

    id = orm.PrimaryKey(str)
    hardware = orm.Required(str)
    name = orm.Required(str)
    address = orm.Required(str)

    wattage = orm.Optional(float, default=0)
    flow = orm.Optional(float, default=0)

    manual_mode = orm.Optional(bool, default=False)
    replacement = orm.Optional(datetime, default=datetime.fromtimestamp(0))

    calibration = orm.Optional(orm.Json)

    history = orm.Set("RelayHistory")

    webcam = orm.Optional(lambda: Webcam)

    @property
    def value(self):
        value = (
            self.history.filter(lambda h: h.timestamp >= datetime.now() - timedelta(seconds=Relay.__MAX_VALUE_AGE))
            .order_by(orm.desc(RelayHistory.timestamp))
            .first()
        )
        if value:
            return value.value

        return None

    @property
    def error(self):
        return True if self.value is None else False

    @property
    def is_dimmer(self):
        return self.hardware.endswith("-dimmer")

    @property
    def is_on(self):
        return self.value is not None and self.value > 0

    @property
    def is_off(self):
        return not self.is_on

    @property
    def current_wattage(self):
        if self.value is None:
            return 0

        return self.value * self.wattage / 100

    @property
    def current_flow(self):
        if self.value is None:
            return 0

        return self.value * self.flow / 100

    @property
    def type(self):
        return "dimmer" if self.is_dimmer else "relay"

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False):
        data = copy.deepcopy(super().to_dict(only, exclude, with_collections, with_lazy, related_objects))

        # Add extra fields
        data["dimmer"] = self.is_dimmer
        data["value"] = self.value
        data["replacement"] = self.replacement.timestamp()
        data["error"] = self.error

        return data

    def update(self, new_value, force=False):
        if new_value is None:
            return None

        if force or new_value != self.value:
            relay_data = RelayHistory(
                relay=self,
                timestamp=datetime.now(),
                value=new_value,
                wattage=(new_value / 100.0) * self.wattage,
                flow=(new_value / 100.0) * self.flow,
            )

            return relay_data

    def __repr__(self):
        return f"{self.hardware} {self.type} named '{self.name}' at address '{self.address}'"


class RelayHistory(db.Entity):
    relay = orm.Required("Relay")
    timestamp = orm.Required(datetime)
    value = orm.Required(float)
    wattage = orm.Required(float)
    flow = orm.Required(float)

    orm.PrimaryKey(relay, timestamp)


class Sensor(db.Entity):
    __MAX_VALUE_AGE = 5 * 60  # Max age of the last measurement in minutes
    __VALUE_MODE = 2  # Mode 1: Only store first value. Mode 2: Store average value. Mode 3: Store last value.

    id = orm.PrimaryKey(str)
    hardware = orm.Required(str)
    type = orm.Required(str)
    name = orm.Required(str)
    address = orm.Required(str)

    limit_min = orm.Optional(float, default=0)
    limit_max = orm.Optional(float, default=100)
    alarm_min = orm.Optional(float, default=0)
    alarm_max = orm.Optional(float, default=100)
    max_diff = orm.Optional(float, default=0)

    exclude_avg = orm.Required(bool, default=False)

    calibration = orm.Optional(orm.Json)

    history = orm.Set("SensorHistory")

    @property
    def offset(self):
        try:
            return float(self.calibration.get("offset", 0.0))
        except Exception:
            return 0.0

    @property
    def alarm(self):
        if self.error:
            return False

        return not self.alarm_min <= self.value <= self.alarm_max

    @property
    def value(self):
        value = (
            self.history.filter(lambda h: h.timestamp >= datetime.now() - timedelta(seconds=Sensor.__MAX_VALUE_AGE))
            .order_by(orm.desc(SensorHistory.timestamp))
            .first()
        )
        if value:
            return value.value

        return None

    @property
    def error(self):
        return True if self.value is None else False

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False):
        data = copy.deepcopy(super().to_dict(only, exclude, with_collections, with_lazy, related_objects))
        # Add extra fields
        data["value"] = self.value
        data["offset"] = self.offset
        data["alarm"] = self.alarm
        data["error"] = self.error

        return data

    def update(self, value):
        if value is None:
            return

        # TODO: Make some insert or update construction. Now we have always 2 queries per update, should be nice to reduce to one.
        timestamp = datetime.now().replace(second=0, microsecond=0)
        sensor_data = self.history.filter(lambda h: h.timestamp == timestamp).first()

        # We have already a value measured for this minute, so we are done!
        if sensor_data and self.__VALUE_MODE == 1:
            return sensor_data

        if sensor_data:
            # Mode 2 will take previous value and current and average it.
            # Mode 3 will just overwrite existing value

            sensor_data.value = value if self.__VALUE_MODE == 3 else (sensor_data.value + value) / 2
            sensor_data.limit_min = (
                self.limit_min if self.__VALUE_MODE == 3 else (sensor_data.limit_min + self.limit_min) / 2
            )
            sensor_data.limit_max = (
                self.limit_max if self.__VALUE_MODE == 3 else (sensor_data.limit_max + self.limit_max) / 2
            )
            sensor_data.alarm_min = (
                self.alarm_min if self.__VALUE_MODE == 3 else (sensor_data.alarm_min + self.alarm_min) / 2
            )
            sensor_data.alarm_max = (
                self.alarm_max if self.__VALUE_MODE == 3 else (sensor_data.alarm_max + self.alarm_max) / 2
            )

            sensor_data.exclude_avg = self.exclude_avg
        else:
            # New data
            sensor_data = SensorHistory(
                sensor=self,
                timestamp=timestamp,
                value=value,
                limit_min=self.limit_min,
                limit_max=self.limit_max,
                alarm_min=self.alarm_min,
                alarm_max=self.alarm_max,
                exclude_avg=self.exclude_avg,
            )

        return sensor_data

    def __repr__(self):
        return f"{self.hardware} {self.type} named '{self.name}' at address '{self.address}'"


class SensorHistory(db.Entity):
    sensor = orm.Required("Sensor")

    timestamp = orm.Required(datetime)
    value = orm.Required(float)
    limit_min = orm.Required(float)
    limit_max = orm.Required(float)
    alarm_min = orm.Required(float)
    alarm_max = orm.Required(float)

    exclude_avg = orm.Required(bool, default=False)

    orm.PrimaryKey(sensor, timestamp)

    @property
    def alarm(self):
        if self.value is None:
            return False

        return not self.alarm_min <= self.value <= self.alarm_max


class Setting(db.Entity):
    id = orm.PrimaryKey(str)
    value = orm.Optional(str)

    def __encrypt_sensitive_fields(self):
        if self.id in ["meross_cloud_username", "meross_cloud_password"] and "" != self.value:
            self.value = terrariumUtils.encrypt(self.value)

    def before_insert(self):
        self.__encrypt_sensitive_fields()

    def before_update(self):
        self.__encrypt_sensitive_fields()

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False):
        return copy.deepcopy(super().to_dict(only, exclude, with_collections, with_lazy, related_objects))


class Webcam(db.Entity):
    id = orm.PrimaryKey(str)
    hardware = orm.Required(str)
    name = orm.Required(str)
    address = orm.Required(str)

    width = orm.Required(int)
    height = orm.Required(int)

    rotation = orm.Required(str)
    awb = orm.Required(str)

    flash = orm.Set(lambda: Relay)

    archive = orm.Optional(orm.Json)
    motion = orm.Optional(orm.Json)

    markers = orm.Optional(orm.Json, default=[])

    enclosure = orm.Optional(lambda: Enclosure)

    @property
    def is_live(self):
        return self.hardware.endswith("-live")

    @property
    def archive_path(self):
        # TODO: Property/setting ??
        return f"webcam/archive/{self.id}"

    @property
    def raw_image(self):
        # TODO: Property/setting ??
        return f"webcam/{self.id}/{self.id}_raw.jpg"

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False):
        data = copy.deepcopy(super().to_dict(only, exclude, with_collections, with_lazy, related_objects))
        # Add extra fields
        data["archive_path"] = self.archive_path
        data["raw_image"] = self.raw_image
        data["is_live"] = self.is_live

        return data

    def __repr__(self):
        return f"{self.hardware} webcam '{self.name}' at address '{self.address}'"
