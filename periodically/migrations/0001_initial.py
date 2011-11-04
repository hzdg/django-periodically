# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExecutionRecord'
        db.create_table('periodically_executionrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('schedule_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('scheduled_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completed_successfully', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_fake', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('periodically', ['ExecutionRecord'])


    def backwards(self, orm):
        
        # Deleting model 'ExecutionRecord'
        db.delete_table('periodically_executionrecord')


    models = {
        'periodically.executionrecord': {
            'Meta': {'object_name': 'ExecutionRecord'},
            'completed_successfully': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_fake': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'schedule_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'scheduled_time': ('django.db.models.fields.DateTimeField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['periodically']
