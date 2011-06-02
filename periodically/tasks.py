class PeriodicTask(object):
    backend = 'default'
    is_blocking = True
    
    @property
    def task_id(self):
        return '%s.%s' % (self.__module__, self.__name__)

    def run(self):
        raise RuntimeError('This method must be overridden by your class.')
