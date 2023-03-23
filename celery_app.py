from celery import Celery
from celery.schedules import crontab
from django.conf import settings
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev_settings')
app = Celery('interview', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings', namespace='interview')

# 自动加载任务
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(name):
    print(name)


@app.task
def debug():
    print('DEBUG')
