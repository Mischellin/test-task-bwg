from fastapi import APIRouter

# Depends, HTTPException
# from sqlalchemy.orm import Session
#
transaction_router = APIRouter()


@transaction_router.get("/")
def get_smoke_test():
    return {"message": "OK"}
