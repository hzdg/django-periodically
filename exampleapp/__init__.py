from __future__ import print_function
from periodically.decorators import *

@every(minutes=1)
@hourly()
@hourly() # This repetition should have no effect.
def task1():
    print('RUNNING exampleapp.task1')