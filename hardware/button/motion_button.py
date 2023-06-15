# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumButton


class terrariumMotionSensor(terrariumButton):
    HARDWARE = "motion"
    NAME = "Motion sensor"

    def _load_hardware(self):
        pass

    @property
    def motion(self):
        return self.pressed

    @property
    def no_motion(self):
        return not self.motion
