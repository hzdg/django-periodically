from django.test import TestCase
from django.utils import timezone
from . import schedules
from datetime import datetime
from .decorators import hourly, every
from .utils import get_scheduler_backends_in_groups
from . import register as task_scheduler


now = timezone.make_aware(
    datetime(1983, 7, 1, 3, 41),
    timezone.utc)


class ScheduleTest(TestCase):

    def setUp(self):

        @hourly()
        def hourly_test_task():
            print "Running test for 'hourly' decorator"


        @every(minutes=1)
        def every_test_task():
            print "Running test for 'every' decorator"



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

    def test_run_tasks(self):

        backends = task_scheduler.backends

        for backend in backends:

            backend.run_scheduled_tasks(backend.tasks, fake=True)
