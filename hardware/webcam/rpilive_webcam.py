# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from pathlib import Path

from . import terrariumWebcamLive, terrariumWebcamLoadingException


class terrariumRPILiveWebcam(terrariumWebcamLive):
    HARDWARE = "rpicam-live"
    NAME = "Live Raspberry PI camera"
    VALID_SOURCE = r"^rpicam_live$"
    INFO_SOURCE = "rpicam_live"

    _HELPER_SCRIPT = "rpilive_webcam.sh"

    def _load_hardware(self):
        if not Path("/usr/bin/raspivid").exists():
            if not Path("/usr/bin/rpicam-vid").exists():
                raise terrariumWebcamLoadingException("Raspicam is not enabled")

            # Fix changed AWB values
            valid_awb = ["auto", "incandescent", "tungsten", "fluorescent", "indoor", "daylight", "cloudy"]

            if self.awb == "sunlight":
                self.awb = "daylight"

            self.awb = "auto" if self.awb not in valid_awb else self.awb

        return super()._load_hardware()
