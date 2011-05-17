"""
A collection of functions for quickly registering periodic tasks using the
decorator syntax. Note that, while these functions are used as decorators, they
actually return the original function.
"""

from datetime import timedelta
from . import register


def hourly():
    def decorator(fn):
        register.simple_task(fn, timedelta(hours=1), task_id_suffix=':hourly')
        return fn
    return decorator


def daily():
    def decorator(fn):
        register.simple_task(fn, timedelta(days=1), task_id_suffix=':daily')
        return fn
    return decorator


def weekly():
    def decorator(fn):
        register.simple_task(fn, timedelta(weeks=1), task_id_suffix=':weekly')
        return fn
    return decorator


def every(*args, **kwargs):
    repeat_interval = timedelta(*args, **kwargs)
    def decorator(fn):
        register.simple_task(fn, repeat_interval, task_id_suffix=':every %s' % repeat_interval)
        return fn
    return decorator
