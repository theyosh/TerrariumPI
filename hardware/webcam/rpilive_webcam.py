# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from gevent import sleep
from pathlib import Path
from io import BytesIO
import subprocess
import os
import signal
import psutil

from . import terrariumWebcam, terrariumWebcamLoadingException

class terrariumRPILiveWebcam(terrariumWebcam):
  HARDWARE     = 'rpicam-live'
  NAME         = 'Live Raspberry PI camera'
  VALID_SOURCE = r'^rpicam_live$'
  INFO_SOURCE  = 'rpicam_live'

  __RASPIVID = '/usr/bin/raspivid'
  __FFMPEG   = '/usr/bin/ffmpeg'

  def stop(self):
    try:
      os.killpg(os.getpgid(self.__process.pid), signal.SIGTERM)
    except Exception as ex:
      logger.debug(f'Live webcam is not running: {ex}')

    super().stop()

  def _load_hardware(self):
    if not Path(self.__RASPIVID).exists():
      raise terrariumWebcamLoadingException('Please install raspivid.')

    if not Path(self.__FFMPEG).exists():
      raise terrariumWebcamLoadingException('Please install ffmpeg.')

    if hasattr(self,'__process'):
      try:
        os.killpg(os.getpgid(self.__process.pid), signal.SIGTERM)
      except Exception as ex:
        print(f'Live webcam is not running: {ex}')
        logger.debug(f'Live webcam is not running: {ex}')

    cmd = Path(__file__).parent / 'rpilive_webcam.sh'

    width  = self.width  if self.rotation not in ['90','270'] else self.height
    height = self.height if self.rotation not in ['90','270'] else self.width

    cmd = [str(cmd), self.name, str(width), str(height), str(self.rotation), self.awb, str(Path(self._STORE_LOCATION).joinpath(self.id))]
    self.__process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, start_new_session=True)

    logger.debug(f'Started {self} with process id: {self.__process.pid} exit code: {self.__process.returncode}')

    # We need some time to wait so that the live stream has produced the first chunks
    sleep(5)

    return True

  def _get_raw_data(self):
    if not psutil.pid_exists(self.__process.pid):
      # Should restart the bash script
      logger.warning(f'Webcam {self} is crashed. Restarting the webcam.')
      self._load_hardware()
      return False

    url = f'{Path(self._STORE_LOCATION).joinpath(self.id)}/stream.m3u8'
    cmd = [self.__FFMPEG, '-hide_banner', '-loglevel', 'panic', '-i', url, '-vframes', '1', '-f', 'image2', '-']

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False) as proc:
      out, _ = proc.communicate()
      return BytesIO(out)

    return False