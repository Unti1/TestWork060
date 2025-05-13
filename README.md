# Transaction Service

REST API микросервис для работы с транзакциями.

## Требования

- Python 3.11+
- Docker и Docker Compose
- Poetry (для локальной разработки)

## Локальный запуск

1. Установите зависимости:
```bash
poetry install
```

2. Создайте файл .env:
```bash
cp .env.example .env
```

3. Запустите базу данных и Redis:
```bash
docker-compose up -d db redis
```

4. Запустите приложение:
```bash
poetry run python webapp.py
```

5. В отдельном терминале запустите Celery worker:
```bash
poetry run celery -A tasks.update_statistics worker --loglevel=info
```

## Запуск через Docker Compose

1. Соберите и запустите все сервисы:
```bash
docker-compose up --build
```

## API Документация

После запуска приложения, документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Тесты

Для запуска тестов:
```bash
poetry run pytest
```

## API Endpoints

### POST /transactions
Загрузка новой транзакции.

### DELETE /transactions
Удаление всех транзакций.

### GET /statistics
Получение статистики по транзакциям.

## Безопасность

Все эндпоинты защищены API ключом. Ключ должен передаваться в заголовке:
```
Authorization: ApiKey <your_api_key>
``` 