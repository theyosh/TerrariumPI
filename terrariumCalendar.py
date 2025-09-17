# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from datetime import datetime, timedelta, timezone
from time import mktime, sleep
from icalendar import Calendar, Event
from icalevents.icalevents import events
from pathlib import Path


class terrariumCalendar(object):
    __ICS_FILE = Path(__file__).parent.joinpath("data/calendar.ics").resolve()

    def __init__(self):
        if not self.__ICS_FILE.exists():
            self.__ical = Calendar()
            self.__ical.add("prodid", "-//TerrariumPI calendar//terrarium.theyosh.nl//")
            self.__ical.add("version", "2.0")
            self.__ICS_FILE.write_bytes(self.__ical.to_ical())

            self.create_event(
                None,
                "TerrariumPI initial github commit",
                "<p>First commit on Github</p>",
                "https://github.com/theyosh/TerrariumPI/commit/526d39a9ceac57768c6fffe6ffe19afd71782952",
                datetime(2016, 1, 14, 0, 0, 0, 0, timezone.utc),
            )
            # give OS some time to write the file
            sleep(1)

        self.__ical = Calendar.from_ical(self.__ICS_FILE.read_bytes())

        # Clear old wrong events
        for event in self.get_events(
            datetime(2020, 1, 1, 0, 0, 0, 0, timezone.utc), datetime(2030, 1, 1, 0, 0, 0, 0, timezone.utc)
        ):
            if event["summary"] == "TerrariumPI 10 year celebration":
                self.delete_event(event["uid"])

        if self.get_event("10-years-celebration") == False:
            self.create_event(
                "10-years-celebration",
                "TerrariumPI 10 year celebration",
                "<p>TerrariumPI is 10 years old!</p>",
                "https://theyosh.github.io/TerrariumPI/",
                datetime(2024, 8, 1, 0, 0, 0, 0, timezone.utc),
                datetime(2024, 8, 30, 0, 0, 0, 0, timezone.utc),
            )

    def __event_schema(self, item):
        event = {
            "uid": str(item.get("uid")),
            "summary": str(item.get("summary")),
            "description": str(item.get("description")),
            "location": str(item.get("location")),
        }

        event["dtstart"] = int(mktime(item.get("dtstart").dt.timetuple()))
        event["dtend"] = int(mktime(item.get("dtend").dt.timetuple()))
        event["all_day"] = event["dtstart"] == event["dtend"]

        if item.has_key("rrule"):
            event["freq"] = item.get("rrule").get("freq")[0].lower()
            event["interval"] = item.get("rrule").get("interval")[0]

        return event

    def get_events(self, start=None, end=None):
        if start is None:
            start = datetime.now(timezone.utc) - timedelta(days=1)

        if end is None:
            end = start + timedelta(days=30)

        return_data = []

        try:
            for event_data in events(string_content=self.__ical.to_ical(), start=start, end=end):
                item = self.get_event(event_data.uid)
                item["dtstart"] = int(event_data.start.timestamp())
                item["dtend"] = int(event_data.end.timestamp())

                return_data.append(item)
        except Exception as ex:
            logger.error(f"Error loading calendar data: {ex}")

        return sorted(return_data, key=lambda event: event["dtstart"])

    def create_event(
        self,
        uid,
        summary,
        description,
        location=None,
        dtstart=None,
        dtend=None,
        freq=None,
        interval=None,
        repeat_end=None,
    ):
        create = self.get_event(uid) == False

        if dtstart is None:
            dtstart = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        if dtend is None:
            # One day event
            dtend = dtstart + timedelta(days=1)

        event = Event()
        if not uid:
            uid = str(datetime.now(timezone.utc).timestamp())
        event.add("uid", uid)

        event.add("summary", summary)
        event.add("description", description)

        if location is not None:
            event.add("location", location)

        event.add("dtstart", dtstart)
        event.add("dtend", dtend)
        event.add("dtstamp", datetime.now(timezone.utc))

        if freq and interval and "_" != freq:
            rrule = {"freq": freq, "interval": interval}
            if repeat_end is not None:
                rrule["count"] = int(repeat_end)
            event.add("rrule", rrule)

        if create:
            self.__ical.add_component(event)

        else:
            for subcomponent in self.__ical.subcomponents:
                if str(subcomponent.get("uid")) == str(uid):
                    if location is None and subcomponent.get("location"):
                        del subcomponent["location"]

                    if (freq is None or interval is None or freq == "_") and subcomponent.get("rrule"):
                        del subcomponent["rrule"]

                    subcomponent.update(event)

        self.__ICS_FILE.write_bytes(self.__ical.to_ical())
        # Need to reload the ical, so the repeating rules are working....?
        self.__ical = Calendar.from_ical(self.__ICS_FILE.read_bytes())

        return self.get_event(uid)

    def get_event(self, uid):
        # This will always return a copy of the event in the ical. Changes will not be saved
        for subcomponent in self.__ical.subcomponents:
            if str(subcomponent.get("uid")) == str(uid):
                return self.__event_schema(subcomponent)

        return False

    def delete_event(self, uid):
        counter = 0
        for subcomponent in self.__ical.subcomponents:
            if subcomponent.get("uid") == uid:
                del self.__ical.subcomponents[counter]
                break
            else:
                counter += 1

        self.__ICS_FILE.write_bytes(self.__ical.to_ical())
        return True

    def download(self):
        return self.__ical.to_ical()

    def get_file(self):
        return self.__ICS_FILE
