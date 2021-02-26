# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumWebcam
from terrariumUtils import terrariumUtils

# export READTHEDOCS=True; pip install picamera
from picamera import PiCamera, PiCameraError
from io import BytesIO

from gevent import sleep

# Bug / Upstream
# https://github.com/raspberrypi/firmware/issues/1167#issuecomment-511798033
# https://github.com/waveform80/picamera/pull/576
from picamera import mmal
import ctypes as ct


class PiCameraUpstream(PiCamera):
  AWB_MODES = {
    'off':           mmal.MMAL_PARAM_AWBMODE_OFF,
    'auto':          mmal.MMAL_PARAM_AWBMODE_AUTO,
    'sunlight':      mmal.MMAL_PARAM_AWBMODE_SUNLIGHT,
    'cloudy':        mmal.MMAL_PARAM_AWBMODE_CLOUDY,
    'shade':         mmal.MMAL_PARAM_AWBMODE_SHADE,
    'tungsten':      mmal.MMAL_PARAM_AWBMODE_TUNGSTEN,
    'fluorescent':   mmal.MMAL_PARAM_AWBMODE_FLUORESCENT,
    'incandescent':  mmal.MMAL_PARAM_AWBMODE_INCANDESCENT,
    'flash':         mmal.MMAL_PARAM_AWBMODE_FLASH,
    'horizon':       mmal.MMAL_PARAM_AWBMODE_HORIZON,
    'greyworld':     ct.c_uint32(10)
  }

class terrariumRPIWebcam(terrariumWebcam):
  HARDWARE     = 'rpicam'
  NAME         = 'Raspberry PI camera'
  VALID_SOURCE = r'^rpicam$'
  INFO_SOURCE  = 'rpicam'

  def _load_hardware(self):
    with PiCameraUpstream(resolution=(self.width, self.height)) as camera:
      camera.start_preview()
      # It does not matter what we return here. So True is the most logic for a successfull hardware loading
      return True

    return None

  def _get_raw_data(self):
    logger.debug('Starting rpicam')
    stream = BytesIO()
    # We need to create a new PiCamera as it is closed after taking image.
    with PiCameraUpstream(resolution=(self.width, self.height)) as camera:
      logger.debug('Set whitebalanc to: {}'.format(self.awb))
      camera.awb_mode = self.awb
      logger.debug('Open rpicam')
      camera.start_preview()
      logger.debug('Wait {} seconds for preview'.format(self._WARM_UP))
      sleep(self._WARM_UP)
      logger.debug('Save rpicam to jpeg stream')
      camera.capture(stream, format='jpeg')
      logger.debug('Done creating RPICAM image')
      return stream

    return False
