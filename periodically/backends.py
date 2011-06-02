from .models import TaskLog
from datetime import datetime
from .signals import task_complete
import logging
import sys
from collections import defaultdict


class TaskInfo(object):
    def __init__(self):
        self.schedules = set()


class BaseBackend(object):
    """
    Keeps a schedule of periodic tasks.
    """
    _tasks = defaultdict(TaskInfo)

    @property
    def logger(self):
        return logging.getLogger('periodically') # TODO: Further namespace logger?
    
    @property
    def scheduled_tasks(self):
        """A list of the scheduled tasks"""
        return [info.task for info in self._tasks.values()]
    
    def schedule_task(self, task, schedule):
        """
        Schedules a periodic task.
        """
        task_id = task.task_id
        self.logger.info('Scheduling task %s to run on schedule %s' % (task_id, schedule))
        self._tasks[task_id].task = task
        self._tasks[task_id].schedules.add(schedule)
        
        # Subscribe to the task_complete signal. We do this when the task
        # is scheduled (instead of when it runs) so that if you kill Django
        # with unfinished tasks still running, they will be able to
        # complete. (For example, whether a task is completed might be
        # determined by polling a web service. When Django restarts, the
        # polling could start again and the task would be completed.)
        if not getattr(task, 'is_blocking', True):
            task_complete.connect(self._create_receiver(task.__class__), sender=task.__class__, dispatch_uid=task_id)
    
    def run_scheduled_tasks(self, tasks=None):
        """
        Runs any scheduled periodic tasks and ends any tasks that have exceeded
        their timeout. The optional <code>tasks</code> argument allows you to
        run only a subset of the registered tasks.
        """
        if tasks is None:
            tasks_to_run = self._tasks.values()
        else:
            tasks_to_run = []
            for task in tasks:
                if task.task_id not in self._tasks:
                    raise Exception('%s is not registered with this backend.' % task)
                else:
                    tasks_to_run.append(self._tasks[task.task_id])
        
        for info in tasks_to_run:
            task = info.task
            schedules = info.schedules
            
            # Cancel the task if it's timed out.
            self.check_timeout(task)
            for schedule in schedules:
                if schedule.task_should_run(task):
                    self.logger.info('Running task %s' % task.task_id)
                    self.run_task(task)

    def check_timeout(self, task):
        try:
            task_log = TaskLog.objects.get(task_id=task.task_id, end_time__isnull=True)
        except TaskLog.DoesNotExist:
            pass
        else:
            from .settings import DEFAULT_TIMEOUT
            timeout = getattr(task, 'timeout', DEFAULT_TIMEOUT)
            running_time = datetime.now() - task_log.start_time
            if running_time > timeout:
                extra = {
                    'level': logging.ERROR,
                    'msg': 'Task timed out after %s.' % running_time,
                }
                self.complete_task(task, extra=extra)
    
    def check_timeouts(self):
        """
        Checks to see whether any scheduled tasks have timed out and handles
        those that have.
        """
        for info in self._tasks.values():
            self.check_timeout(info.task)
    
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
            end_time=None,)

        # Run the task.
        try:
            task.run()
        except Exception, err:
            extra = {
                'level': logging.ERROR,
                'msg': str(err),
                'exc_info': sys.exc_info(),
            }
        else:
            extra = None

        if extra is not None or getattr(task, 'is_blocking', True):
            self.complete_task(task, extra=extra)
    
    def _create_receiver(self, sender):
        def receiver(task, extra=None):
            task_complete.disconnect(receiver, sender, dispatch_uid=task.task_id)
            self.complete_task(task, extra=extra)
        return receiver
    
    def complete_task(self, task, extra=None):
        """
        Marks a task as complete and performs other post-completion tasks. The
        <code>extra</code> argument is a dictionary of values to be passed to
        <code>Logger.log()</code> as keyword args.
        """
        if extra is not None:
            self.logger.log(**extra)
            completed_successfully = extra.get('level', logging.ERROR) != logging.ERROR
        else:
            completed_successfully = True
            
        task_log = TaskLog.objects.get(task_id=task.task_id, end_time=None)
        task_log.end_time = datetime.now()
        task_log.completed_successfully = completed_successfully
        task_log.save()

        # TODO: Retries.


class CommandBackend(BaseBackend):
    """A backend that only runs tasks when the runtasks command is called."""
    id = 'command'
    pass
