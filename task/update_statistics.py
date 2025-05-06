from celery import Celery
import redis

celery = Celery('tasks', broker='redis://redis:6379/0')

@celery.task
def update_statistics(transaction_data):
    r = redis.Redis(host='redis', port=6379, db=0)
    r.incr("stats:total_transactions")
    amount = transaction_data["amount"]
    r.incrbyfloat("stats:total_amount", amount)
    transaction_id = transaction_data["transaction_id"]
    r.zadd("stats:top_transactions", {transaction_id: amount})