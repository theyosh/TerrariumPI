# -*- coding: utf-8 -*-
import logging
import logging.config
import zipfile
import os
from logging.handlers import TimedRotatingFileHandler
from gevent import monkey
monkey.patch_all()

class TimedCompressedRotatingFileHandler(TimedRotatingFileHandler):
  """
  Extended version of TimedRotatingFileHandler that compress logs on rollover.
  """
  def find_last_rotated_file(self):
    dir_name, base_name = os.path.split(self.baseFilename)
    file_names = os.listdir(dir_name)
    result = []
    prefix = '{}.20'.format(base_name)  # we want to find a rotated file with eg filename.2017-12-12... name
    for file_name in file_names:
      if file_name.startswith(prefix) and not file_name.endswith('.zip'):
        result.append(file_name)
    result.sort()
    return result[0]

  def doRollover(self):
    super(TimedCompressedRotatingFileHandler, self).doRollover()

    dfn = self.find_last_rotated_file()
    dfn_zipped = '{}.zip'.format(dfn)
    if os.path.exists(dfn_zipped):
      os.remove(dfn_zipped)
    with zipfile.ZipFile(dfn_zipped, 'w') as f:
      f.write(dfn, dfn_zipped, zipfile.ZIP_DEFLATED)
    os.remove(dfn)


logging.config.fileConfig('logging.cfg')
