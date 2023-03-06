from celery import Celery

from app.core.config import settings


celery = Celery(
    'worker',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    include=['app.tasks.tasks']
    )
