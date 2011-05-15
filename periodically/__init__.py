import inspect


# Based on django's admin app's autodiscover.
def autodiscover():
    """
    Auto-discover INSTALLED_APPS periodictasks.py modules and fail silently
    when not present.
    """

    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's periodictasks module.
        try:
            import_module('%s.periodictasks' % app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have a periodictasks module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'periodictasks'):
                raise


class PeriodicTask(object):
    def run():
        raise RuntimeError('This method must be overridden by your class.')


class TaskRegistry(object):
    
    _tasks = {}
    
    def simple_task(self, fn, repeat_interval, task_id_suffix=''):
        """
        Registers a callable as a periodic task.
        """
        _task_id = '%s.%s%s' % (fn.__module__, fn.__name__, task_id_suffix)
        _repeat_interval = repeat_interval

        # Create a PeriodicTask subclass that wraps the function.
        class DecoratedTask(PeriodicTask):
            task_id = _task_id
            repeat_interval = _repeat_interval
            def run(*args, **kwargs):
                fn(*args, **kwargs)

        self.task(DecoratedTask)
        return DecoratedTask
    
    def task(self, task):
        """
        Registers a periodic task.
        """
        if inspect.isclass(task):
            task = task()
        print 'registering %s with id %s' % (task, task.task_id)
        self._tasks[task.task_id] = task
        

register = TaskRegistry()
autodiscover()
