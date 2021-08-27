import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PLANEKS.settings')
app = Celery('celery_tasks', include=['celery_tasks.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
