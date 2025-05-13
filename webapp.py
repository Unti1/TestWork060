from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.statistic import router as statistics_router
from app.transactions import router as transactions_router

app = FastAPI(
    title="Transaction Service",
    description="REST API микросервис для работы с транзакциями",
    version="1.0.0"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

# App inicialize
app = FastAPI(lifespan=lifespan)



# Подключаем роутеры
app.include_router(transactions_router)
app.include_router(statistics_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
