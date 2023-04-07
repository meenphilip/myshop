import os
from celery import Celery

# set the default Django settings module for the 'celry' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE","myshop.settings")

app = Celery("myshop")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
