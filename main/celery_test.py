import time

from celery import Celery

from main.image_conf import make_resize
from main.config import REDIS


celery = Celery(
    'celery_test',
    broker=f'redis://{REDIS}:6379/0',
    backend=f'redis://{REDIS}:6379/0',
)


@celery.task
def process_image(image_data, filename, sizes):
    make_resize(image_data, filename, sizes)
    time.sleep(2)

    return f'Image resized'

