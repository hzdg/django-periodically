from datetime import timedelta, datetime
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
    
    def task_should_run(self, task):
        previous_record = self.get_previous_record(task)
        return not previous_record or datetime.now() - previous_record.start_time >= self.repeat_interval
    
    def __hash__(self):
        return hash((PeriodicSchedule, self.repeat_interval))
    

class Daily(Schedule):
    
    def __init__(self, hour=0, minute=0, second=0, microsecond=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
    
    def __hash__(self):
        return hash((Daily, self.hour, self.minute, self.second, self.microsecond))
    
    def task_should_run(self, task):
        previous_record = self.get_previous_record(task)
        if previous_record:
            last_run_date = datetime.date(previous_record.start_time)
            current_time = datetime.now()
            current_date = datetime.date(current_time)
            if current_date > last_run_date:
                run_after_time = datetime(current_date.year,
                    current_date.month, current_date.day, self.hour,
                    self.minute, self.second, self.microsecond)
                if current_time > run_after_time:
                    return True
            return False
        else:
            return True


class Hourly(PeriodicSchedule):
    repeat_interval = timedelta(hours=1)
    
    def __unicode__(self):
        return 'Hourly'


class Weekly(PeriodicSchedule):
    repeat_interval = timedelta(weeks=1)

    def __unicode__(self):
        return 'Weekly'


class Every(PeriodicSchedule):
    def __init__(self, interval=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        super(Every, self).__init__()
        if interval is None:
            interval = timedelta(days, seconds, microseconds, milliseconds,
                minutes, hours, weeks)
        self.repeat_interval = interval
    
    def __unicode__(self):
        return 'Every %s' % self.repeat_interval
