from celery import Celery
import redis
from settings.config import settings

# Инициализация Celery
celery = Celery('tasks', broker=settings.get_redis_url())

@celery.task
def update_statistics(transaction_data):
    # Подключение к Redis
    r = redis.Redis.from_url(settings.get_redis_url())
    
    # Обновление статистики
    r.incr("stats:total_transactions")
    amount = transaction_data["amount"]
    r.incrbyfloat("stats:total_amount", amount)
    transaction_id = transaction_data["transaction_id"]
    r.zadd("stats:top_transactions", {transaction_id: amount})