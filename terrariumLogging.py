# -*- coding: utf-8 -*-

import logging
import logging.handlers
import logging.config

import zipfile
import codecs
import sys
import os
import os.path
import time
import glob
import shutil

from terrariumConfig import terrariumConfig
from terrariumNotification import terrariumNotification

class TimedCompressedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Extended version of TimedRotatingFileHandler that compress logs on rollover.
    """
    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """

        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        timeTuple = time.localtime(t)
        dfn = self.baseFilename + '.' + time.strftime(self.suffix, timeTuple)
        if os.path.exists(dfn):
            os.remove(dfn)

        self.stream.close()

        shutil.copyfile(os.path.realpath(self.baseFilename), os.path.abspath(dfn))
        # Empty source file for new day
        open(self.baseFilename, 'w').close()

        if self.encoding:
            self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
        else:
            self.stream = open(self.baseFilename, 'w')

        self.rolloverAt = self.rolloverAt + self.interval

        if self.backupCount > 0:
            # find the oldest log file and delete it
            s = glob.glob(self.baseFilename + '.20*')
            if len(s) > self.backupCount:
                s.sort()
                os.remove(s[0])

        if os.path.exists(dfn + '.zip'):
            os.remove(dfn + '.zip')

        log_archive = zipfile.ZipFile(dfn + '.zip', 'w')
        log_archive.write(dfn, os.path.basename(dfn), zipfile.ZIP_DEFLATED)
        log_archive.close()

        os.remove(dfn)

class NotificationLogger(logging.StreamHandler):

  def __init__(self,trafficlights,*args, **kwargs):
    super(NotificationLogger,self).__init__(*args, **kwargs)

    terrariumpi_config = terrariumConfig()
    self.notification = terrariumNotification(trafficlights,terrariumpi_config.get_profile_image(),terrariumpi_config.get_system()['version'])

  def emit(self,data):
    if data.name not in ['terrariumTranslations']:
      self.notification.message('system_' + str(data.levelname).lower() , {'message':data.getMessage()} )

if os.path.isfile('logging.custom.cfg'):
  logging.config.fileConfig('logging.custom.cfg')
else:
  logging.config.fileConfig('logging.cfg')
