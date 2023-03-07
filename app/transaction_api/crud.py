import datetime
from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.models import Transaction, User, Wallet

from .schemas import AddCoin, RemoveCoin, TransactionBase


class CRUDUser:
    def __init__(self) -> None:
        self.model = User

    def get_by_id(self, db: Session, user_id: UUID) -> User:
        obj = db.query(self.model).filter(self.model.user_id == user_id).one_or_none()
        return obj

    def create(self, db: Session) -> User:
        obj = self.model()
        obj.wallets.append(Wallet(balance=1000.1))
        db.add(obj)
        db.commit()
        return obj


class CRUDTransaction:
    def __init__(self) -> None:
        self.model = Transaction

    def get_by_id(self, db: Session, transaction_id: int) -> Transaction:
        obj = (
            db.query(self.model)
            .filter(self.model.transaction_id == transaction_id)
            .one_or_none()
        )
        return obj

    def create(self, db: Session, obj_in):
        if not isinstance(obj_in, dict):
            obj_in = jsonable_encoder(obj_in, by_alias=False)

        db_obj = self.model()
        db.add(db_obj)
        # TODO закончить добавление транзакции

        pass


class CRUDWallet:
    def __init__(self) -> None:
        self.model = Wallet

    def check_coin(self, db: Session, msg: AddCoin):
        obj = db.query(self.model).filter(self.model.wallet_id == msg.wallet_id).one()
        if msg.ammount <= obj.balance:
            return True
        else:
            return False

    def add_coin(self, db: Session, msg: AddCoin):
        obj = db.query(self.model).filter(self.model.wallet_id == msg.wallet_id).one()
        obj.balance += msg.ammount
        db.add(obj)
        db.commit()

    def remove_coin(self, db: Session, msg: RemoveCoin):
        obj = db.query(self.model).filter(self.model.wallet_id == msg.wallet_id).one()
        obj.balance -= msg.ammount
        db.add(obj)
        db.commit()
