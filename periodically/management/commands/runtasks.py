from django.core.management.base import BaseCommand, CommandError
from ... import schedule as task_scheduler


class Command(BaseCommand):
    help = "Runs scheduled tasks."

    def handle(self, *args, **options):
        if len(args) == 0:
            backends = task_scheduler.backends
        else:
            backends = [task_scheduler.get_backend(id) for id in args]
        
        for backend in backends:
            backend.run_scheduled_tasks()
