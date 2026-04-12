from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_system.settings')

app = Celery('parking_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
