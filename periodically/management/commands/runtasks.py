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
            help='The scheduler group that should run its scheduled tasks. Groups can be defined in your settings.py file.',
        ),
        make_option('--force',
            dest='force_execution',
            action='store_true',
            default=False,
            help='Use this flag to run tasks regardless of whether they are scheduled to be run.',
        ),
        make_option('--fake',
            dest='fake',
            action='store_true',
            default=None,
            help='Use this flag to create execution records for tasks without actually running them. If the flag is not used, the backend will decide whether to fake tasks.',
        ),
    )

    def handle(self, *args, **options):
        task_ids = args
        backend_groups = options.get('backend_groups', None)
        fake = options['fake']
        force_execution = options['force_execution']
        
        if backend_groups:
            backends = get_scheduler_backends_in_groups(backend_groups)
        else:
            backends = task_scheduler.backends
        
        for backend in backends:
            if task_ids:
                tasks = set([task for task in backend.tasks if task.task_id in task_ids])
            else:
                tasks = backend.tasks
            if force_execution:
                backend.run_tasks(tasks, fake=fake)
            else:
                backend.run_scheduled_tasks(tasks, fake=fake)
