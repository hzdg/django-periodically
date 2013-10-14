from django.test import TestCase
from django.utils import timezone
from . import schedules
from datetime import datetime


now = timezone.make_aware(
    datetime(1983, 7, 1, 3, 41),
    timezone.utc)


class ScheduleTest(TestCase):
    def test_hourly(self):
        sched = schedules.Hourly(20, 2, 4)
        self.assertEqual(sched.time_before(now),
                         timezone.make_aware(
                             datetime(1983, 7, 1, 3, 20, 2, 4),
                             timezone.utc))
        self.assertEqual(sched.time_after(now),
                         timezone.make_aware(
                             datetime(1983, 7, 1, 4, 20, 2, 4),
                             timezone.utc))

    def test_every(self):
        sched = schedules.Every(minutes=1)
        self.assertEqual(sched.time_before(now),
                         timezone.make_aware(
                             datetime(1983, 7, 1, 3, 41),
                             timezone.utc))
        self.assertEqual(sched.time_after(now),
                         timezone.make_aware(
                             datetime(1983, 7, 1, 3, 42),
                             timezone.utc))
