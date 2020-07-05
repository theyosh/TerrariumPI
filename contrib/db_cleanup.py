"""
 Run this script in the contrib folder with the same python version as TerrariumPI

 python3 db_cleanup.py
"""

import sqlite3
from datetime import datetime, timedelta
import time
import math
import subprocess
import shutil
import os
import requests

def humansize(nbytes):
  suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  i = 0
  while nbytes >= 1024 and i < len(suffixes)-1:
    nbytes /= 1024.
    i += 1
  f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
  return '%s %s' % (f, suffixes[i])

class HistoryCleanup():

  def __init__(self, database = '../history.db', period = timedelta(weeks = 60), batch = 1000):
    self.database = database
    self.new_database = self.database.replace('.db','.new.db')
    self.period = period
    self.delete_batch = batch
    self.timestamp_limit = int((datetime.now() - period).timestamp())

    self.db = sqlite3.connect(self.database)
    with self.db as db:
      cur = db.cursor()
      cur.execute('PRAGMA journal_mode = MEMORY')
      cur.execute('PRAGMA temp_store = MEMORY')

    self.db.row_factory = sqlite3.Row
    self.get_current_db_version()

    self.new_db = sqlite3.connect(self.new_database)
    with self.new_db as db:
      cur = db.cursor()
      cur.execute('PRAGMA journal_mode = MEMORY')
      cur.execute('PRAGMA temp_store = MEMORY')
      cur.execute('PRAGMA user_version = {}'.format(self.version))

  def get_current_db_version(self):
    self.version = 0
    with self.db as db:
      cur = db.cursor()
      self.version = int(cur.execute('PRAGMA user_version').fetchall()[0][0])

  def check_free_storage(self):
    diskstats = shutil.disk_usage(self.database)
    filesize = os.path.getsize(self.database)
    print('Database size: {}, free diskspace: {}'.format(humansize(filesize),humansize(diskstats[2])))
    if filesize > diskstats[0]:
      print('Not enough space left for cleaning the database. We need at least {}'.format(humansize(filesize)))
      exit(1)

  def check_offline(self):
    try:
      data = requests.get('http://localhost:8090/api/system')
      if data.status_code == 200:
        print('TerrariumPI is still running. Please shutdown first, else you will get data corruption.')
        exit(1)
    except requests.ConnectionError:
      pass

  def get_total_records(self, table, period = None):
    with self.db as db:
      sql = 'SELECT count(*) as total, MIN(timestamp) as begin, MAX(timestamp) as end FROM {}'.format(table)
      filter = ()
      if period is not None:
        sql += ' WHERE timestamp < ?'
        filter = (self.timestamp_limit,)

      cur = db.cursor()

      for row in cur.execute(sql, filter):
        return (row['total'],row['begin'],row['end'])

  def get_clean_up_records(self,table):
    return self.get_total_records(table,self.period)

  def get_space_back(self):
    start = time.time()
    print('Start reclaming lost space. This will rebuild the database and give all the delete space back. This will take a lot of time')

    source = subprocess.Popen(['/usr/bin/sqlite3', self.database, '.dump'],
                        stdout=subprocess.PIPE,
                        )

    destination = subprocess.Popen(['/usr/bin/sqlite3',self.new_database],
                        stdin=source.stdout,
                        stdout=subprocess.PIPE,
                        )

    while source.returncode is None:
      source.poll()
      print('.',end='',flush=True)
      time.sleep(1)

    while destination.returncode is None:
      destination.poll()
      print('.',end='',flush=True)
      time.sleep(1)

    if not (source.returncode == 0 and destination.returncode == 0):
      print('Error cleaning up deleted space. Looks like database corruption...')
      exit(1)

    print('Done in {}'.format(time.time()-start))

  def __clean_up(self, table):
    print('Starting cleaning up table \'{}\'. Deleting data older then {} in batches of {} records. This could take some time...'.format(table, datetime.now() - self.period,self.delete_batch))

    start = time.time()
    print('Total rows:', end='', flush=True)
    total_sensor_data = self.get_total_records(table)
    print(' {} from {} till {}. Took ({})'.format(total_sensor_data[0],
                                                  datetime.utcfromtimestamp(total_sensor_data[1]),
                                                  datetime.utcfromtimestamp(total_sensor_data[2]),
                                                  time.time()-start))
    start = time.time()
    print('Clean up rows:',end='', flush=True)
    total_cleanup_data = self.get_clean_up_records(table)

    if total_cleanup_data[0] == 0:
      print(' No data, nothing to do!')
      return

    print(' {} from {} till {}. Took ({})'.format(total_cleanup_data[0],
                                                  datetime.utcfromtimestamp(total_cleanup_data[1]),
                                                  datetime.utcfromtimestamp(total_cleanup_data[2]),
                                                  time.time()-start))

    start = time.time()
    delete_steps = math.ceil( total_cleanup_data[0] / self.delete_batch)
    print('Removing {} rows ({}%) of data in {} steps of {} rows.'.format(total_cleanup_data[0], (total_cleanup_data[0]/total_sensor_data[0]) * 100,delete_steps, self.delete_batch))
    print('0%',end='',flush=True)
    new_percentage = 10

    sql = 'DELETE FROM {} WHERE timestamp < ? LIMIT {}'.format(table, self.delete_batch)
    filter = (self.timestamp_limit,)

    for step in range(delete_steps):
      if int( (step / delete_steps) * 100) == new_percentage:
        print('{}%'.format(new_percentage),end='',flush=True)
        new_percentage += 10

      print('.',end='',flush=True)

      with self.db as db:
        cur = db.cursor()
        cur.execute(sql,filter)

    print('100%')
    print('Clean up is done in {}'.format(time.time()-start))

  def move_db(self):
    shutil.move(self.database,self.database.replace('.db','.db.old'))
    shutil.move(self.new_database, self.database)

  def clean_up_sensors(self):
    self.__clean_up('sensor_data')

  def clean_up_doors(self):
    self.__clean_up('door_data')

  def clean_up_weather(self):
    self.__clean_up('weather_data')

  def clean_up_status(self):
    self.__clean_up('system_data')


print('This script will cleanup your history.db file. We will keep 60 weeks of data from now. If you want to make a backup first, please enter no and make your backup.')

cleanup = HistoryCleanup()
cleanup.check_free_storage()
cleanup.check_offline()

go = input('Would you like to continue? Enter yes to start. Anything else will abort.\n')
if go.lower() != 'yes':
  exit(0)

cleanup.clean_up_sensors()
cleanup.clean_up_doors()
cleanup.clean_up_weather()
cleanup.clean_up_status()

cleanup.get_space_back()
cleanup.move_db()

print('Database is now cleaned and should be reduced in size:')
cleanup.check_free_storage()
print('Restart TerrariumPI and check if the sensor graphs still working. If it is al working, remove the file {}'.format(cleanup.database.replace('.db','.db.old')))
