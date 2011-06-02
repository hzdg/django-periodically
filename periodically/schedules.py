from datetime import timedelta, datetime
from .models import TaskLog


class Schedule(object):
    pass


class PeriodicSchedule(Schedule):
    
    def task_should_run(self, task):
        log_list = TaskLog.objects.filter(task_id=task.task_id).order_by('-start_time')
        if log_list:
            run = datetime.now() - log_list[0].start_time >= self.repeat_interval
        else:
            run = True
        return run
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.repeat_interval)
    

class Daily(PeriodicSchedule):
    repeat_interval = timedelta(days=1)


class Hourly(PeriodicSchedule):
    repeat_interval = timedelta(hours=1)
    
    def __unicode__(self):
        return 'Hourly'


class Weekly(PeriodicSchedule):
    repeat_interval = timedelta(weeks=1)

    def __unicode__(self):
        return 'Weekly'


class Every(PeriodicSchedule):
    def __init__(self, repeat_interval):
        super(Every, self).__init__()
        self.repeat_interval = repeat_interval
    
    def __unicode__(self):
        return 'Every %s' % self.repeat_interval
