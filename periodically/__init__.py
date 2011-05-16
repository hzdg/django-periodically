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
    
    @property
    def task_id(self):
        return '%s.%s' % (self.__module__, self.__name__)

    def run(self):
        raise RuntimeError('This method must be overridden by your class.')


class SchedulerBackendAttributeError(Exception):
    """Scheduler backend attribute is missing."""
    pass

class SchedulerBackendImproperlyConfigured(Exception):
    """Scheduler Backend is somehow misconfigured."""
    pass
    
class TaskRegistry(object):

    _tasks = {}
    _backends = {}
    
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
            @staticmethod
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
        
        for backend in self._get_backends(task):
            backend.schedule(task)

        print 'registering %s with id %s' % (task, task.task_id)
        self._tasks[task.task_id] = task

    def _load_backend(self, path):
        from django.utils.importlib import import_module

        i = path.rfind('.')
        module, attr = path[:i], path[i + 1:]
        try:
            mod = import_module(module)
        except ImportError, e:
            raise SchedulerBackendImproperlyConfigured('Error importing scheduler backend %s: "%s"' % (path, e))
        except ValueError, e:
            raise SchedulerBackendImproperlyConfigured('Error importing scheduler backends: %s' % e)
        try:
            cls = getattr(mod, attr)
        except AttributeError, e:
            raise SchedulerBackendImproperlyConfigured('Module "%s" does not define a "%s" scheduler backend' % (module, attr))
        if not hasattr(cls, 'schedule'):
            raise SchedulerBackendAttributeError('Backend %s has no schedule attribute.' % path)
        return cls()

    def _get_backends(self, task):
        from django.conf import settings
        
        backends = []
        backend_paths = getattr(task, 'scheduler_backends', [])
        if not backend_paths:
            # TODO: Name the global setting.
            backend_paths = getattr(settings, 'SCHEDULER_BACKENDS', 
                ('periodically.backends.CommandBackend',))

        for backend_path in backend_paths:
            if backend_path not in self._backends:
                self._backends[backend_path] = self._load_backend(backend_path)
            backends.append(self._backends[backend_path])

        if not backends:
            raise SchedulerBackendImproperlyConfigured('No scheduler backends are defined.')

        return backends

register = TaskRegistry()
autodiscover()

def get_command_backend():
    return register._backends.get('periodically.backends.CommandBackend', None)