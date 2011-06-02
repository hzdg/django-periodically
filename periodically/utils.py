from django.utils import importlib
from . import settings


class InvalidBackendAliasError(Exception):
    def __init__(self, backend):
        Exception.__init__(self, "There is no scheduler backend with alias '%s'" % backend)


class InvalidBackendError(Exception):
    def __init__(self, backend):
        Exception.__init__(self, 'Could not find backend %s' % backend)


def get_scheduler_backend_class(backend_alias=None):
    """
    Accepts a scheduler alias and returns the corresponding backend class.
    """
    if backend_alias is None:
        backend_alias = 'default'

    try:
        class_path = settings.SCHEDULERS[backend_alias].get('backend')
    except KeyError:
        raise InvalidBackendAliasError(backend_alias)

    mod_path, cls_name = class_path.rsplit('.', 1)    
    try:
        mod = importlib.import_module(mod_path)
        backend_class = getattr(mod, cls_name)
    except (AttributeError, ImportError):
        raise InvalidBackendError(class_path)
    
    return backend_class


def get_scheduler_backends_in_groups(groups):
    backend_aliases = set()
    for group in groups:
        for alias, info in settings.SCHEDULERS.items():
            if group in info.get('groups', []):
                backend_aliases.add(alias)
    return [get_scheduler_backend_class(alias)() for alias in backend_aliases]
