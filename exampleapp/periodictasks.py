from periodically.decorators import *
from periodically import schedule
from datetime import timedelta


@every(minutes=30)
def f():
    print 'f'


def f2():
    print 'f2'


schedule.simple_task(f2, timedelta(weeks=2))
