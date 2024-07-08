import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal_project.settings')

app = Celery('NewsPortal_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_new_post_notify': {
        'task': 'NewsPortal_app.tasks.weekly_new_post_notification',
        'schedule': crontab(minute='0', hour='8', day_of_week='mon'),
    },
}


