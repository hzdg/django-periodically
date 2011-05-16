from django.core.management.base import BaseCommand, CommandError
from periodically import get_command_backend

class Command(BaseCommand):
    help = "Testing command-based periodic tasks. DELETE ME."

    def handle(self, *args, **options):
        
        backend = get_command_backend()
        if backend:
            return backend.execute()
        else:
            return "No tasks scheduled to run via command."
