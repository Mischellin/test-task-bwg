from fastapi import APIRouter

from .transaction_views import transaction_router

api_router = APIRouter()
api_router.include_router(transaction_router, prefix="", tags=["Transactions"])
