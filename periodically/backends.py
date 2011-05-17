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
    def run_scheduled_tasks(self):
        """
        Executes any scheduled periodic tasks.
        """
        for task in self._tasks:
            print 'running task %s' % task.task_id
            self.run_task(task)
    
    def run_task(self, task):
        """
        Runs the provided task. This method is provided as a convenience to
        subclasses so that they do not have to implement all of the extra stuff
        that goes with running a single task--for example, retries, failure
        emails, etc. If you want, your subclass's run_scheduled_tasks method
        can call task.run() directly (avoiding this method), but it is highly
        discouraged.
        """
        # TODO: Error handling/supression, retries, email notification.
        task.run()


class CommandBackend(SchedulerBackend):
    """A backend that only runs tasks when the runtasks command is called."""
    pass
