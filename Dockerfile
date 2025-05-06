# Базовый образ Python
FROM python:3.9-slim

# Установка рабочей директории
WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копирование файлов конфигурации Poetry
COPY pyproject.toml poetry.lock ./

# Установка зависимостей через Poetry
# Отключаем создание виртуального окружения, так как оно не нужно в контейнере
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копирование остального кода приложения
COPY . .

# Команда для запуска приложения
CMD ["python3.11", "webapp.py"]