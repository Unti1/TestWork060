from celery import Celery
from settings.config import redis_client

celery_app = Celery('tasks', broker='redis://redis:6379/0')

@celery_app.task
def update_statistics(transaction_id: str, amount: float):
    # Обновляем общее количество транзакций
    redis_client.incr("stats:total_transactions")
    
    # Обновляем общую сумму
    redis_client.incrbyfloat("stats:total_amount", amount)
    
    # Обновляем топ транзакции используя Redis Sorted Set
    redis_client.zadd("stats:top_transactions", {transaction_id: amount})
    
    # Оставляем только топ-3 транзакции
    redis_client.zremrangebyrank("stats:top_transactions", 0, -4) 