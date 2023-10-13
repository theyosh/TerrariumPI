# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from io import BytesIO
import subprocess

from . import terrariumWebcam
from terrariumUtils import terrariumUtils


class terrariumHLSLiveWebcam(terrariumWebcam):
    HARDWARE = "hls-live"
    NAME = "Live HLS Stream"
    VALID_SOURCE = r"^https?://.*\.m3u8$"
    INFO_SOURCE = "http(s)://server.com/stream/playlist.m3u8"

    def _load_hardware(self):
        data = terrariumUtils.get_remote_data(self.address)
        if data is not None:
            return self.address

        return None

    def _get_raw_data(self):
        return super()._get_raw_data(self.address)
