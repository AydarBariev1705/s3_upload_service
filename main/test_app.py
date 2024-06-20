from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase
from fastapi.testclient import TestClient

from main.app import app
from main.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, FILE_URL
from main.models import ImageORM

DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase, ):
    pass


client = TestClient(app)


async def test_get_status_bad():
    response = client.get("/projects/-10/images", )

    assert response.json() == [{'error': 'Project id: -10 not found'}, 404]


async def test_get_status_str():
    response = client.get("/projects/str/images", )

    assert response.json() == {
        'detail':
            [
                {
                    'input': 'str',
                    'loc': ['path', 'project_id'],
                    'msg': 'Input should be a valid integer, unable to parse string '
                           'as an integer',
                    'type': 'int_parsing'
                },
            ],
    }


async def test_upload_file():
    file_content = b"test file content"

    response = client.post(
        "images/?project_id=222",
        files={"file": ("test_file.png", file_content, "image/png")},
    )
    assert response.json() == {'upload_link': f'{FILE_URL}test_file.png'}
    async with async_session() as session:
        query = delete(ImageORM).where(ImageORM.project_id == 222)
        await session.execute(query)
        await session.commit()


async def test_upload_bad_file():
    file_content = b"test file content"

    response = client.post(
        "images/?project_id=123456",
        files={"file": ("test_file.txt", file_content, "text/plain")},
    )
    assert response.json() == [{'error': 'Extension:txt not allowed!'}, 400]
