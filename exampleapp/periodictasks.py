from periodically.decorators import *
from periodically import schedule
from datetime import timedelta


@every(minutes=1)
def task2():
    print 'exampleapp.periodictasks.task2'
    raise Exception('Custom exception!')


def task3():
    print 'exampleapp.periodictasks.task3'


schedule.simple_task(task3, timedelta(weeks=2))
