from periodically.decorators import *

@every(minutes=30)
def f():
    print 'f'
    pass
