# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from icalendar import Calendar, Event
from icalevents.icalevents import events

import os.path


from datetime import datetime, timedelta, date
#from dateutil.tz import UTC

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


  def get_events(self,start,end):
    return events(file=terrariumCalendar.ICS_FILE,start=start,end=end)