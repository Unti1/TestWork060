from fastapi import APIRouter, Depends
from settings.config import redis_client, api_key_auth

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/", dependencies=[Depends(api_key_auth)])
def get_statistics():
    # Retrieve statistics from Redis
    total_transactions = int(redis_client.get("stats:total_transactions") or 0)
    total_amount = float(redis_client.get("stats:total_amount") or 0)
    average = total_amount / total_transactions if total_transactions > 0 else 0

    # Get top 3 transactions
    top_transactions = redis_client.zrevrange(
        "stats:top_transactions", 0, 2, withscores=True
    )
    top_transactions_list = [
        {"transaction_id": tx_id.decode(), "amount": score}
        for tx_id, score in top_transactions
    ]

    return {
        "total_transactions": total_transactions,
        "average_transaction_amount": average,
        "top_transactions": top_transactions_list,
    }
