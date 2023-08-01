# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumWebcamLive


class terrariumRTSPLiveWebcam(terrariumWebcamLive):
    HARDWARE = "rtsp-live"
    NAME = "Live RTSP camera"
    VALID_SOURCE = r"^rtsp?://.*(?<!\.m3u8)$"
    INFO_SOURCE = "rtsp://server.com/stream"

    _HELPER_SCRIPT = "rtsplive_webcam.sh"
