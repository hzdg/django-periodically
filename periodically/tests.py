from django.test import TestCase
from . import schedules
from datetime import datetime


now = datetime(1983, 7, 1, 3, 41)


class ScheduleTest(TestCase):
    def test_hourly(self):
        sched = schedules.Hourly(20, 2, 4)
        self.assertEqual(sched.time_before(now), datetime(1983, 7, 1, 3, 20, 2, 4))
        self.assertEqual(sched.time_after(now), datetime(1983, 7, 1, 4, 20, 2, 4))

    def test_every(self):
        sched = schedules.Every(minutes=1)
        self.assertEqual(sched.time_before(now), datetime(1983, 7, 1, 3, 41))
        self.assertEqual(sched.time_after(now), datetime(1983, 7, 1, 3, 42))
