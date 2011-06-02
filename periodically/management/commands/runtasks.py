from django.core.management.base import BaseCommand, CommandError
from ... import register as task_scheduler
from optparse import make_option
from ...utils import get_scheduler_backends_in_groups


class InvalidBackendGroupError(Exception):
    def __init__(self, backend_group):
        Exception.__init__(self, '%s is not a valid backend group' % backend_group)


class InvalidBackendError(Exception):
    def __init__(self, backend):
        Exception.__init__(self, 'Could not find backend %s' % backend)


class Command(BaseCommand):
    help = "Runs scheduled tasks."

    option_list = BaseCommand.option_list + (
        make_option('--group',
            dest='backend_groups',
            type='string',
            action='append',
            default=None,
            help='The scheduler group that should run its scheduled tasks. Groups can be defined in your settings.py file.'
        ),
    )

    def handle(self, *args, **options):
        task_ids = args
        backend_groups = options.get('backend_groups', None)
        
        if backend_groups:
            backends = get_scheduler_backends_in_groups(backend_groups)
        else:
            backends = task_scheduler.backends
        
        for backend in backends:
            if task_ids:
                tasks = set([task for task in backend.scheduled_tasks if task.task_id in task_ids])
            else:
                tasks = backend.scheduled_tasks
            backend.run_scheduled_tasks(tasks)
