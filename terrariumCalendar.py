# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from datetime import datetime, timedelta, date, timezone
from operator import attrgetter
from icalendar import Calendar, Event
from icalevents.icalevents import events
from pathlib import Path

class terrariumCalendar(object):

  __ICS_FILE = Path(__file__).parent.joinpath('calendar.ics').resolve()

  def __init__(self):

    if not self.__ICS_FILE.exists():
      self.__ical = Calendar()
      self.__ical.add('prodid', '-//TerrariumPI calendar//terrarium.theyosh.nl//')
      self.__ical.add('version', '2.0')
      self.__ICS_FILE.write_bytes(self.__ical.to_ical())

      self.create_event(
        None,
        'TerrariumPI initial github commit',
        'First commit on Github',
        'https://github.com/theyosh/TerrariumPI/commit/526d39a9ceac57768c6fffe6ffe19afd71782952',
        datetime(2016,1,14,0,0,0,0,timezone.utc)
      )

    self.__ical = Calendar.from_ical(self.__ICS_FILE.read_bytes())

  def __event_schema(self,item):
    event = {'uid'         : str(item.get('uid')),
             'summary'     : str(item.get('summary')),
             'description' : str(item.get('description'))}


    event['dtstart'] = item.get('dtstart').dt.timestamp()
    event['dtend']   = item.get('dtend').dt.timestamp()
    event['all_day'] = event['dtstart'] == event['dtend']

    if item.has_key('rrule'):
      event['freq']     = item.get('rrule').get('freq')[0].lower()
      event['interval'] = item.get('rrule').get('interval')[0]

    return event

  def get_events(self, start = None, end = None):
    if start is None:
      start = datetime.now(timezone.utc) - timedelta(days=1)

    if end is None:
      end = start + timedelta(days=30)

    data = sorted(events(string_content=self.__ical.to_ical(), start=start, end=end), key=attrgetter('start'))

    return_data = []
    for event_data in data:
      item = self.get_event(event_data.uid)
      item['dtstart'] = event_data.start.timestamp()
      item['dtend'] = event_data.end.timestamp()

      return_data.append(item)

    return return_data

  def create_event(self, uid, summary, description, location = None, dtstart = None, dtend = None, freq = None, interval = None):
    #ical = Calendar.from_ical(self.__ical_data)
    create = uid is None or '' == uid

    if dtstart is None:
      dtstart = datetime.now(timezone.utc)

    if dtend is None:
      # One day event
      dtend = dtstart

    event = Event()
    uid = uid if uid is not None else '{}'.format(datetime.now(timezone.utc).timestamp())
    event.add('uid',uid)

    event.add('summary', summary)
    event.add('description', description)

    if location is not None:
      event.add('location', location)

    event.add('dtstart', dtstart)
    event.add('dtend', dtend)
    event.add('dtstamp', datetime.now(timezone.utc))

    if freq and interval and '_' != freq:
      event.add('rrule', {'freq' : freq, 'interval': interval})

    if create:
      self.__ical.add_component(event)

    else:
      for subcomponent in self.__ical.subcomponents:
        if subcomponent.get('uid') == uid:

          if location is None and subcomponent.get('location'):
            del(subcomponent['location'])

          if (freq is None or interval is None or freq == '_') and subcomponent.get('rrule'):
            del(subcomponent['rrule'])

          subcomponent.update(event)

    self.__ICS_FILE.write_bytes(self.__ical.to_ical())
    # Need to reload the ical, so the repeating rules are working....?
    self.__ical = Calendar.from_ical(self.__ICS_FILE.read_bytes())

    return self.get_event(uid)

  def get_event(self,uid):
    # This will always return a copy of the event in the ical. Changes will not be saved
    for subcomponent in self.__ical.subcomponents:
      if subcomponent.get('uid') == uid:
        return self.__event_schema(subcomponent)

    return False

  def delete_event(self, uid):
    counter = 0
    for subcomponent in self.__ical.subcomponents:
      if subcomponent.get('uid') == uid:
        del(self.__ical.subcomponents[counter])
        break
      else:
        counter += 1

    self.__ICS_FILE.write_bytes(self.__ical.to_ical())
    return True

  def download(self):
    return self.__ical.to_ical()

  def get_file(self):
    return self.__ICS_FILE