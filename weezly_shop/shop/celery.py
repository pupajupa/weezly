from celery import Celery
from celery.schedules import crontab

app = Celery('online_shop')

app.conf.beat_schedule = {
    'check_price_tracking_every_10_minutes': {
        'task': 'shop.tasks.check_price_tracking',
        'schedule': crontab(minute='*/10'),
    },
}