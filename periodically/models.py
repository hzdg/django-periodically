from django.db import models


class TaskLog(models.Model):
    task_id = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    success = models.BooleanField()
    
    def __unicode__(self):
        return '%s @ %s' % (self.task_id, self.start_time)
