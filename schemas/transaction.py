from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    id: str
    user_id: str
    amount: Decimal
    currency: str
    timestamp: datetime

class TransactionResponse(BaseModel):
    message: str
    task_id: str

class StatisticsResponse(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: list[dict[str, float]]