# tasks.py (inside your GIS app)
from celery import shared_task
from django.utils import timezone
from .models import Task

@shared_task
def update_task_status():
    tasks = Task.objects.filter(start_date__lte=timezone.now(), deadline__gt=timezone.now(), status='assigned')
    for task in tasks:
        task.status = 'pending'
        task.save()

    overdue_tasks = Task.objects.filter(deadline__lte=timezone.now(), status='pending')
    for task in overdue_tasks:
        task.status = 'completed'
        task.save()
