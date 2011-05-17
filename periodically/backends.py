from .models import TaskLog
from datetime import datetime

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
    
    def run_scheduled_tasks(self):
        """
        Runs any scheduled periodic tasks.
        """
        for task in self._tasks:
            log, run_now = TaskLog.objects.get_or_create(task_id=task.task_id)
            
            # FIXME: Use start_time or finish_time? Does finish_time get set even if success if false?
            if not run_now:
                run_now = log.start_time is None or \
                    (datetime.now() - log.start_time > task.repeat_interval)

            if run_now:
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
        log = TaskLog.objects.get_or_create(task_id=task.task_id)[0]

        # TODO: Handle situation when task is currently executing.
        if not log.executing:
            log.start_time = datetime.now()
            log.end_time = None
            log.executing = True
            log.success = False
            log.save()

            success = False
            try:
                task.run()
                sucesss = True
            except:
                # TODO: Error handling/supression, retries, email notification.
                pass

            log.end_time = datetime.now()
            log.success = success
            log.executing = False
            log.save()
    


class CommandBackend(SchedulerBackend):
    """A backend that only runs tasks when the runtasks command is called."""
    id = 'command'
    pass
