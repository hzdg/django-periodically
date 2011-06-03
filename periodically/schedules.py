import datetime
from .models import ExecutionRecord


class Schedule(object):
    def get_previous_record(self, task):
        record_list = ExecutionRecord.objects.filter(task_id=task.task_id, schedule_id=self.__hash__()).order_by('-start_time')
        if record_list:
            return record_list[0]
        else:
            return None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


class PeriodicSchedule(Schedule):
        
    def get_next_run_time(self, task):
        previous_record = self.get_previous_record(task)
        if previous_record:
            next_run_time = previous_record.scheduled_time + self.repeat_interval
        else:
            next_run_time = datetime.datetime.now()
        return next_run_time
    
    def __hash__(self):
        class_name = '%s.%s' % (self.__module__, self.__class__)
        return hash((class_name, self.repeat_interval))
    

class Daily(Schedule):
    
    def __init__(self, hour=0, minute=0, second=0, microsecond=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
    
    def __hash__(self):
        class_name = '%s.%s' % (self.__module__, self.__class__)
        return hash((class_name, self.hour, self.minute, self.second, self.microsecond))
    
    def get_next_run_time(self, task):
        previous_record = self.get_previous_record(task)
        if previous_record:
            previous_run_date = datetime.datetime.date(previous_record.scheduled_time)
            next_run_date = previous_run_date + datetime.timedelta(days=1)
        else:
            next_run_date = datetime.date.today()

        return datetime.datetime.combine(next_run_date, datetime.time(self.hour,
            self.minute, self.second, self.microsecond))


class Hourly(PeriodicSchedule):
    repeat_interval = datetime.timedelta(hours=1)
    
    def __unicode__(self):
        return 'Hourly'


class Weekly(PeriodicSchedule):
    repeat_interval = datetime.timedelta(weeks=1)

    def __unicode__(self):
        return 'Weekly'


class Every(PeriodicSchedule):
    def __init__(self, interval=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        super(Every, self).__init__()
        if interval is None:
            interval = datetime.timedelta(days, seconds, microseconds, milliseconds,
                minutes, hours, weeks)
        self.repeat_interval = interval
    
    def __unicode__(self):
        return 'Every %s' % self.repeat_interval
