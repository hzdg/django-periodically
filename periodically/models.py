from django.db import models


class ExecutionRecordManager(models.Manager):
    def get_most_recent(self, task=None, schedule=None):
        qs = self.get_query_set().order_by('-start_time').all()
        if task:
            qs = qs.filter(task_id=task.task_id)
        if schedule:
            qs = qs.filter(schedule_id=schedule.schedule_id)
        return qs[0] if qs else None


class ExecutionRecord(models.Model):
    task_id = models.CharField(max_length=255)
    schedule_id = models.CharField(max_length=32)
    scheduled_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    completed_successfully = models.BooleanField(default=False)
    is_fake = models.BooleanField(default=False)

    objects = ExecutionRecordManager()

    def __unicode__(self):
        return '%s @ %s' % (self.task_id, self.start_time)
