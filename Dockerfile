# Базовый образ с Python 3.11
FROM python:3.11-alpine

# Переменные окружения
ENV TELEGRAM_BOT_USERNAME=pd_antispam_bot
ENV TELEGRAM_BOT_TOKEN=
ENV METRICS_PORT=9090
ENV METRICS_HOST=0.0.0.0

# Устанавливаем зависимости для компиляции пакетов Python
RUN apk add --no-cache gcc musl-dev libffi-dev bash

# Создаём рабочую директорию
WORKDIR /app

# Копируем проект в контейнер
COPY . /app

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаём директорию для хранения данных (FileSystem storage)
RUN mkdir -p /app/storage

# Команда запуска бота
CMD ["python", "./main.py"]
