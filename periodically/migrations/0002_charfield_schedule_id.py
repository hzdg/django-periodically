# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ExecutionRecord.schedule_id'
        db.alter_column('periodically_executionrecord', 'schedule_id', self.gf('django.db.models.fields.CharField')(max_length=32))


    def backwards(self, orm):
        
        # Changing field 'ExecutionRecord.schedule_id'
        db.alter_column('periodically_executionrecord', 'schedule_id', self.gf('django.db.models.fields.BigIntegerField')())


    models = {
        'periodically.executionrecord': {
            'Meta': {'object_name': 'ExecutionRecord'},
            'completed_successfully': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_fake': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'schedule_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'scheduled_time': ('django.db.models.fields.DateTimeField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['periodically']
