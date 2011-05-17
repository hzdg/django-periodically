from django.db import models


class TaskLog(models.Model):
    task_id = models.CharField(max_length=255)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    executing = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s @ %s' % (self.task_id, self.start_time)
