"""
A collection of functions for quickly registering periodic tasks using the
decorator syntax. Note that, while these functions are used as decorators, they
actually return the original function, so you can decorate multiple times
without worry.
"""

from . import register
from .schedules import Every, Hourly, Daily, Weekly


def _create_decorator(schedule_class, backend=None, *args, **kwargs):
    """
    Creates a decorator that registers periodic tasks. Decorators in this
    module delegate to this method in the interest of DRY: it handles all of
    the common arguments.
    """
    schedule = schedule_class(*args, **kwargs)
    def decorator(fn):
        register.simple_task(fn, schedule, backend=backend)
        return fn
    return decorator


def every(*args, **kwargs):
    """
    A decorator that allows you to specify an arbitrary repeat interval.
    """
    return _create_decorator(Every, *args, **kwargs)


def hourly(*args, **kwargs):
    return _create_decorator(Hourly, *args, **kwargs)


def daily(*args, **kwargs):
    return _create_decorator(Daily, *args, **kwargs)


def weekly(*args, **kwargs):
    return _create_decorator(Weekly, *args, **kwargs)
