# Dockerfile
FROM python:3.11.2-slim

# Установить рабочую директорию
WORKDIR /app

# Скопировать requirements.txt и установить зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать весь проект в контейнер
COPY . .

# Установить переменную окружения для FastAPI
ENV PYTHONPATH=/app

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
