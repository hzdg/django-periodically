from django.conf import settings as project_settings
import datetime


_settings = getattr(project_settings, 'PERIODICALLY_SETTINGS', {})
DEFAULT_TIMEOUT = _settings.get('DEFAULT_TIMEOUT', datetime.timedelta(minutes=10))
SCHEDULERS = _settings.get('SCHEDULERS', {})

# Add the default scheduler it hasn't been explicitly overridden. This way, you
# won't have to redefine the default when you really just want to add a new
# scheduler.
if not SCHEDULERS.has_key('default'):
    SCHEDULERS['default'] = {'backend': 'periodically.backends.DefaultBackend'}
