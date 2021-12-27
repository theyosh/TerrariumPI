# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from pony import orm
from terrariumArea import terrariumArea
from terrariumDatabase import Button, Relay, Sensor
from terrariumUtils import terrariumUtils

import copy
class terrariumEnclosure(object):

  def __init__(self, id, name, engine, doors = [], areas = []):
    self.__main_lights = None

    if id is None:
      id = terrariumUtils.generate_uuid()

    self.id          = id
    self.name        = name
    self.engine      = engine
    self.doors       = doors

    self.areas = {}

    self.load_areas(areas)

  @property
  def weather(self):
    return self.engine.weather

  @property
  def relays(self):
    return self.engine.relays

  def __repr__(self):
    return f'Enclosure {self.name} with {len(self.areas)} areas'

  def __door_status(self):
    # By default, when zero doors are configured, we have to assume the doors are CLOSED
    for door in self.doors:
      if self.engine.buttons[door].is_open:
        return False

    return True

  def __light_status(self):
    main_lights = self.main_lights
    if main_lights is None:
      return True

    return main_lights.state['day']['powered']

  def load_areas(self, data):
    for area in data:
      if area.type != 'lights':
        continue

      area_setup = copy.deepcopy(area.setup)
      area_setup['is_day'] = area.state.get('is_day',None)

      new_area = self.add(terrariumArea(
        area.id,
        self,
        area.type,
        area.name,
        area.mode,
        area_setup
      ))

    for area in data:
      if area.type == 'lights':
        continue

      area_setup = copy.deepcopy(area.setup)
      area_setup['is_day'] = area.state.get('is_day',None)

      new_area = self.add(terrariumArea(
        area.id,
        self,
        area.type,
        area.name,
        area.mode,
        area_setup
      ))

  @property
  def main_lights(self):
    for area in self.areas:
      area = self.areas[area]
      if 'disabled' == area.mode:
        continue

      if area.setup.get('main_lights', False):
        return self.areas[area.id]

    return None

  def add(self, area):
    if area.id not in self.areas:
      self.areas[area.id] = area

    return area

  def update(self, read_only = False):
    area_states = {}

    # First we update the main lights area, as they can change the power state for heaters and other areas
    for area_id in self.areas:
      if 'disabled' == self.areas[area_id].mode or 'lights' != self.areas[area_id].type:
        continue

      if self.areas[area_id].setup.get('main_lights', False):
        area_states[area_id] = self.areas[area_id].update(read_only)

    # Update the remaining areas, skipping all that have dependencies...
    for area_id in self.areas:
      if 'disabled' == self.areas[area_id].mode or area_id in area_states or len(self.areas[area_id].depends_on) > 0:
        continue

      area_states[area_id] = self.areas[area_id].update(read_only)

    # Update the remaining areas that have depencies on other areas
    for area_id in self.areas:
      if 'disabled' == self.areas[area_id].mode or area_id in area_states:
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