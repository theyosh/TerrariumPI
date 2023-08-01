# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumWebcamLive


class terrariumUSBLiveWebcam(terrariumWebcamLive):
    HARDWARE = "usb-live"
    NAME = "Live USB camera"
    VALID_SOURCE = r"^/dev/video\d+"
    INFO_SOURCE = "/dev/video[NR]"

    _HELPER_SCRIPT = "usblive_webcam.sh"
