from django.conf import settings as project_settings
from .backends import CommandBackend
import datetime


_settings = getattr(project_settings, 'PERIODICALLY_SETTINGS', {})
DEFAULT_BACKEND = getattr(_settings, 'DEFAULT_BACKEND', CommandBackend)
DEFAULT_TIMEOUT = getattr(_settings, 'DEFAULT_TIMEOUT', datetime.timedelta(minutes=10))
