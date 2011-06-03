from django.db import models


class ExecutionRecord(models.Model):
    task_id = models.CharField(max_length=255)
    schedule_id = models.BigIntegerField()
    scheduled_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    completed_successfully = models.BooleanField(default=False)
    is_fake = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s @ %s' % (self.task_id, self.start_time)
