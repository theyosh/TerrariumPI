from datetime import datetime, timedelta
from pony import orm
import uuid
import re
from pathlib import Path
from cryptography.fernet import Fernet

from terrariumUtils import terrariumUtils

import copy

db = orm.Database()

@db.on_connect(provider='sqlite')
def sqlite_speedups(db, connection):
    cursor = connection.cursor()
    cursor.execute('PRAGMA synchronous  = OFF')
    cursor.execute('PRAGMA journal_mode = MEMORY')
    cursor.execute('PRAGMA temp_store   = MEMORY')

def init(version):
  db.bind(provider='sqlite', filename='terrariumpi.db', create_db=True)
  db.generate_mapping(create_tables=True)
  create_defaults(version)

@orm.db_session
def create_defaults(version):
  setting_defaults = [
    {'id' : 'version',                    'value' : f'{version}'},
    {'id' : 'host',                       'value' : '0.0.0.0'},
    {'id' : 'port',                       'value' : '8090'},
    {'id' : 'pi_wattage',                 'value' : '5'},
    {'id' : 'username',                   'value' : 'admin'},
    {'id' : 'password',                   'value' : terrariumUtils.generate_password('password')},
    {'id' : 'profile_image',              'value' : 'static/assets/img/profile_image.jpg'},
    {'id' : 'always_authenticate',        'value' : 'false'},
    {'id' : 'weather_source',             'value' : ''},
    {'id' : 'language',                   'value' : 'EN'},
    {'id' : 'title',                      'value' : 'TerrariumPI'},
    {'id' : 'exclude_ids',                'value' : ''},
    {'id' : 'power_price',                'value' : '0'},
    {'id' : 'water_price',                'value' : '0'},
    {'id' : 'meross_cloud_username',      'value' : ''},
    {'id' : 'meross_cloud_password',      'value' : ''},
    {'id' : 'wind_speed_indicator',       'value' : 'km/h'},
    {'id' : 'temperature_indicator',      'value' : 'celsius'},
    {'id' : 'distance_indicator',         'value' : 'cm'},
    {'id' : 'water_volume_indicator',     'value' : 'l'},
    {'id' : 'show_min_max_gauge',         'value' : 'false'},
    {'id' : 'hide_environment_dashboard', 'value' : 'false'},
    {'id' : 'all_gauges_on_single_page',  'value' : 'false'},
    {'id' : 'graph_smooth_value',         'value' : '0'},
    {'id' : 'encryption_salt',            'value' : Fernet.generate_key().decode()},
  ]

  for setting in setting_defaults:
    try:
      Setting(**setting)
      orm.commit()
    except orm.core.TransactionIntegrityError:
      # Setting is already in the database. Ignore
      pass


class Area(db.Entity):

  __VALID_TYPES = ['lights','watertank'] # + All sensor types....

  id        = orm.PrimaryKey(str, default=terrariumUtils.generate_uuid)
  enclosure = orm.Required(lambda: Enclosure)
  name      = orm.Required(str)
  type      = orm.Required(str)
  mode      = orm.Required(str)
  setup     = orm.Required(orm.Json)

  state     = orm.Optional(orm.Json)

  def __repr__(self):
    return f'Area {self.type} {self.name} in {self.mode} modus, part of {self.enclosure}'

class Audiofile(db.Entity):

  id         = orm.PrimaryKey(str)
  name       = orm.Required(str)
  filename   = orm.Required(str, unique=True)
  duration   = orm.Required(float)
  filesize   = orm.Required(float)

  playlists  = orm.Set(lambda: Playlist)

  def before_delete(self):
    filename = Path(self.filename)
    if filename.exists():
      filename.unlink()
      print(f'Deleted file {filename}')

  def __repr__(self):
    return f'Audio file {self.name}'


