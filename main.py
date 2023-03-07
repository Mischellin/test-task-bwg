from fastapi import FastAPI

from app import transaction_api

app = FastAPI(
    title="Test_task_api",
    openapi_url="/openapi.json",
)

app.include_router(transaction_api.api_router)
