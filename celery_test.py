import time

from celery import Celery

from image_conf import make_resize

# celery -A celery_test.celery worker --loglevel=info

celery = Celery(
    'celery_test',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@celery.task
def process_image(image_data, filename, sizes):
    make_resize(image_data, filename, sizes)
    time.sleep(2)

    return f'Image resized'

