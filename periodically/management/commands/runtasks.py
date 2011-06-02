from django.core.management.base import BaseCommand, CommandError
from ... import register as task_scheduler
from optparse import make_option
from ...settings import BACKEND_GROUPS


class InvalidBackendGroupError(Exception):
    def __init__(self, backend_group):
        Exception.__init__(self, '%s is not a valid backend group' % backend_group)


class InvalidBackendError(Exception):
    def __init__(self, backend):
        Exception.__init__(self, 'Could not find backend %s' % backend)


class Command(BaseCommand):
    help = "Runs scheduled tasks."

    option_list = BaseCommand.option_list + (
        make_option('--backend',
            dest='backend_groups',
            type='string',
            action='append',
            default=None,
            help='A list of backend groups that should run their scheduled tasks. Backend groups can be defined in your settings.py f'
        ),
    )

    def handle(self, *args, **options):
        task_ids = args
        backend_groups = options.get('backend_groups', None)
        
        if backend_groups:
            backend_classes = set()
            for backend_group in backend_groups:
                try:
                    backend_paths = BACKEND_GROUPS[backend_group]
                except KeyError:
                    raise InvalidBackendGroupError(backend_group)

                for backend_path in backend_paths:
                    mod_path, cls_name = backend_path.rsplit('.', 1)
                    try:
                        mod = importlib.import_module(mod_path)
                        backend_class = getattr(mod, cls_name)
                    except (AttributeError, ImportError):
                        raise InvalidBackendError("Could not find backend '%s'" % backend_path)

                    backend_classes.add(backend_class)
            backends = [backend_class() for backend_class in backend_classes]
        else:
            backends = task_scheduler.backends
        
        for backend in backends:
            if task_ids:
                tasks = set([task for task in backend.scheduled_tasks if task.task_id in task_ids])
            else:
                tasks = backend.scheduled_tasks
            backend.run_scheduled_tasks(tasks)
