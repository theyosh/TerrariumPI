# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from pony import orm
from terrariumArea import terrariumArea
from terrariumDatabase import Button, Relay, Sensor

import copy


class terrariumEnclosure(object):

  def __init__(self, id, name, engine, doors = [], areas = []):
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
    # By default, when zero doors are configured, we have to asume the doors are CLOSED
    for door in self.doors:
      if self.engine.buttons[door].is_open:
        return False

    return True

  def __light_status(self):
    for area_id in self.areas:
      if 'lights' == self.areas[area_id].type and self.areas[area_id].setup.get('main_lights', False):
        return self.areas[area_id].state['powered']

    return False

  def load_areas(self, data):
    for area in data:
      area_setup = copy.deepcopy(area.setup)

      self.add(terrariumArea(
        str(area.id),
        self,
        area.type,
        area.name,
        area.mode,
        area_setup
      ))

  def add(self, area):
    if area.id not in self.areas:
      self.areas[area.id] = area

    return area

  def update(self):
    area_states = {}

    # First we update the main lights area, as they can change the power state for heaters and other areas
    light_areas = []
    for area_id in self.areas:
      if 'lights' == self.areas[area_id].type and self.areas[area_id].setup.get('main_lights', False):
        area_states[area_id] = self.areas[area_id].update()
        light_areas.append(area_id)

    # Update the remaining areas
    for area_id in self.areas:
      if area_id in light_areas:
        continue

      area_states[area_id] = self.areas[area_id].update()

    return area_states

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