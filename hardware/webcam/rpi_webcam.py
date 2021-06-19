# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumWebcam
from io import BytesIO

from pathlib import Path
import subprocess
import shlex

class terrariumRPIWebcam(terrariumWebcam):
  HARDWARE     = 'rpicam'
  NAME         = 'Raspberry PI camera'
  VALID_SOURCE = r'^rpicam$'
  INFO_SOURCE  = 'rpicam'

  def _load_hardware(self):
    raspistill = Path('/usr/bin/raspistill')
    if not raspistill.exists():
      return None

    return f'{raspistill} -q 95 -t {self._WARM_UP*1000} -e jpg'

  def _get_raw_data(self):
    logger.debug('Starting rpicam')
    stream = BytesIO()

    cmd = f'{self._device["device"]} -w {self.width} -h {self.height} -awb {self.awb} -o -'
    cmd = shlex.split(cmd)

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
      out, err = proc.communicate()
      if err != b'':
        return False

      return BytesIO(out)

    return False
