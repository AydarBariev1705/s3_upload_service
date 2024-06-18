import os
from dotenv import load_dotenv

load_dotenv()  # Извлекаем переменные окружения из файла .env


# PostgresSQL
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
FILE_URL = os.environ.get("FILE_URL")

ALLOWED_EXTENSION = ['jpeg', 'jpg','tif', 'png', 'tiff', 'gif', 'bmp',]