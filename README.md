# Описание проекта
Проект представляет собой сервис для обработки фотографий и загрузки в s3 хранилище.


## Используемые инструменты
* **Python** (3.10);
* **FastApi** (asynchronous Web Framework);
* **Docker** and **Docker Compose** (containerization);
* **PostgreSQL** (database);
* **SQLAlchemy** (working with database from Python);
* **Pytest** (tests);
* **Celery**;
* **Redis**;
* **Botocore** (s3 storage).
* **Celery**

## Сборка и запуск приложения
1. Переименовать .env.template в .env
2. Заполнить необходимые данные в .env файле
3. Собрать и запустить контейнеры с приложением. В терминале в общей директории (с файлом "docker-compose.yml") 
вводим команду:
    ```
    docker-compose up -d
    ```
4. Запускаем скрипт внутри контейнера с API для создания DB:
    ```
    docker-compose exec app python3 -m main.models
    ```

## Документация

После сборки и запуска приложения ознакомиться с документацией API можно по адресу:
    ```
    0.0.0.0:8000/docs/
    ```