class Button(db.Entity):

  __MAX_VALUE_AGE = 65 * 60  # Max age of the last measurement in minutes

  id          = orm.PrimaryKey(str)
  hardware    = orm.Required(str)
  name        = orm.Required(str)
  address     = orm.Required(str)

  calibration = orm.Optional(orm.Json)

  history     = orm.Set('ButtonHistory')

  enclosure   = orm.Optional(lambda: Enclosure)

  @property
  def value(self):
    timestamp_limit = datetime.now() - timedelta(seconds=Button.__MAX_VALUE_AGE)
    value = self.history.filter(lambda h: h.timestamp >= timestamp_limit).order_by(orm.desc(ButtonHistory.timestamp)).first()
    if value:
      return value.value

    return None

  @property
  def error(self):
    return True if self.value is None else False

  def update(self, new_value, force = False):
    if new_value is None:
      return

    if force or new_value != self.value:
      button_data = ButtonHistory(
        button    = self,
        timestamp = datetime.now(),
        value     = new_value
      )

      return button_data

  def __repr__(self):
    return f'{self.hardware} button \'{self.name}\' at address \'{self.address}\''


class ButtonHistory(db.Entity):

  button    = orm.Required('Button')
  timestamp = orm.Required(datetime)
  value     = orm.Required(float)

  orm.PrimaryKey(button, timestamp)


class Enclosure(db.Entity):

  id          = orm.PrimaryKey(str, default=terrariumUtils.generate_uuid)
  name        = orm.Required(str)

  image       = orm.Optional(str)
  description = orm.Optional(str)

  areas       = orm.Set(lambda: Area)
  doors       = orm.Set(lambda: Button)
  webcams     = orm.Set(lambda: Webcam)

  def __rename_image(self):
    regex = re.compile(f'{self.id}\.(jpg|jpeg|gif|png)$',re.IGNORECASE)
    if not regex.search(self.image):
      image = Path(self.image)
      image_name = f'{image.parent}/{self.id}{image.suffix}'
      image.rename(image_name)
      print(f'Renamed from {self.image} to {image_name}')
      self.image = str(image_name)

  def before_insert(self):
    self.__rename_image()

  def before_update(self):
    self.__rename_image()

  def before_delete(self):
    image = Path(self.image)
    if image.exists():
      image.unlink()
      print(f'Deleted file {image}')

  def __repr__(self):
    return f'Enclosure {self.name} with {len(self.areas)} areas'


class NotificationMessage(db.Entity):
  id         = orm.PrimaryKey(str)
  title      = orm.Required(str)
  message    = orm.Required(str)
  rate_limit = orm.Optional(int, default=0)
  enabled    = orm.Required(bool, default=True)
  services   = orm.Set(lambda: NotificationService)

class NotificationService(db.Entity):

  id         = orm.PrimaryKey(str, default=terrariumUtils.generate_uuid)
  type       = orm.Required(str)
  name       = orm.Required(str)
  rate_limit = orm.Optional(int, default=0)
  enabled    = orm.Required(bool, default=True)
  setup      = orm.Required(orm.Json)
  messages   = orm.Set(lambda: NotificationMessage)

  def __encrypt_sensitive_fields(self):
    # encryption_salt = Setting['encryption_salt'].value.encode()
    # encryption = Fernet(encryption_salt)

    # Encrypt sensitive fields
    for field in ['username','password','user_key','access_secret']:
      if field in self.setup:
        self.setup[field] = encryptterrariumUtilsion.encrypt(self.setup[field])

  def before_insert(self):
    self.__encrypt_sensitive_fields()

  def before_update(self):
    self.__encrypt_sensitive_fields()

  def to_dict(self,only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False):
    data = copy.deepcopy(super().to_dict(only, exclude, with_collections, with_lazy, related_objects))
    # encryption_salt = Setting['encryption_salt'].value.encode()
    # encryption = Fernet(encryption_salt)
    # Encrypt sensitive fields
    for field in ['username','password','user_key','access_secret']:
      if field in data['setup']:
        data['setup'][field] = terrariumUtils.decrypt(data['setup'][field])

       # encryption.decrypt(data['setup'][field].encode()).decode()

    return data

  def __repr__(self):
    return f'Notification service {self.type} {self.name}'


