from django.core.management.base import BaseCommand, CommandError
from ... import schedule as task_scheduler
from optparse import make_option


class Command(BaseCommand):
    help = "Runs scheduled tasks."

    option_list = BaseCommand.option_list + (
        make_option('--backends',
            dest='backends',
            action='append',
            default=None,
            help='A list of backends that should run their scheduled tasks.'
        ),
    )

    def handle(self, *args, **options):
        backends = options.get('backends', task_scheduler.backends)
        task_ids = args
        
        backend_ids = options.get('backends', None)
        if backend_ids:
            backends = [task_scheduler.get_backend(id) for id in args]
        else:
            backends = task_scheduler.backends
        
        for backend in backends:
            if task_ids:
                tasks = set([task for task in backend.scheduled_tasks if task.task_id in task_ids])
            else:
                tasks = backend.scheduled_tasks
            backend.run_scheduled_tasks(tasks)
