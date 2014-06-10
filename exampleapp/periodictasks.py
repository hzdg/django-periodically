from __future__ import print_function
from periodically.decorators import *
from periodically import register
from datetime import timedelta


@every(minutes=1)
def task2():
    print('RUNNING exampleapp.periodictasks.task2')
    raise Exception('Custom exception!')


def task3():
    print('RUNNING exampleapp.periodictasks.task3')
register.simple_task(task3, Every(timedelta(weeks=2)))


@daily(hour=19, minute=38)
@daily(hour=19, minute=38) # Duplicate. Shouldn't reschedule.
@daily(hour=20, minute=13) # Not a duplicate. Should schedule again.
def task4():
    print('RUNNING exampleapp.periodictasks.task4')
