import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.pika_client import PikaClient
from db.deps import get_db

from . import crud
from .schemas import AddCoin, RemoveCoin

transaction_router = APIRouter()


@transaction_router.post("/create_queue")
async def create_queue(qeue_name: str):
    pika_client = PikaClient(queue_name=qeue_name)
    loop = asyncio.get_running_loop()
    task = loop.create_task(pika_client.consume(loop))
    await task


@transaction_router.get("/")
def get_smoke_test():
    return {"message": "OK"}


@transaction_router.patch("/add-coins")
async def add_coins_balance(
    msg: AddCoin, queue_name: str, db: Session = Depends(get_db)
):
    # crud.CRUDWallet().add_coin(db=db,msg=msg)
    print(True)
    pika_client = PikaClient(queue_name=queue_name)
    pika_client.send_message(message=msg)
    await create_queue(qeue_name=queue_name)
    return HTTPException(status_code=200)


@transaction_router.patch("/remove-coins")
async def remove_coins_balance(
    msg: RemoveCoin, queue_name: str, db: Session = Depends(get_db)
):
    # crud.CRUDWallet().remove_coin(db=db,msg=msg)
    if not crud.CRUDWallet().check_coin(db=db, msg=msg):
        raise HTTPException(status_code=403, detail="not enough funds on the balance")
    else:
        pika_client = PikaClient(queue_name=queue_name)
        pika_client.send_message(message=msg)
        await create_queue(qeue_name=queue_name)
        return HTTPException(status_code=200)


@transaction_router.post("/create-user")
def create_user(db: Session = Depends(get_db)):
    user = crud.CRUDUser().create(db=db)
    return user.user_id, user.wallets[0]