class Playlist(db.Entity):

  id      = orm.PrimaryKey(str, default=terrariumUtils.generate_uuid)
  name    = orm.Required(str)

  volume  = orm.Optional(float, default=80)

  shuffle = orm.Optional(bool, default=False)
  repeat  = orm.Optional(bool, default=False)

  files   = orm.Set(lambda: Audiofile)

  @property
  def length(self):
    return self.files.count()

  @property
  def duration(self):
    return orm.sum(audiofile.duration for audiofile in self.files)

  def __repr__(self):
    return f'Playlist {self.name} with {len(self.files)} files'

class Relay(db.Entity):
  __MAX_VALUE_AGE = 65 * 60  # Max age of the last measurement in minutes

  id          = orm.PrimaryKey(str)
  hardware    = orm.Required(str)
  name        = orm.Required(str)
  address     = orm.Required(str)

  wattage     = orm.Optional(float, default=0)
  flow        = orm.Optional(float, default=0)

  manual_mode = orm.Optional(bool, default=False)
  replacement = orm.Optional(datetime, default=datetime.fromtimestamp(0))

  calibration = orm.Optional(orm.Json)

  history     = orm.Set('RelayHistory')

  @property
  def value(self):
    timestamp_limit = datetime.now() - timedelta(seconds=Relay.__MAX_VALUE_AGE)
    value = self.history.filter(lambda h: h.timestamp >= timestamp_limit).order_by(orm.desc(RelayHistory.timestamp)).first()
    if value:
      return value.value

    return None

  @property
  def error(self):
    return True if self.value is None else False

  @property
  def is_dimmer(self):
    return self.hardware.endswith('-dimmer')

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
    return 'dimmer' if self.is_dimmer else 'relay'

  def update(self, new_value, force = False):
    if new_value is None:
      return None

    if force or new_value != self.value:
      relay_data = RelayHistory(
        relay     = self,
        timestamp = datetime.now(),

        value     = new_value,
        wattage   = (new_value / 100.0) * self.wattage,
        flow      = (new_value / 100.0) * self.flow
      )

      return relay_data

  def __repr__(self):
    return f'{self.hardware} {self.type} named \'{self.name}\' at address \'{self.address}\''


class RelayHistory(db.Entity):

  relay     = orm.Required('Relay')
  timestamp = orm.Required(datetime)
  value     = orm.Required(float)
  wattage   = orm.Required(float)
  flow      = orm.Required(float)

  orm.PrimaryKey(relay, timestamp)


class Sensor(db.Entity):

  __MAX_VALUE_AGE = 5 * 60 # Max age of the last measurement in minutes
  __VALUE_MODE = 2         # Mode 1: Only store first value. Mode 2: Store average value. Mode 3: Store last value.

  id       = orm.PrimaryKey(str)
  hardware = orm.Required(str)
  type     = orm.Required(str)
  name     = orm.Required(str)
  address  = orm.Required(str)

  limit_min = orm.Optional(float, default = 0)
  limit_max = orm.Optional(float, default = 100)
  alarm_min = orm.Optional(float, default = 0)
  alarm_max = orm.Optional(float, default = 100)
  max_diff  = orm.Optional(float, default = 0)


  #offset    = orm.Optional(float, default = 0)

  exclude_avg = orm.Required(bool, default = False)

  calibration = orm.Optional(orm.Json)

  history = orm.Set('SensorHistory')

  @property
  def offset(self):
    return 0 if self.calibration is None else self.calibration.get('offset', 0)

  @property
  def alarm(self):
    if self.error:
      return False

    return not self.alarm_min <= self.value <= self.alarm_max

  @property
  def value(self):
    timestamp_limit = datetime.now() - timedelta(seconds=Sensor.__MAX_VALUE_AGE)
    value = self.history.filter(lambda h: h.timestamp >= datetime.now() - timedelta(seconds=Sensor.__MAX_VALUE_AGE)).order_by(orm.desc(SensorHistory.timestamp)).first()
    if value:
      return value.value

    return None

  @property
  def error(self):
    return True if self.value is None else False

  def update(self, value):
    if value is None:
      return

    # TODO: Make some insert or update construction. Now we have always 2 queries per update, should be nice to reduce to one.
    timestamp = datetime.now().replace(second=0,microsecond=0)
    sensor_data = self.history.filter(lambda h: h.timestamp == timestamp).first()

    # We have already a value measured for this minute, so we are done!
    if sensor_data and self.__VALUE_MODE == 1:
      return sensor_data

    if (sensor_data):
      # Mode 2 will take previous value and current and average it.
      # Mode 3 will just overwrite existing value

      sensor_data.value     = value          if self.__VALUE_MODE == 3 else (sensor_data.value + value)  / 2
      sensor_data.limit_min = self.limit_min if self.__VALUE_MODE == 3 else (sensor_data.limit_min + self.limit_min) / 2
      sensor_data.limit_max = self.limit_max if self.__VALUE_MODE == 3 else (sensor_data.limit_max + self.limit_max) / 2
      sensor_data.alarm_min = self.alarm_min if self.__VALUE_MODE == 3 else (sensor_data.alarm_min + self.alarm_min) / 2
      sensor_data.alarm_max = self.alarm_max if self.__VALUE_MODE == 3 else (sensor_data.alarm_max + self.alarm_max) / 2
    else:
      # New data
      sensor_data = SensorHistory(
        sensor    = self,
        timestamp = timestamp,

        value     = value,
        limit_min = self.limit_min,
        limit_max = self.limit_max,
        alarm_min = self.alarm_min,
        alarm_max = self.alarm_max
      )

    return sensor_data

  def __repr__(self):
    return f'{self.hardware} {self.type} named \'{self.name}\' at address \'{self.address}\''


