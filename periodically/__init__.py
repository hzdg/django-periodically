import inspect
from . import settings
from .tasks import PeriodicTask


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


class TaskScheduler(object):

    _backend_singletons = {} # Maps backend classes to instances.
    _backends = set()

    class BackendDoesNotExist(Exception):
        # TODO: A message that includes the backend id that doesn't exist, perhaps?
        pass

    @property
    def backends(self):
        return self._backends

    def get_backend(self, id):
        for backend in self._backends:
            if getattr(backend, 'id', None) == id:
                return backend
        raise TaskScheduler.BackendDoesNotExist

    def simple_task(self, fn, repeat_interval, task_id_suffix='',
        backend=None):
        """
        Registers a callable as a periodic task.
        """
        _task_id = '%s.%s%s' % (fn.__module__, fn.__name__, task_id_suffix)
        _repeat_interval = repeat_interval
        _backend = backend

        # Create a PeriodicTask subclass that wraps the function.
        class DecoratedTask(PeriodicTask):
            backend = _backend
            task_id = _task_id
            repeat_interval = _repeat_interval

            def run(self, *args, **kwargs):
                fn(*args, **kwargs)

        self.task(DecoratedTask)
        return DecoratedTask

    def task(self, task):
        """
        Registers a periodic task.
        """
        if inspect.isclass(task):
            task = task()

        # If classes are used for backend properties, the TaskScheduler will
        # only create one instance. If you need unique instances, you must
        # instantiate them yourself.
        backend = getattr(task, 'backend', None) or settings.DEFAULT_BACKEND
        if inspect.isclass(backend):
            cls = backend
            try:
                backend = self._backend_singletons[cls]
            except KeyError:
                backend = self._backend_singletons[cls] = cls()
        self._backends.add(backend)
        backend.schedule(task)

        print 'registering %s with id %s' % (task, task.task_id)


schedule = TaskScheduler()
autodiscover()
