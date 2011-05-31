from .models import TaskLog
from datetime import datetime
from .signals import task_complete


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
            
            # Subscribe to the task_complete signal. We do this when the task
            # is scheduled (instead of when it runs) so that if you kill Django
            # with unfinished tasks still running, they will be able to
            # complete. (For example, whether a task is completed might be
            # determined by polling a web service. When Django restarts, the
            # polling could start again and the task would be completed.)
            if not getattr(task, 'is_blocking', True):
                task_complete.connect(self._create_receiver(), sender=task.__class__, dispatch_uid=task.task_id)
    
    def run_scheduled_tasks(self):
        """
        Runs any scheduled periodic tasks and ends any tasks that have exceeded
        their timeout.
        """
        for task in self._tasks:
            try:
                log = TaskLog.objects.get(task_id=task.task_id, end_time__isnull=True)
            except TaskLog.DoesNotExist:
                task_is_running = False
                log = None
            else:
                task_is_running = True
            
            # If the task isn't already running, run it now.
            if not task_is_running:
                print 'running task %s' % task.task_id
                self.run_task(task)
            elif log and datetime.now() > log.start_time + self._get_timeout(task):
                self.complete_task(task.task_id, Exception('Task timed out after <TIME> time.')) # FIXME: Show the time.
    
    def _get_timeout(self, task):
        return 1209
    
    def task_is_running(self, task):
        """
        Determines whether the provided task is currently running.
        """
        return bool()
    
    def run_task(self, task):
        """
        Runs the provided task. This method is provided as a convenience to
        subclasses so that they do not have to implement all of the extra stuff
        that goes with running a single task--for example, retries, failure
        emails, etc. If you want, your subclass's run_scheduled_tasks method
        can call task.run() directly (avoiding this method), but it is highly
        discouraged.
        """
        # Create the log for this execution.
        log = TaskLog.objects.create(
            task_id=task.task_id,
            start_time=datetime.now(),
            end_time=None,
            is_success=False,)

        # Run the task.
        try:
            task.run()
        except Exception, err:
            error = err
        else:
            error = None

        if error is not None or getattr(task, 'is_blocking', True):
            self.complete_task(task.task_id, error=error)
    
    def _create_receiver(self):
        def receiver(task_id, error=None):
            task_complete.disconnect(receiver, task.__class__, dispatch_uid=task_id)
            self.complete_task(task_id, error)
        return receiver
    
    def complete_task(self, task_id, error=None):
        """
        Marks a task as complete and performs other post-completion tasks.
        """
        log = TaskLog.objects.get(task_id=task_id, end_time=None)
        log.end_time = datetime.now()
        log.is_success = error is not None
        log.error_message = str(error)
        log.save()
        
        # TODO: Retries, email notification.


class CommandBackend(SchedulerBackend):
    """A backend that only runs tasks when the runtasks command is called."""
    id = 'command'
    pass
