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
    # New RPI Camera app
    raspistill = Path('/usr/bin/libcamera-still')
    if not raspistill.exists():
      # Old RPI Camera app
      raspistill = Path('/usr/bin/raspistill')
      if not raspistill.exists():
        return None

    return f'{raspistill} --quality 95 --timeout {self._WARM_UP*1000} --encoding jpg'

  def _get_raw_data(self):
    if self._device["device"] is None:
      return False

    logger.debug('Starting rpicam')

    cmd = f'{self._device["device"]} --width {self.width} --height {self.height} --awb {self.awb} --output -'
    cmd = shlex.split(cmd)

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
      out, err = proc.communicate()
      if err != b'':
        return False

      return BytesIO(out)

    return False
