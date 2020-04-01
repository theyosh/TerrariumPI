# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import sqlite3
import time
import copy
import os

from terrariumUtils import terrariumUtils

class terrariumCollector(object):
  DATABASE = 'history.db'
  # Store data every Xth minute. Except switches and doors
  STORE_MODULO = 1 * 60

  def __init__(self,versionid):
    logger.info('Setting up collector database %s' % (terrariumCollector.DATABASE,))
    self.__recovery = False
    self.__connect()
    self.__create_database_structure()
    self.__upgrade(int(versionid.replace('.','')))
    logger.info('TerrariumPI Collecter is ready')

  def __connect(self):
    self.db = sqlite3.connect(terrariumCollector.DATABASE)
    # https://www.whoishostingthis.com/compare/sqlite/optimize/
    with self.db as db:
      cur = db.cursor()
      cur.execute('PRAGMA journal_mode = MEMORY')
      cur.execute('PRAGMA temp_store = MEMORY')
      # Line below is not safe for a Pi. As this can/will corrupt the database when the Pi crashes....
      # cur.execute('PRAGMA synchronous = OFF')

    self.db.row_factory = sqlite3.Row
    logger.info('Database connection created to database %s' % (terrariumCollector.DATABASE,))

  def __create_database_structure(self):
    with self.db as db:
      cur = db.cursor()
      cur.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                      (id VARCHAR(50),
                       type VARCHAR(15),
                       timestamp INTEGER(4),
                       current FLOAT(4),
                       limit_min FLOAT(4),
                       limit_max FLOAT(4),
                       alarm_min FLOAT(4),
                       alarm_max FLOAT(4),
                       alarm INTEGER(1))''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS sensor_data_unique ON sensor_data(id,type,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_timestamp ON sensor_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_avg ON sensor_data(type,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_id ON sensor_data(id,timestamp ASC)')

      cur.execute('''CREATE TABLE IF NOT EXISTS switch_data
                      (id VARCHAR(50),
                       timestamp INTEGER(4),
                       state INTERGER(1),
                       power_wattage FLOAT(2),
                       water_flow FLOAT(2))''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS switch_data_unique ON switch_data(id,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS switch_data_timestamp ON switch_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS switch_data_id ON switch_data(id,timestamp ASC)')

      cur.execute('''CREATE TABLE IF NOT EXISTS door_data
                      (id INTEGER(4),
                       timestamp INTEGER(4),
                       state TEXT CHECK( state IN ('open','closed') ) NOT NULL DEFAULT 'closed')''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS door_data_unique ON door_data(id,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS door_data_timestamp ON door_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS door_data_id ON door_data(id,timestamp ASC)')

      cur.execute('''CREATE TABLE IF NOT EXISTS weather_data
                      (timestamp INTEGER(4),
                       wind_speed FLOAT(4),
                       temperature FLOAT(4),
                       pressure FLOAT(4),
                       wind_direction VARCHAR(50),
                       weather VARCHAR(50),
                       icon VARCHAR(50))''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS weather_data_unique ON weather_data(timestamp ASC)')


      cur.execute('''CREATE TABLE IF NOT EXISTS system_data
                       (timestamp INTEGER(4),
                       load_load1 FLOAT(4),
                       load_load5 FLOAT(4),
                       load_load15 FLOAT(4),
                       uptime INTEGER(4),
                       temperature FLOAT(4),
                       cores VARCHAR(25),
                       memory_total INTEGER(6),
                       memory_used INTEGER(6),
                       memory_free INTEGER(6),
                       disk_total INTEGER(6),
                       disk_used INTEGER(6),
                       disk_free INTEGER(6))''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS system_data_unique ON system_data(timestamp ASC)')

    db.commit()

  def __upgrade(self,to_version):
    # Set minimal version to 3.0.0
    current_version = 300
    table_upgrades = {'310' : ['ALTER TABLE system_data ADD COLUMN disk_total INTEGER(6)',
                               'ALTER TABLE system_data ADD COLUMN disk_used INTEGER(6)',
                               'ALTER TABLE system_data ADD COLUMN disk_free INTEGER(6)'],

                      '380' : ['DROP INDEX IF EXISTS sensor_data_type',
                               'CREATE INDEX IF NOT EXISTS sensor_data_avg ON sensor_data (type, timestamp ASC)',
                               'DROP INDEX IF EXISTS sensor_data_id',
                               'CREATE INDEX IF NOT EXISTS sensor_data_id ON sensor_data (id, timestamp ASC)',
                               'DROP INDEX IF EXISTS switch_data_id',
                               'CREATE INDEX IF NOT EXISTS switch_data_id ON switch_data (id, timestamp ASC)',
                               'DROP INDEX IF EXISTS door_data_id',
                               'CREATE INDEX IF NOT EXISTS door_data_id ON door_data (id, timestamp ASC)']}

    try:
      with open('.collector.update.{}.sql'.format('393'),'r') as sql_file:
        table_upgrades['393'] = [line.strip() for line in sql_file.readlines()]

      os.remove('.collector.update.{}.sql'.format('393'))
      logger.warning('There are {} sensors that have an updated ID and needs to be renamed in the database. This can take a lot of time! Please wait...'
                     .format(len(table_upgrades['393'])/2))

    except IOError as ex:
      # No updates... just ignore
      pass

    with self.db as db:
      cur = db.cursor()
      db_version = int(cur.execute('PRAGMA user_version').fetchall()[0][0])
      if db_version > current_version:
        current_version = db_version

    if current_version == to_version:
      logger.info('Collector database is up to date')
    elif current_version < to_version:
      logger.info('Collector database is out of date. Running updates from %s to %s' % (current_version,to_version))
      # Execute updates
      with self.db as db:
        cur = db.cursor()
        for update_version in table_upgrades:
          if current_version < int(update_version) <= to_version:
            # Execute all updates between the versions
            for sql_upgrade in table_upgrades[update_version]:
              try:
                cur.execute(sql_upgrade)
                logger.info('Collector database upgrade for version %s succeeded! %s' % (update_version,sql_upgrade))
              except Exception as ex:
                if 'duplicate column name' not in str(ex):
                  logger.error('Error updating collector database. Please contact support. Error message: %s' % (ex,))

            if '380' == update_version:
              self.__upgrade_to_380()

        db.commit()
        if int(to_version) % 10 == 0:
          logger.warning('Cleaning up disk space. This will take a couple of minutes depending on the database size and sd card disk speed.')
          filesize = os.path.getsize(terrariumCollector.DATABASE)
          speed = 2 # MBps
          duration = filesize / 1024.0 / 1024.0 / speed
          logger.warning('Current database is {} in size and with a speed of {}MBps it will take {} to complete'.format(terrariumUtils.format_filesize(filesize),speed,terrariumUtils.format_uptime(duration)))
          cur.execute('VACUUM')

        cur.execute('PRAGMA user_version = ' + str(to_version))
        logger.info('Updated collector database. Set version to: %s' % (to_version,))

      db.commit()

  def __upgrade_to_380(self):
    # This update will remove 'duplicate' records that where added for better graphing... This will now be done at the collecting the data
    tables = ['door_data','switch_data']

    with self.db as db:
      for table in tables:
        cur = db.cursor()
        data = cur.execute('SELECT id, timestamp, state FROM ' + table + ' ORDER BY id ASC, timestamp ASC')
        data = data.fetchall()

        prev_state = None
        prev_id = None
        for row in data:
          if prev_id is None:
            prev_id = row['id']

          elif prev_id != row['id']:
            prev_id = row['id']
            prev_state = None

          if prev_state is None:
            prev_state = row['state']
            continue

          if row['state'] == prev_state:
            cur.execute('DELETE FROM ' + table + ' WHERE id = ? AND timestamp = ? AND state = ?', (row['id'],row['timestamp'],row['state']))

          prev_state = row['state']
          prev_id = row['id']

        db.commit()
      logger.info('Collector database upgrade for version 3.8.0 succeeded! Removed duplicate records')

  def __recover(self):
    starttime = time.time()
    # Based on: http://www.dosomethinghere.com/2013/02/20/fixing-the-sqlite-error-the-database-disk-image-is-malformed/
    # Enable recovery status
    self.__recovery = True
    logger.warn('TerrariumPI Collecter recovery mode is starting! %s', (self.__recovery,))

    # Create empty sql dump variable
    sqldump = ''
    lines = 0
    with open('.recovery.sql', 'w') as f:
      # Dump SQL data line for line
      for line in self.db.iterdump():
        lines += 1
        sqldump += line + "\n"
        f.write('%s\n' % line)

    logger.warn('TerrariumPI Collecter recovery mode created SQL dump of %s lines and %s bytes!', (lines,strlen(sqldump),))

    # Delete broken db
    os.remove(terrariumCollector.DATABASE)
    logger.warn('TerrariumPI Collecter recovery mode deleted faulty database from disk %s', (terrariumCollector.DATABASE,))

    # Reconnect will recreate the db
    logger.warn('TerrariumPI Collecter recovery mode starts reconnecting database to create a new clean database at %s', (terrariumCollector.DATABASE,))
    self.__connect()
    self.__create_database_structure()
    cur = self.db.cursor()
    # Load the SQL data back to db
    cur.executescript(sqldump)
    logger.warn('TerrariumPI Collecter recovery mode restored the old data in a new database. %s', (terrariumCollector.DATABASE,))

    # Return to normal mode
    self.__recovery = False
    logger.warn('TerrariumPI Collecter recovery mode is finished in %s seconds!', (time.time()-starttime,))

  def __log_data(self,type,id,newdata):
    timer = time.time()

    if self.__recovery:
      logger.warn('TerrariumPI Collecter is in recovery mode. Cannot store new logging data!')
      return

    now = int(time.time())
    rows = []
    if type not in ['switches','door']:
      now -= (now % terrariumCollector.STORE_MODULO)

    try:
      with self.db as db:
        cur = db.cursor()

        if type in ['humidity','moisture','temperature','distance','ph','conductivity','light','uva','uvb','uvi','fertility','co2','volume']:
          cur.execute('REPLACE INTO sensor_data (id, type, timestamp, current, limit_min, limit_max, alarm_min, alarm_max, alarm) VALUES (?,?,?,?,?,?,?,?,?)',
                      (id, type, now, newdata['current'], newdata['limit_min'], newdata['limit_max'], newdata['alarm_min'], newdata['alarm_max'], newdata['alarm']))

        if type in ['weather']:
          cur.execute('REPLACE INTO weather_data (timestamp, wind_speed, temperature, pressure, wind_direction, weather, icon) VALUES (?,?,?,?,?,?,?)',
                      (now, newdata['wind_speed'], newdata['temperature'], newdata['pressure'], newdata['wind_direction'], newdata['weather'], newdata['icon']))

        if type in ['system']:
          cur.execute('REPLACE INTO system_data (timestamp, load_load1, load_load5, load_load15, uptime, temperature, cores, memory_total, memory_used, memory_free, disk_total, disk_used, disk_free) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (now, newdata['load']['load1'], newdata['load']['load5'], newdata['load']['load15'], newdata['uptime'], newdata['temperature'], newdata['cores'], newdata['memory']['total'], newdata['memory']['used'], newdata['memory']['free'],newdata['disk']['total'], newdata['disk']['used'], newdata['disk']['free']))

        if type in ['switches']:
          if 'time' in newdata:
            now = newdata['time']

          cur.execute('REPLACE INTO switch_data (id, timestamp, state, power_wattage, water_flow) VALUES (?,?,?,?,?)',
                      (id, now, newdata['state'], newdata['current_power_wattage'], newdata['current_water_flow']))

        if type in ['door']:
          cur.execute('REPLACE INTO door_data (id, timestamp, state) VALUES (?,?,?)',
                      (id, now, newdata))

        db.commit()
    except sqlite3.DatabaseError as ex:
      logger.error('TerrariumPI Collecter exception! %s', (ex,))
      if 'database disk image is malformed' == str(ex):
        self.__recover()

    logger.debug('Timing: updating %s data in %s seconds.' % (type,time.time()-timer))

  def stop(self):
    self.db.close()
    logger.info('Shutdown data collector')

  def get_total_power_water_usage(self):
    timer = time.time()

    totals = {'power_wattage' : {'duration' : 0 , 'wattage' : 0.0},
              'water_flow'    : {'duration' : 0 , 'water'   : 0.0}}

    sql = '''SELECT SUM(total_wattage) AS Watt, SUM(total_water) AS Water, MAX(timestamp2)-MIN(timestamp) AS TotalTime FROM (
                SELECT
                    t1.timestamp as timestamp,
                    t2.timestamp as timestamp2,
                    t2.timestamp-t1.timestamp AS duration_in_seconds,
                   (t2.timestamp-t1.timestamp)          * t1.power_wattage AS total_wattage,
                  ((t2.timestamp-t1.timestamp) / 60.0)  * t1.water_flow AS total_water
                FROM switch_data AS t1
                LEFT JOIN switch_data AS t2
                ON t2.id = t1.id
                AND t2.timestamp = (SELECT MIN(timestamp) FROM switch_data WHERE timestamp > t1.timestamp AND id = t1.id)
                WHERE t1.state > 0)'''

    with self.db as db:
      cur = db.cursor()
      cur.execute(sql)
      row = cur.fetchone()
      if row['TotalTime'] is not None and row['Watt'] is not None:
        totals = {'power_wattage' : {'duration' : int(row['TotalTime']) , 'wattage' : float(row['Watt'])},
                  'water_flow'    : {'duration' : int(row['TotalTime']) , 'water'   : float(row['Water'])}}

    logger.debug('Timing: Total power and water usage calculation done in %s seconds.' % ((time.time() - timer),))
    return totals

  def log_switch_data(self,data):
    if data['hardwaretype'] not in ['pwm-dimmer','remote-dimmer','dc-dimmer']:
      # Store normal switches with value 100 indicating full power (aka no dimming)
      data['state'] = (100 if data['state'] == 1 else 0)

    self.__log_data('switches',data['id'],data)

  def log_door_data(self,data):
    self.__log_data('door',data['id'], data['state'])

  def log_weather_data(self,data):
    self.__log_data('weather',None,data)

  def log_sensor_data(self,data):
    self.__log_data(data['type'],data['id'],data)

  def log_system_data(self, data):
    self.__log_data('system',None,data)

  def get_history(self, parameters = [], starttime = None, stoptime = None, exclude_ids = None):
    # Default return object
    timer = time.time()
    history = {}
    periods = {'day' : 1 * 24,
               'week' : 7 * 24,
               'month' : 30 * 24,
               'year' : 365 * 24,
               'all' : 3650 * 24}
    modulo = terrariumCollector.STORE_MODULO

    logtype = parameters[0]
    del(parameters[0])

    # Define start time
    if starttime is None:
      starttime = int(time.time())

    # Define stop time
    if stoptime is None:
      stoptime = starttime - (24 * 60 * 60)

    if len(parameters) > 0 and parameters[-1] in periods:
      stoptime = starttime - periods[parameters[-1]] * 60 * 60
      modulo = (periods[parameters[-1]] / 24) * terrariumCollector.STORE_MODULO
      del(parameters[-1])

    sql = ''
    filters = (stoptime,starttime,)
    if logtype == 'sensors':
      fields = { 'current' : [], 'alarm_min' : [], 'alarm_max' : [] , 'limit_min' : [], 'limit_max' : []}
      sql = 'SELECT id, type, timestamp,' + ', '.join(list(fields.keys())) + ' FROM sensor_data WHERE timestamp >= ? AND timestamp <= ?'

      if len(parameters) > 0 and parameters[0] == 'average':
        sql = 'SELECT "average" AS id, type, timestamp'
        for field in fields:
          sql = sql + ', AVG(' + field + ') as ' + field
        sql = sql + ' FROM sensor_data WHERE timestamp >= ? AND timestamp <= ?'

        if exclude_ids is not None:
          sql = sql + ' AND sensor_data.id NOT IN (\'' + '\',\''.join(exclude_ids) +'\')'

        if len(parameters) == 2:
          sql = sql + ' AND type = ?'
          filters = (stoptime,starttime,parameters[1],)

        sql = sql + ' GROUP BY type, timestamp'

      elif len(parameters) == 2 and parameters[0] in ['temperature','humidity','distance','ph','conductivity','light','uva','uvb','uvi','fertility']:
        sql = sql + ' AND type = ? AND id = ?'
        filters = (stoptime,starttime,parameters[0],parameters[1],)
      elif len(parameters) == 1 and parameters[0] in ['temperature','humidity','distance','ph','conductivity','light','uva','uvb','uvi','fertility']:
        sql = sql + ' AND type = ?'
        filters = (stoptime,starttime,parameters[0],)

      elif len(parameters) == 1:
        sql = sql + ' AND id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'switches':
      fields = { 'power_wattage' : [], 'water_flow' : [] }
      sql = '''SELECT id, "switches" AS type, timestamp, timestamp2, state, ''' + ', '.join(list(fields.keys())) + ''' FROM (
                 SELECT
                   t1.id AS id,
                   t1.timestamp AS timestamp,
                   IFNULL(t2.timestamp, ''' + str(starttime) + ''') as timestamp2,
                   t1.power_wattage AS power_wattage,
                   t1.water_flow AS water_flow,
                   t1.state AS state
                 FROM switch_data AS t1
                 LEFT JOIN switch_data AS t2
                 ON t2.id = t1.id
                 AND t2.timestamp = (SELECT MIN(timestamp) FROM switch_data WHERE switch_data.timestamp > t1.timestamp AND switch_data.id = t1.id) )
              WHERE timestamp2 > IFNULL((SELECT MAX(timestamp) AS timelimit FROM switch_data AS ttable WHERE ttable.id = id AND ttable.timestamp < ?),0)
              AND   timestamp <= ?'''

      if len(parameters) > 0 and parameters[0] is not None:
        sql = sql + ' AND id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'doors':
      fields = {'state' : []}
      sql = '''SELECT id, "doors" AS type, timestamp, timestamp2, (CASE WHEN state == 'open' THEN 1 ELSE 0 END) AS state FROM (
                 SELECT
                   t1.id AS id,
                   t1.timestamp AS timestamp,
                   IFNULL(t2.timestamp, ''' + str(starttime) + ''') as timestamp2,
                   t1.state AS state
                 FROM door_data AS t1
                 LEFT JOIN door_data AS t2
                 ON t2.id = t1.id
                 AND t2.timestamp = (SELECT MIN(timestamp) FROM door_data WHERE door_data.timestamp > t1.timestamp AND door_data.id = t1.id) )
              WHERE timestamp2 > IFNULL((SELECT MAX(timestamp) AS timelimit FROM door_data AS ttable WHERE ttable.id = id AND ttable.timestamp < ?),0)
              AND   timestamp <= ?'''

      if len(parameters) > 0 and parameters[0] is not None:
        sql = sql + ' AND id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'weather':
      fields = { 'wind_speed' : [], 'temperature' : [], 'pressure' : [] , 'wind_direction' : [], 'rain' : [],
                 'weather' : [], 'icon' : []}
      sql = 'SELECT "city" AS id, "weather" AS type, timestamp, ' + ', '.join(list(fields.keys())) + ' FROM weather_data WHERE timestamp >= ? AND timestamp <= ?'

    elif logtype == 'system':
      fields = ['load_load1', 'load_load5','load_load15','uptime', 'temperature','cores', 'memory_total', 'memory_used' , 'memory_free', 'disk_total', 'disk_used' , 'disk_free']

      if len(parameters) > 0 and parameters[0] == 'load':
        fields = ['load_load1', 'load_load5','load_load15']
      elif len(parameters) > 0 and parameters[0] == 'cores':
        fields = ['cores']
      elif len(parameters) > 0 and parameters[0] == 'uptime':
        fields = ['uptime']
      elif len(parameters) > 0 and parameters[0] == 'temperature':
        fields = ['temperature']
      elif len(parameters) > 0 and parameters[0] == 'memory':
        fields = ['memory_total', 'memory_used' , 'memory_free']
      elif len(parameters) > 0 and parameters[0] == 'disk':
        fields = ['disk_total', 'disk_used' , 'disk_free']

      sql = 'SELECT "system" AS type, timestamp, ' + ', '.join(fields) + ' FROM system_data WHERE timestamp >= ? AND timestamp <= ?'

    sql = sql + ' ORDER BY timestamp ASC, type ASC' + (', id ASC' if logtype != 'system' else '')

    if not self.__recovery:
      try:
        first_item = None
        with self.db as db:
          cur = db.cursor()
          for row in cur.execute(sql, filters):
            if row['type'] not in history:
              history[row['type']] = {}

            if logtype == 'system':
              for field in fields:
                system_parts = field.split('_')
                if system_parts[0] not in history[row['type']]:
                  history[row['type']][system_parts[0]] = {} if len(system_parts) == 2 else []

                if len(system_parts) == 2:
                  if system_parts[1] not in history[row['type']][system_parts[0]]:
                    history[row['type']][system_parts[0]][system_parts[1]] = []

                  history[row['type']][system_parts[0]][system_parts[1]].append([row['timestamp'] * 1000,row[field]])
                else:
                  history[row['type']][system_parts[0]].append([row['timestamp'] * 1000,row[field]])

            else:
              if row['id'] not in history[row['type']]:
                history[row['type']][row['id']] = copy.deepcopy(fields)

                if row['type'] in ['switches','doors']:
                  history[row['type']][row['id']]['totals'] = {'duration' : 0, 'power_wattage' : 0, 'water_flow' : 0}

              if row['type'] in ['switches','doors'] and row['state'] > 0 and row['timestamp2'] is not None and '' != row['timestamp2']:
                # Update totals data
                duration = float(row['timestamp2'] - (row['timestamp'] if row['timestamp'] >= stoptime else stoptime))
                history[row['type']][row['id']]['totals']['duration'] += duration

                if 'switches' == row['type']:
                  history[row['type']][row['id']]['totals']['power_wattage'] += duration * float(row['power_wattage'])
                  # Devide by 60 to get Liters water used per minute based on seconds durations
                  history[row['type']][row['id']]['totals']['water_flow'] += (duration / 60.0) * float(row['water_flow'])

              for field in fields:
                history[row['type']][row['id']][field].append([ (row['timestamp'] if row['timestamp'] >= stoptime else stoptime) * 1000,row[field]])

                if row['type'] in ['switches','doors'] and row['timestamp2'] is not None and '' != row['timestamp2']:
                  # Add extra point for nicer graphing of doors and power switches
                  history[row['type']][row['id']][field].append([row['timestamp2'] * 1000,row[field]])

          logger.debug('Timing: history %s query: %s seconds' % (logtype,time.time()-timer))
      except sqlite3.DatabaseError as ex:
        logger.error('TerrariumPI Collecter exception! %s', (ex,))
        if 'database disk image is malformed' == str(ex):
          self.__recover()

    # In order to get nicer graphs, we are adding a start and end time based on the selected time range if needed
    if logtype in ['switches','doors'] and logtype not in history and len(parameters) > 0:
      # Create 'empty' history array if single id is requested
      history[logtype] = {}
      history[logtype][parameters[0]] = copy.deepcopy(fields)
      for field in fields:
        history[logtype][parameters[0]][field].append([stoptime  * 1000,0])
        history[logtype][parameters[0]][field].append([starttime * 1000,0])

    return history
