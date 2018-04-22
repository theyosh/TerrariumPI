# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import sqlite3
import time
import json
import copy
import os

class terrariumCollector():
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
    self.db.row_factory = sqlite3.Row
    logger.info('Database connection created to database %s' % (terrariumCollector.DATABASE,))

  def __create_database_structure(self):
    with self.db:
      cur = self.db.cursor()
      cur.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                      (id VARCHAR(50),
                       type VARCHAR(15),
                       timestamp INTEGER(4),
                       current FLOAT(4),
                       limit_min FLOAT(4),
                       limit_max FLOAT(4),
                       alarm_min FLOAT(4),
                       alarm_max FLOAT(4),
                       alarm INTEGER(1) )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS sensor_data_unique ON sensor_data(id,type,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_timestamp ON sensor_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_type ON sensor_data(type)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_id ON sensor_data(id)')

      cur.execute('''CREATE TABLE IF NOT EXISTS switch_data
                      (id VARCHAR(50),
                       timestamp INTEGER(4),
                       state INTERGER(1),
                       power_wattage FLOAT(2),
                       water_flow FLOAT(2)
                        )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS switch_data_unique ON switch_data(id,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS switch_data_timestamp ON switch_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS switch_data_id ON switch_data(id)')

      cur.execute('''CREATE TABLE IF NOT EXISTS door_data
                      (id INTEGER(4),
                       timestamp INTEGER(4),
                       state TEXT CHECK( state IN ('open','closed') ) NOT NULL DEFAULT 'closed'
                       )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS door_data_unique ON door_data(id,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS door_data_timestamp ON door_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS door_data_id ON door_data(id)')

      cur.execute('''CREATE TABLE IF NOT EXISTS weather_data
                      (timestamp INTEGER(4),
                       wind_speed FLOAT(4),
                       temperature FLOAT(4),
                       pressure FLOAT(4),
                       wind_direction VARCHAR(50),
                       weather VARCHAR(50),
                       icon VARCHAR(50)
                        )''')

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
                       disk_free INTEGER(6)
                        )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS system_data_unique ON system_data(timestamp ASC)')

    self.db.commit()

  def __upgrade(self,to_version):
    # Set minimal version to 3.0.0
    current_version = 300
    table_upgrades = {'310' : ['ALTER TABLE system_data ADD COLUMN disk_total INTEGER(6)',
                               'ALTER TABLE system_data ADD COLUMN disk_used INTEGER(6)',
                               'ALTER TABLE system_data ADD COLUMN disk_free INTEGER(6)']}

    with self.db:
      cur = self.db.cursor()
      db_version = int(cur.execute('PRAGMA user_version').fetchall()[0][0])
      if db_version > current_version:
        current_version = db_version

    if current_version == to_version:
      logger.info('Collector database is up to date')
    elif current_version < to_version:
      logger.info('Collector database is out of date. Running updates from %s to %s' % (current_version,to_version))
      # Execute updates
      with self.db:
        cur = self.db.cursor()
        for update_version in table_upgrades.keys():
          if current_version < int(update_version) <= to_version:
            # Execute all updates between the versions
            for sql_upgrade in table_upgrades[update_version]:
              try:
                cur.execute(sql_upgrade)
                logger.info('Collector database upgrade for version %s succeeded! %s' % (update_version,sql_upgrade))
              except Exception, ex:
                if 'duplicate column name' not in str(ex):
                  logger.error('Error updating collector database. Please contact support. Error message: %s' % (ex,))

        cur.execute('VACUUM')
        cur.execute('PRAGMA user_version = ' + str(to_version))
        logger.info('Updated collector database. Set version to: %s' % (to_version,))

      self.db.commit()

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
    cur = self.db.cursor()
    # Load the SQL data back to db
    cur.executescript(sqldump)
    logger.warn('TerrariumPI Collecter recovery mode restored the old data in a new database. %s', (terrariumCollector.DATABASE,))

    # Return to normal mode
    self.__recovery = False
    logger.warn('TerrariumPI Collecter recovery mode is finished in %s seconds!', (time.time()-starttime,))

  def __log_data(self,type,id,newdata):
    if self.__recovery:
      logger.warn('TerrariumPI Collecter is in recovery mode. Cannot store new logging data!')
      return

    now = int(time.time())
    rows = []
    if type not in ['switches','door']:
      now -= (now % terrariumCollector.STORE_MODULO)

    try:
      with self.db:
        cur = self.db.cursor()

        if type in ['humidity','moisture','temperature','distance','ph']:
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

          # Make a duplicate of last state and save it with 1 sec back in time to smooth the graphs
          cur.execute('''REPLACE INTO switch_data (id,timestamp,state,power_wattage,water_flow)
                          SELECT id, ? as curtimestamp,state,power_wattage,water_flow
                          FROM switch_data
                          WHERE id = ? ORDER BY timestamp DESC LIMIT 1''', (now-1, id))

          cur.execute('REPLACE INTO switch_data (id, timestamp, state, power_wattage, water_flow) VALUES (?,?,?,?,?)',
                      (id, now, newdata['state'], newdata['power_wattage'], newdata['water_flow']))

        if type in ['door']:
          # Make a duplicate of last state and save it with 1 sec back in time to smooth the graphs
          cur.execute('''REPLACE INTO door_data (id,timestamp,state)
                          SELECT id, ? as curtimestamp,state
                          FROM door_data
                          WHERE id = ? ORDER BY timestamp DESC LIMIT 1''', (now-1, id))

          cur.execute('REPLACE INTO door_data (id, timestamp, state) VALUES (?,?,?)',
                      (id, now, newdata))

        self.db.commit()
    except sqlite3.DatabaseError as ex:
      logger.error('TerrariumPI Collecter exception! %s', (ex,))
      if 'database disk image is malformed' == str(ex):
        self.__recover()

  def __calculate_power_and_water_usage(self,history):
    if 'switches' not in history:
      return

    now = int(time.time()) * 1000
    for switchid in history['switches']:
      # First add a new element to all the data arrays with the current timestamp. This is needed for:
      # - Better power usage calculation
      # - Better graphs in the interface
      history['switches'][switchid]['power_wattage'].append([now,history['switches'][switchid]['power_wattage'][-1][1]])
      history['switches'][switchid]['water_flow'].append([now,history['switches'][switchid]['water_flow'][-1][1]])
      history['switches'][switchid]['state'].append([now,history['switches'][switchid]['state'][-1][1]])

      totals = {'power_wattage' : {'duration' : 0.0 , 'wattage' : 0.0},
                'water_flow'    : {'duration' : 0.0 , 'water'   : 0.0}}
      power_on_time = None
      for counter,state in enumerate(history['switches'][switchid]['state']):
        if state[1] > 0 and power_on_time is None: # Power went on! The value could be variable from zero to 100. Above zero is 'on'
          power_on_time = counter
        elif power_on_time is not None: # Now check if the power went off, or put on a second time...
          power_wattage_start = history['switches'][switchid]['power_wattage'][power_on_time][1] * (history['switches'][switchid]['state'][power_on_time][1] / 100.0)
          power_wattage_end = history['switches'][switchid]['power_wattage'][counter][1] * (state[1] / 100.0)
          power_wattage = (power_wattage_start + power_wattage_end) / 2.0

          water_flow_start = history['switches'][switchid]['water_flow'][power_on_time][1] * (history['switches'][switchid]['state'][power_on_time][1] / 100.0)
          water_flow_end = history['switches'][switchid]['water_flow'][counter][1] * (state[1] / 100.0)
          water_flow = (water_flow_start + water_flow_end) / 2.0

          duration = (state[0] - history['switches'][switchid]['state'][power_on_time][0]) / 1000.0 # Devide by 1000 because history is using Javascript timestamps

          totals['power_wattage']['duration'] += duration
          totals['power_wattage']['wattage'] += (duration * power_wattage)

          totals['water_flow']['duration'] += duration
          totals['water_flow']['water'] += (duration * (water_flow / 60)) # Water flow is in Liter per minute. So devide by 60 to get per seconds

          if state[1] == 0:
            power_on_time = None # Power went down. Reset so we can measure new period
          else:
            power_on_time = counter # Change in power useage (dimmer)

        # Here we change the wattage and water flow to zero if the switch was off. This is needed for drawing the right graphs
        if state[1] == 0:
          history['switches'][switchid]['power_wattage'][counter][1] = 0
          history['switches'][switchid]['water_flow'][counter][1] = 0
        else:
          history['switches'][switchid]['power_wattage'][counter][1] *= (state[1] / 100.0)
          history['switches'][switchid]['water_flow'][counter][1] *= (state[1] / 100.0)

      history['switches'][switchid]['totals'] = totals

  def __calculate_door_usage(self,history):
    if 'doors' not in history:
      return

    now = int(time.time()) * 1000
    for doorid in history['doors']:
      history['doors'][doorid]['state'].append([now,history['doors'][doorid]['state'][-1][1]])

      totals = {'duration': 0}
      door_open_on_time = None
      for counter,state in enumerate(history['doors'][doorid]['state']):
        if state[1] != 'closed' and door_open_on_time is None: # Door went open!
          door_open_on_time = counter
        elif state[1] == 'closed' and door_open_on_time is not None: # Door is closed. Calc period and data
          totals['duration'] += (state[0] - history['doors'][doorid]['state'][door_open_on_time][0]) / 1000.0 # Devide by 1000 because history is using Javascript timestamps
          door_open_on_time = None # Reset so we can measure new period

        # Here we translate closed to zero and open to one. Else the graphs will not work
        history['doors'][doorid]['state'][counter][1] = (0 if state[1] == 'closed' else 1)

      history['doors'][doorid]['totals'] = totals

  def stop(self):
    self.db.close()
    logger.info('Shutdown data collector')

  def log_switch_data(self,data):
    if data['hardwaretype'] not in ['pwm-dimmer','remote-dimmer']:
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

  def get_history(self, parameters = [], starttime = None, stoptime = None):
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

    if len(parameters) > 0 and parameters[-1] in periods.keys():
      stoptime = starttime - periods[parameters[-1]] * 60 * 60
      modulo = (periods[parameters[-1]] / 24) * terrariumCollector.STORE_MODULO
      del(parameters[-1])

    sql = ''
    filters = (stoptime,starttime,)
    if logtype == 'sensors':
      fields = { 'current' : [], 'alarm_min' : [], 'alarm_max' : [] , 'limit_min' : [], 'limit_max' : []}
      sql = 'SELECT id, type, timestamp,' + ', '.join(fields.keys()) + ' FROM sensor_data WHERE timestamp >= ? and timestamp <= ?'

      if len(parameters) > 0 and parameters[0] == 'average':
        sql = 'SELECT "average" as id, type, timestamp'
        for field in fields:
          sql = sql + ', AVG(' + field + ') as ' + field
        sql = sql + ' FROM sensor_data WHERE timestamp >= ? and timestamp <= ?'

        if len(parameters) == 2:
          sql = sql + ' and type = ?'
          filters = (stoptime,starttime,parameters[1],)

        sql = sql + ' GROUP BY type, timestamp'

      elif len(parameters) == 2 and parameters[0] in ['temperature','humidity','distance','ph']:
        sql = sql + ' and type = ? and id = ?'
        filters = (stoptime,starttime,parameters[0],parameters[1],)
      elif len(parameters) == 1 and parameters[0] in ['temperature','humidity','distance','ph']:
        sql = sql + ' and type = ?'
        filters = (stoptime,starttime,parameters[0],)

      elif len(parameters) == 1:
        sql = sql + ' and id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'switches':
      fields = { 'power_wattage' : [], 'water_flow' : [] , 'state' : []}
      sql = 'SELECT id, "switches" as type, timestamp, ' + ', '.join(fields.keys()) + ' FROM switch_data WHERE timestamp >= ? and timestamp <= ? '
      if len(parameters) > 0 and parameters[0] is not None:
        sql = sql + ' and id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'doors':
      fields = { 'state' : []}
      sql = 'SELECT id, "doors" as type, timestamp, ' + ', '.join(fields.keys()) + ' FROM door_data WHERE timestamp >= ? and timestamp <= ? '

      if len(parameters) > 0 and parameters[0] is not None:
        sql = sql + ' and id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'weather':
      fields = { 'wind_speed' : [], 'temperature' : [], 'pressure' : [] , 'wind_direction' : [], 'rain' : [],
                 'weather' : [], 'icon' : []}
      sql = 'SELECT "city" as id, "weather" as type, timestamp, ' + ', '.join(fields.keys()) + ' FROM weather_data WHERE timestamp >= ? and timestamp <= ?'

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

      sql = 'SELECT "system" as type, timestamp, ' + ', '.join(fields) + ' FROM system_data WHERE timestamp >= ? and timestamp <= ?'

    sql = sql + ' ORDER BY timestamp ASC'

    rows = []
    if not self.__recovery:
      try:
        with self.db:
          cur = self.db.cursor()
          cur.execute(sql, filters)
          rows = cur.fetchall()
          logger.debug('TerrariumPI Collecter history query:  %s seconds, %s records -> %s, %s' % (time.time()-timer,len(rows),sql,filters))
      except sqlite3.DatabaseError as ex:
        logger.error('TerrariumPI Collecter exception! %s', (ex,))
        if 'database disk image is malformed' == str(ex):
          self.__recover()

    for row in rows:
      if logtype == 'switches' and len(row) == len(fields)+1:
        for field in fields:
          history[field] = row[field]

        return history

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

        for field in fields:
          history[row['type']][row['id']][field].append([row['timestamp'] * 1000,row[field]])

    if logtype == 'switches':
      self.__calculate_power_and_water_usage(history)
    elif logtype == 'doors':
      self.__calculate_door_usage(history)

    return history
