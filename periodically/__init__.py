import inspect
from .tasks import PeriodicTask
from .utils import get_scheduler_backend_class


# Based on django's admin app's autodiscover.
def autodiscover():
    """
    Auto-discover INSTALLED_APPS periodictasks.py modules and fail silently
    when not present.
    """

    from django.conf import settings as project_settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in project_settings.INSTALLED_APPS:
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


class TaskRegistry(object):

    _backend_singletons = {} # Maps backend classes to instances.
    _backends = set()

    @property
    def backends(self):
        return self._backends

    def simple_task(self, fn, schedule, backend=None):
        """
        Registers a callable as a periodic task.
        """
        _task_id = '%s.%s' % (fn.__module__, fn.__name__)

        # Create a PeriodicTask subclass that wraps the function.
        class DecoratedTask(PeriodicTask):
            task_id = _task_id

            def run(self, *args, **kwargs):
                fn(*args, **kwargs)

        task_instance = DecoratedTask()
        self.task(task_instance, schedule, backend)
        return task_instance

    def task(self, task, schedule, backend=None):
        """
        Registers a periodic task.
        """
        if inspect.isclass(task):
            task = task()
            
        backend_class = get_scheduler_backend_class(backend)
        try:
            backend = self._backend_singletons[backend_class]
        except KeyError:
            backend = self._backend_singletons[backend_class] = backend_class()
        self._backends.add(backend)
        backend.schedule_task(task, schedule)


register = TaskRegistry()
autodiscover()