class SensorHistory(db.Entity):
  sensor    = orm.Required('Sensor')

  timestamp = orm.Required(datetime)
  value     = orm.Required(float)
  limit_min = orm.Required(float)
  limit_max = orm.Required(float)
  alarm_min = orm.Required(float)
  alarm_max = orm.Required(float)

  orm.PrimaryKey(sensor, timestamp)

  @property
  def alarm():
    if self.value is None:
      return False

    return not self.alarm_min <= self.value <= self.alarm_max


class Setting(db.Entity):
  id    = orm.PrimaryKey(str)
  value = orm.Optional(str)

  def __encrypt_sensitive_fields(self):
    if self.id in ['meross_cloud_username','meross_cloud_password'] and '' != self.value:
#      print(f'Encrypt field {self.id} with value: {self.value}')
      self.value = terrariumUtils.encrypt(self.value)
#      print(f'Encrypted data is: {self.value}')

    # # encryption_salt = Setting['encryption_salt'].value.encode()
    # # encryption = Fernet(encryption_salt)

    # # Encrypt sensitive fields
    # for field in ['username','password','user_key','access_secret']:
    #   if field in self.setup:
    #     self.setup[field] = terrariumUtilsion.encrypt(self.setup[field])

  def before_insert(self):
    self.__encrypt_sensitive_fields()

  def before_update(self):
    self.__encrypt_sensitive_fields()


class Webcam(db.Entity):

  id               = orm.PrimaryKey(str)
  hardware         = orm.Required(str)
  name             = orm.Required(str)
  address          = orm.Required(str)

  width            = orm.Required(int)
  height           = orm.Required(int)

  rotation         = orm.Required(str)
  awb              = orm.Required(str)

  archive          = orm.Optional(str)
  archive_door     = orm.Optional(str)
  archive_light    = orm.Optional(str)

  motion_boxes     = orm.Optional(str)
  motion_threshold = orm.Optional(int)
  motion_area      = orm.Optional(int)
  motion_frame     = orm.Optional(str)

  markers          = orm.Optional(orm.Json, default=[])

  enclosure        = orm.Optional(lambda: Enclosure)

  @property
  def is_live(self):
    return self.hardware.endswith('-live')

  @property
  def archive_path(self):
    return f'webcam/archive/{self.id}'

  def __repr__(self):
    return f'{self.hardware} webcam \'{self.name}\' at address \'{self.address}\''


# This will allow us to convert the data to JSON....
# not needed, as this will also give out schema... so to_dict is enough
# with db.set_perms_for(Setting, Sensor, SensorHistory):
#  orm.perm('view', group='anybody')
