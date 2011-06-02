"""
A collection of functions for quickly registering periodic tasks using the
decorator syntax. Note that, while these functions are used as decorators, they
actually return the original function.
"""

from datetime import timedelta
from . import register
from .schedules import Every, Hourly, Daily, Weekly


def _create_decorator(schedule, backend=None):
    """
    Creates a decorator that registers periodic tasks. Decorators in this
    module delegate to this method in the interest of DRY: it handles all of
    the common arguments.
    """
    def decorator(fn):
        register.simple_task(fn, schedule, backend=backend)
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
    return _create_decorator(Every(interval), *args, **kwargs)


def hourly(*args, **kwargs):
    return _create_decorator(Hourly(), *args, **kwargs)


def daily(*args, **kwargs):
    return _create_decorator(Daily(), *args, **kwargs)


def weekly(*args, **kwargs):
    return _create_decorator(Weekly(), *args, **kwargs)
