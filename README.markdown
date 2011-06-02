Periodically lets you define periodic tasks in Python, and then run them however you want (think cron job).


Goals
-------

1. Tasks and their schedules should be defined in Python—not crontabs or the database.
2. There should be multiple ways to trigger tasks, but only one syntax for defining them. Just because you trigger your tasks with a cron job on one server doesn't mean you can always do that. When you can't, you shouldn't have to rewrite all your code—just change a setting.
3. The system should be highly flexible, but…
4. …there should be shortcuts for the most common schedules (hourly, daily, etc.).
5. The system should try to recover gracefully, but…
6. …it should also alert the administrators if anything goes wrong.


Installation
------------

1. `pip install git+https://github.com/hzdg/django-periodically.git#egg=django-periodically`
2. Add 'periodically' to your `INSTALLED_APPS` in settings.py.


Usage
-----

### Defining and Scheduling Tasks

Periodically gives you a few ways to schedule periodic tasks. The easiest is to use the included decorators:

    from periodically.decorators import *
    
    @hourly()
    def my_task():
        print 'Do something!'
    
    @every(minutes=45)
    def my_other_task():
        print 'Do something else every 45 minutes!'

However, you can also define task classes:

    from periodically.tasks import PeriodicTask
    from periodically import register
    from periodically.schedules import Daily
    
    # Define the task.
    class MyTask(PeriodicTask):
        def run(self):
            print 'Do something.'
    
    # Schedule the task.
    register.task(MyTask(), Daily())

Tasks can be scheduled anywhere in your project, but Periodically automatically looks for a `periodictasks` module in your `INSTALLED_APPS`, so it's probably a good idea to define all your tasks in `myapp/periodictasks.py`.

### Running Your Tasks

Periodically uses a pluggable backend system to decouple the defining and scheduling of your tasks from their execution. **The default backend will not run your tasks automatically**, so you need to tell it to by using the `runtasks` management command. Generally, you would use a cronjob (or similar) to do this.  For example, placing the following line in your crontab file would check for tasks that need to be run every five minutes:

    */5 * * * * /path/to/manage.py runtasks

### Logging

Periodically uses Django's logging system to let you know when something goes wrong. To enable this, just add a "periodically" logger to your `settings.py` file:

    LOGGING = {
	    ...
        # This part should be in your settings file by default.
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            ...
            # Add the following to enable logging for Periodically.
            'periodically': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }

This is a relatively simple setup that will send an email to the site admins whenever a periodic task fails, but Django is capable of much more. For more information, check out [the Django docs](https://docs.djangoproject.com/en/dev/topics/logging/).

