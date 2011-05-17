from django.core.management.base import BaseCommand, CommandError
from ... import register as task_registry


class Command(BaseCommand):
    help = "Runs scheduled tasks."

    def handle(self, *args, **options):
        if len(args) == 0:
            backends = task_registry.backends
        else:
            backends = [task_registry.get_backend(id) for id in args]
        
        for backend in backends:
            print backend
            backend.run_scheduled_tasks()
