from celery import Celery
from django.conf import settings
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev_settings')

app = Celery('interview', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='interview')

# 自动加载任务
app.autodiscover_tasks()


@app.task
def debug():
    print('DEBUG')


