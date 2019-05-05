from __future__ import absolute_import,unicode_literals
from celery import Celery,platforms
from django.conf import settings
import  os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocelery.settings')

# 创建celery应用
app = Celery('djangocelery')

platforms.C_FORCE_ROOT = True




app.config_from_object('django.conf:settings')
# This means that you don’t have to use multiple configuration files, and instead configure Celery directly from the Django settings.
# You can pass the object directly here, but using a string is better since then the worker doesn’t have to serialize the object.


# 如果在工程的应用中创建了tasks.py模块，那么Celery应用就会自动去检索创建的任务。比如你添加了一个任#务，在django中会实时地检索出来。
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# With the line above Celery will automatically discover tasks in reusable apps if you define all tasks in a separate tasks.py module.
# The tasks.py should be in dir which is added to INSTALLED_APP in settings.py.
# So you do not have to manually add the individual modules to the CELERY_IMPORT in settings.py.






@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

