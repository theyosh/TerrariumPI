# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from terrariumArea import terrariumArea
from terrariumUtils import terrariumUtils

import copy


class terrariumEnclosure(object):
    def __init__(self, id, name, engine, doors=[], areas=[]):
        if id is None:
            id = terrariumUtils.generate_uuid()

        self.id = id
        self.name = name
        self.engine = engine
        self.doors = doors

        self.areas = {}

        self.load_areas(areas)

    @property
    def weather(self):
        return self.engine.weather

    @property
    def relays(self):
        return self.engine.relays

    @property
    def sensors(self):
        return self.engine.sensors

    @property
    def buttons(self):
        return self.engine.buttons

    def __repr__(self):
        return f"Enclosure {self.name} with {len(self.areas)} areas"

    def __door_status(self):
        # By default, when zero doors are configured, we have to assume the doors are CLOSED
        for door in self.doors:
            if self.engine.buttons[door].is_open:
                return False

        return True

    def __light_status(self):
        if self.main_lights is None or "day" not in self.main_lights.state:
            return True

        return self.main_lights.state["day"]["powered"]

    def load_areas(self, data):
        # First we want to load all the lights areas and then the other areas in any order (not sure if this is still needed -> see def update)
        for area in [area for area in data if area.type == "lights"] + [area for area in data if area.type != "lights"]:
            area_setup = copy.deepcopy(area.setup)
            area_setup["is_day"] = area.state.get("is_day", None)

            self.add(terrariumArea(area.id, self, area.type, area.name, area.mode, area_setup))

    @property
    def main_lights(self):
        for area in self.areas:
            area = self.areas[area]

            if area.setup.get("main_lights", False):
                return self.areas[area.id]

        return None

    def add(self, area):
        if area.id not in self.areas:
            self.areas[area.id] = area

        return area

    def delete(self, area_id):
        if area_id in self.areas:
            del self.areas[area_id]

        return True

    def update(self, read_only=False):
        area_states = {}

        # Construct a list in the order of:
        # - First list is only main lights area, as they can change the power state for heaters and other areas
        # - Then all the areas that do not have dependencies
        # - The the rest of the areas that have dependencies on the previous areas
        for area_id in (
            [
                area_id
                for area_id, area in self.areas.items()
                if area.type == "lights" and area.setup.get("main_lights", False)
            ]
            + [area_id for area_id, area in self.areas.items() if len(area.depends_on) == 0]
            + [area_id for area_id, area in self.areas.items() if len(area.depends_on) > 0]
        ):
            if area_id in area_states:
                # This area is already processed...
                continue

            area_states[area_id] = self.areas[area_id].update(read_only)

        return area_states

    def stop(self):
        for area_id in self.areas:
            self.areas[area_id].stop()

    @property
    def door_closed(self):
        return self.__door_status() == True

    @property
    def door_open(self):
        return self.__door_status() == False

    @property
    def lights_on(self):
        return self.__light_status() == True

    @property
    def lights_off(self):
        return self.__light_status() == False
