from fastapi import APIRouter, Depends
from settings.config import api_key_auth, redis_client
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionResponse
from tasks.update_statistics import update_statistics

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse, dependencies=[Depends(api_key_auth)])
async def create_transaction(
    transaction: TransactionCreate,
):
    # Save to database
    result = await Transaction.create(**dict(transaction))
    # Trigger Celery task
    update_statistics.delay(transaction.id, transaction.amount)
    return {"message": "Transaction received", "task_id": result.id}


@router.delete("/", dependencies=[Depends(api_key_auth)])
async def delete_transactions():
    # Удаляем все транзакции
    await Transaction.delete()
    
    # Очищаем статистику в Redis
    redis_client.delete("stats:total_transactions")
    redis_client.delete("stats:total_amount")
    redis_client.delete("stats:top_transactions")
    
    return {"message": "Transactions deleted"}
