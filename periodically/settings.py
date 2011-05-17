from django.conf import settings
from .backends import CommandBackend


DEFAULT_BACKEND = getattr(settings, 'PERIODICALLY_DEFAULT_BACKEND', CommandBackend)
