# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from gevent import sleep
from pathlib import Path
from io import BytesIO
import subprocess
import threading
import shlex

from . import terrariumWebcam, terrariummWebcamLoadingException
from terrariumUtils import terrariumUtils

class terrariumRPILiveWebcam(terrariumWebcam):
  HARDWARE     = 'rpicam-live'
  NAME         = 'Live Raspberry PI camera'
  VALID_SOURCE = '^rpicam_live$'
  INFO_SOURCE  = 'rpicam_live'

  __RASPIVID = '/usr/bin/raspivid'
  __FFMPEG   = '/usr/bin/ffmpeg'

  def __run(self):
    cmd = Path(__file__).parent / 'rpilive_webcam.sh'

    width  = self.width  if self.rotation not in ['90','270'] else self.height
    height = self.height if self.rotation not in ['90','270'] else self.width

    cmd = f'{cmd} "{self.name}" {width} {height} {self.rotation} {self.awb} {Path(self._STORE_LOCATION).joinpath(self.id)}'
    cmd = shlex.split(cmd)

    self.__process_id = subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

  def stop(self):
    try:
      self.__process_id.terminate()
    except Exception as ex:
      pass
    super().stop()

  def _load_hardware(self):
    if not Path(self.__RASPIVID).exists():
      raise terrariummWebcamLoadingException(f'Please install raspivid.')

    if not Path(self.__FFMPEG).exists():
      raise terrariummWebcamLoadingException(f'Please install ffmpeg.')

    try:
      self.__process_id.terminate()
    except Exception as ex:
      pass

    threading.Thread(target=self.__run).start()
    # We need some time to wait so that the live stream has produced the first chunks
    sleep(5)

    return True

  def _get_raw_data(self):
    url = f'{Path(self._STORE_LOCATION).joinpath(self.id)}/stream.m3u8'
    cmd = f'{self.__FFMPEG} -hide_banner -loglevel panic -i {url} -vframes 1 -f image2 -'
    cmd = shlex.split(cmd)

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
      out, err = proc.communicate()
      return BytesIO(out)

    return False
