import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "specsharing_test.settings")

app = Celery('specsharing_test')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()