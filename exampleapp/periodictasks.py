from periodically.decorators import *
from periodically import register
from datetime import timedelta


@every(minutes=1)
def task2():
    print 'exampleapp.periodictasks.task2'
    raise Exception('Custom exception!')


def task3():
    print 'exampleapp.periodictasks.task3'


register.simple_task(task3, Every(timedelta(weeks=2)))
