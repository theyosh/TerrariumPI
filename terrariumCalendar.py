# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from hashlib import md5


from datetime import datetime, timedelta, date
from operator import attrgetter
from icalendar import Calendar, Event
from icalevents.icalevents import events

import os.path

class terrariumCalendar(object):

  ICS_FILE = 'calendar.ics'

  def __init__(self):
    if not os.path.isfile(terrariumCalendar.ICS_FILE):
      ical = Calendar()
      ical.add('prodid', '-//TerrariumPI calendar//terrarium.theyosh.nl//')
      ical.add('version', '2.0')

      event = Event()
      event.add('uid','1')
      event.add('summary', 'TerrariumPI initial github commit')
      event.add('location', 'https://github.com/theyosh/TerrariumPI/commit/526d39a9ceac57768c6fffe6ffe19afd71782952')
      event.add('dtstart', date(2016,1,14))
      event.add('dtend', date(2016,1,14))
      event.add('dtstamp', datetime.now())

      ical.add_component(event)

      with open(terrariumCalendar.ICS_FILE, 'wb') as fp:
        fp.write(ical.to_ical())

    self.__ical_data = None
    with open(terrariumCalendar.ICS_FILE, 'rb') as fp:
      self.__ical_data = fp.read()

  def get_events(self,start,end):
    if start is None:
      start = datetime.now() - timedelta(days=1)

    return sorted(events(string_content=self.__ical_data,start=start,end=end), key=attrgetter('start'))

  def create_event(self,uid,title,message,location = None,start = None,stop = None):
    ical = Calendar.from_ical(self.__ical_data)
    create = uid is None or '' == uid

    if start is None:
      start = datetime.now()

    if stop is None:
      stop = start


    if create:
      uid = str(datetime.now()).replace(' ','@') + '/' + str(start) + '/' + str(uid)
      event = Event()
      event.add('uid',uid)

      event.add('summary', title)
      event.add('description', message)

      if location is not None:
        event.add('location', location)

      event.add('dtstart', start)
      event.add('dtend', stop)
      event.add('dtstamp', datetime.now())

      ical.add_component(event)

    else:
      for subcomponent in ical.subcomponents:
        if subcomponent.get('uid') == uid:
          update_data = {
            'summary': subcomponent._encode('summary',title),
            'description' : subcomponent._encode('description',message),
            'dtstart' : subcomponent._encode('dtstart',start),
            'dtend': subcomponent._encode('dtend',stop)
          }

          if location is not None:
            update_data['location']  = subcomponent._encode('location',location)

          subcomponent.update(update_data)

    with open(terrariumCalendar.ICS_FILE, 'wb') as fp:
      fp.write(ical.to_ical())

    self.__ical_data = ical.to_ical()

  def get_ical(self):
    return self.__ical_data
