class PeriodicTask(object):
    backend = None
    retries = 0
    
    @property
    def task_id(self):
        return '%s.%s' % (self.__module__, self.__name__)

    def run(self):
        raise RuntimeError('This method must be overridden by your class.')
