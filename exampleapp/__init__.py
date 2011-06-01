from periodically.decorators import *

@hourly()
def task1():
    print 'exampleapp.task1'