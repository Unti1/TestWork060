from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.statistic import router as statistic_router
from app.transactions import router as transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

# App inicialize
app = FastAPI(lifespan=lifespan)



# Connect routers
app.include_router(transactions_router)
app.include_router(statistic_router)

if __name__ == "__main__":
    uvicorn.run("webapp:app", reload=True)
