import django.dispatch

task_complete = django.dispatch.Signal(providing_args=['task', 'extra'])
