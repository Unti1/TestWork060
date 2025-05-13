import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from webapp import app
from settings.config import redis_client
from settings.database import Base, engine
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    redis_client.flushall()

def test_create_transaction():
    transaction_data = {
        "transaction_id": "test123",
        "user_id": "user_001",
        "amount": 150.50,
        "currency": "USD",
        "timestamp": datetime.now().isoformat()
    }
    
    response = client.post(
        "/transactions/",
        json=transaction_data,
        headers={"Authorization": "ApiKey test_key"}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction received"
    assert "task_id" in response.json()

def test_delete_transactions():
    response = client.delete(
        "/transactions/",
        headers={"Authorization": "ApiKey test_key"}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "Transactions deleted"

def test_get_statistics():
    # Создаем тестовые данные
    redis_client.set("stats:total_transactions", 3)
    redis_client.set("stats:total_amount", 450.50)
    redis_client.zadd("stats:top_transactions", {
        "tx1": 200.00,
        "tx2": 150.50,
        "tx3": 100.00
    })
    
    response = client.get(
        "/statistics/",
        headers={"Authorization": "ApiKey test_key"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_transactions"] == 3
    assert data["average_transaction_amount"] == 150.17
    assert len(data["top_transactions"]) == 3 