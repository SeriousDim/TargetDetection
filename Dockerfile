# Dockerfile
FROM python:3.11.2-slim

# Установить рабочую директорию
WORKDIR /app

# Скопировать requirements.txt и установить зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать весь проект в контейнер
COPY . /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Команда запуска
CMD ["python", "run.py"]
