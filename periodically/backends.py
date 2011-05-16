

class SchedulerBackend(object):
    """
    Keeps a schedule of periodic tasks.
    """
    _tasks = []
    
    def schedule(self, task):
        """
        Schedules a periodic task.
        """
        if task not in self._tasks:
            print 'scheduled task %s to run every %s' % (task.task_id, task.repeat_interval)
            self._tasks.append(task)
    
    # TODO: better name for this?
    def execute(self):
        """
        Executes any scheduled periodic tasks.
        """
        for task in self._tasks:
            print 'running task %s' % task.task_id
            task.run()
        pass
    
    
class CommandBackend(SchedulerBackend):
    pass
