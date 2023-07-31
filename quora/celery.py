import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quora.settings')
app = Celery('Quora_Celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'run-task-every-10-mins': {
#         'task': 'questions.tasks.print_func',  # Update with the correct path to your task function
#         'schedule': timedelta(minutes=1),
#     },
# }
