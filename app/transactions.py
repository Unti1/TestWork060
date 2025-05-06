from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException


from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionResponse
from settings.config import api_key_auth, redis_client
from tasks.update_statistics import update_statistics

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    dependencies=[Depends(api_key_auth)],
)
async def create_transaction(transaction: TransactionCreate):
    # Check for duplicate transaction_id
    if await Transaction.get(id=transaction.id):
        raise HTTPException(status_code=400, detail="Transaction ID already exists")

    # Save to database
    transaction_id = await Transaction.create(**dict(transaction))
    # Trigger Celery task
    result = update_statistics.delay(dict(transaction))
    return {"message": "Transaction received", "task_id": result.id}


@router.delete("/transactions", dependencies=[Depends(api_key_auth)])
async def delete_transactions():
    # Delete all transactions
    await Transaction.delete()

    # Reset statistics in Redis
    redis_client.set("stats:total_transactions", 0)
    redis_client.set("stats:total_amount", 0)
    redis_client.delete("stats:top_transactions")
    return {"message": "Transactions deleted"}
