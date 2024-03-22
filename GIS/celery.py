# celery.py (inside your water_pipeline_GIS directory)
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_pipeline_GIS.settings')

app = Celery('water_pipeline_GIS')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-task-status': {
        'task': 'GIS.tasks.update_task_status',
        'schedule': 60.0,  # Run every minute
    },
}
