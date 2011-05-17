"""
A collection of functions for quickly registering periodic tasks using the
decorator syntax. Note that, while these functions are used as decorators, they
actually return the original function.
"""

from datetime import timedelta
from . import register


def _create_decorator(repeat_interval, task_id_suffix=None, backend=None):
    """
    Creates a decorator that registers a periodic tasks. Decorators in this
    module delegate to this method in the interest of DRY: it handles all of
    the common arguments.
    """
    
    if task_id_suffix is None:
        task_id_suffix = '/every %s' % repeat_interval
    
    def decorator(fn):
        register.simple_task(fn, repeat_interval,
            task_id_suffix=task_id_suffix, backend=backend)
        return fn
    return decorator


def every(interval=None, days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0, *args, **kwargs):
    """
    A decorator that allows you to specify an arbitrary repeat interval.
    """
    if interval is None:
        interval = timedelta(days, seconds, microseconds, milliseconds,
            minutes, hours, weeks)
    return _create_decorator(interval, *args, **kwargs)


def hourly(*args, **kwargs):
    return _create_decorator(timedelta(hours=1), task_id_suffix='/hourly',
        *args, **kwargs)


def daily(*args, **kwargs):
    return _create_decorator(timedelta(days=1), task_id_suffix='/daily',
        *args, **kwargs)


def weekly(*args, **kwargs):
    return _create_decorator(timedelta(weeks=1), task_id_suffix='/weekly',
        *args, **kwargs)
