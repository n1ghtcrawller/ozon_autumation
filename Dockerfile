# Базовый образ с Python и Alpine (легковесный)
FROM python:3.11-alpine

# Установка системных зависимостей
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    chromium \
    chromium-chromedriver \
    tzdata \
    && pip install --upgrade pip

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Настройка переменных окружения для Chrome
ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/lib/chromium/ \
    DISPLAY=:99 \
    PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python", "main.py"]