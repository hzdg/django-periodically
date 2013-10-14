import time as _time
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from hashlib import md5


class Schedule(object):
    def __eq__(self, other):
        other_id = getattr(other, 'schedule_id', None)
        return self.schedule_id == other_id

    def __ne__(self, other):
        return not self.__eq__(other)


class BaseSchedule(object):
    """A base class for the built-in schedules. Don't use this yourself.

    """

    @property
    def schedule_id(self):
        class_name = '%s.%s' % (self.__class__.__module__,
                self.__class__.__name__)
        time_args = tuple([getattr(self, name) for name in self._time_attrs])
        return md5(str((class_name, time_args))).hexdigest()

    def time_before(self, time):
        kwargs = dict((k, getattr(self, k)) for k in self._time_attrs)
        t = time.replace(**kwargs)
        if t > time:
            previous_time = t - self.repeat_interval
        else:
            previous_time = t
        return previous_time

    def time_after(self, time):
        return self.time_before(time) + self.repeat_interval


class Hourly(BaseSchedule):
    repeat_interval = timedelta(hours=1)
    _time_attrs = ['minute', 'second', 'microsecond']

    def __init__(self, minute=0, second=0, microsecond=0):
        super(Hourly, self).__init__()
        self.minute = minute
        self.second = second
        self.microsecond = microsecond

    def __str__(self):
        return 'Hourly @ %s' % time(minute=self.minute, second=self.second,
                microsecond=self.microsecond)


class Daily(BaseSchedule):
    repeat_interval = timedelta(days=1)
    _time_attrs = ['hour', 'minute', 'second', 'microsecond']

    def __init__(self, hour=0, minute=0, second=0, microsecond=0):
        super(Daily, self).__init__()
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond

    def __str__(self):
        return 'Daily @ %s' % time(hour=self.hour, minute=self.minute,
                second=self.second, microsecond=self.microsecond)


class Weekly(BaseSchedule):
    repeat_interval = timedelta(days=7)
    _time_attrs = ['day', 'hour', 'minute', 'second', 'microsecond']

    def __init__(self, day=0, hour=0, minute=0, second=0, microsecond=0):
        super(Weekly, self).__init__()
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond

    def __str__(self):
        day_name = _time.strftime('%A', _time.strptime(str(self.day), '%w'))
        return '%s @ %s' % (day_name, time(hour=self.hour, minute=self.minute,
                second=self.second, microsecond=self.microsecond))


def total_seconds(td):
    """Since ``timedelta.total_seconds()`` is new in 2.7"""
    return float(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6


class Every(BaseSchedule):
    _time_attrs = ['repeat_interval']

    def __init__(self, interval=None, days=0, seconds=0, microseconds=0,
            milliseconds=0, minutes=0, hours=0, weeks=0,
                 starting_at=timezone.make_aware(datetime(1970, 1, 1),
                                                 timezone.utc)):
        super(Every, self).__init__()
        if interval is None:
            interval = timedelta(days, seconds, microseconds,
                milliseconds, minutes, hours, weeks)
        self.repeat_interval = interval
        self.starting_at = starting_at

    def time_before(self, time):
        # Uses "perfect time" (no leap years, etc.)
        interval = self.repeat_interval.microseconds / 1000 \
                + total_seconds(self.repeat_interval) * 1000
        time_since_start = time - self.starting_at
        ms_since_start = time_since_start.microseconds / 1000 \
                + total_seconds(time_since_start) * 1000
        delta_in_ms = interval * int(ms_since_start / interval)
        return self.starting_at + timedelta(milliseconds=delta_in_ms)

    def __str__(self):
        return 'Every %s' % self.repeat_interval
