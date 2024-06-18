from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


async def test_get_status_good():
    response = client.get("/projects/1/images", )

    assert response.status_code == 200
    assert response.json() == [
        {
            'images':
                [
                    {
                        'image_id': 1,
                        'project_id': 1,
                        'state': 'done',
                        'versions': {
                            'big_1920': 'https://62aad04c-707a-4365-a978-142464df3e4f.selstorage.ru/big_1920_1231.png',
                            'big_thumb': 'https://62aad04c-707a-4365-a978-142464df3e4f.selstorage.ru/big_thumb_1231.png',
                            'd2500': 'https://62aad04c-707a-4365-a978-142464df3e4f.selstorage.ru/d2500_1231.png',
                            'original': 'https://62aad04c-707a-4365-a978-142464df3e4f.selstorage.ru/1231.png',
                            'thumb': 'https://62aad04c-707a-4365-a978-142464df3e4f.selstorage.ru/thumb_1231.png'
                        },
                    },
                ],
        },
        200]


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
