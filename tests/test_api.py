from fastapi.testclient import TestClient
from webapp import app

client = TestClient(app)

def test_create_transaction():
    response = client.post(
        "/transactions",
        json={
            "transaction_id": "test1",
            "user_id": "user1",
            "amount": 100.0,
            "currency": "USD",
            "timestamp": "2024-12-12T12:00:00"
        },
        headers={"Authorization": "ApiKey your_api_key"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction received"

def test_delete_transactions():
    response = client.delete("/transactions", headers={"Authorization": "ApiKey your_api_key"})
    assert response.status_code == 200
    assert response.json()["message"] == "Transactions deleted"

def test_get_statistics():
    # Добавляем несколько транзакций
    for i in range(1, 6):
        client.post(
            "/transactions",
            json={
                "transaction_id": f"test{i}",
                "user_id": "user1",
                "amount": i * 100.0,
                "currency": "USD",
                "timestamp": "2024-12-12T12:00:00"
            },
            headers={"Authorization": "ApiKey your_api_key"}
        )
    response = client.get("/statistics", headers={"Authorization": "ApiKey your_api_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_transactions"] == 5
    assert data["average_transaction_amount"] == 300.0
    assert len(data["top_transactions"]) == 3
    assert data["top_transactions"][0]["amount"] == 500.0