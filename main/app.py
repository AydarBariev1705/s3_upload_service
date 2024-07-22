import aiofiles
from celery import group
from fastapi import FastAPI, UploadFile

from sqlalchemy import select
import os
from main.config import FILE_URL, ALLOWED_EXTENSION, PREFIX_SIZES

from main.celery_test import process_image, celery
from main.database import async_session
from main.models import ImageORM

app = FastAPI()


@app.post("/images/")
async def upload_file(file: UploadFile, project_id: int):
    extension = file.filename.split('.')[-1]
    if extension in ALLOWED_EXTENSION:
        async with async_session() as session:
            project = await session.scalar(
                select(ImageORM).where(ImageORM.project_id == project_id),
            )
        if not project:
            async with aiofiles.open(file.filename, 'wb', ) as out_file:
                content = await file.read()
                task_group = group(
                    process_image.s(
                        image_data=content,
                        filename=key + file.filename,
                        sizes=value,
                    )
                    for key, value in PREFIX_SIZES.items()
                )
                result = task_group.apply_async()
                result.save()
                async with async_session() as session:
                    session.add(
                        ImageORM(
                            project_id=project_id,
                            filename=file.filename,
                            celery_id=result.id,
                        )
                    )
                    await session.commit()
            os.remove(file.filename)
            return {
                'upload_link': f'{FILE_URL}{file.filename}',
            }
        else:
            return {
                'error': f'Project id: {project_id} already exists'
            }, 400
    else:
        return {
            'error': f'Extension:{extension} not allowed!'
        }, 400


@app.get('/projects/{project_id}/images', )
async def get_status(project_id: int):
    async with async_session() as session:
        image = await session.scalar(
            select(
                ImageORM
            ).where(
                ImageORM.project_id == project_id
            ),
        )
    if image:
        result = celery.GroupResult.restore(image.celery_id)
        if result:
            state = result.completed_count() / len(result)
            if state == 0:
                state = 'init'
            elif 0 < state < 1:
                state = 'processing'
            elif state == 1:
                state = 'done'

            return {'images':
                [
                    {'image_id': image.id,
                     'state': state,
                     'project_id': image.project_id,
                     'versions': {
                         'original': f'{FILE_URL}{image.filename}',
                         'thumb': f'{FILE_URL}thumb_{image.filename}',
                         'big_thumb': f'{FILE_URL}big_thumb_{image.filename}',
                         'big_1920': f'{FILE_URL}big_1920_{image.filename}',
                         'd2500': f'{FILE_URL}d2500_{image.filename}',
                     },
                     },
                ],
            }, 200
        else:
            return {
                'error': f'Celery id not found'
            }, 404

    else:
        return {
            'error': f'Project id: {project_id} not found'
        }, 404
