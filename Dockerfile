FROM python:3.11

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./main /app/main
WORKDIR /app

CMD ["uvicorn", "main.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]