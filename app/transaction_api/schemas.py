import datetime
from decimal import Decimal
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class CustomBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class TransactionBase(CustomBaseModel):
    user_id: UUID
    wallet_id: int
    ammount: float


class WalletBase(CustomBaseModel):
    wallet_id: int
    user_id: UUID
    balance: float


class UserBase(CustomBaseModel):
    user_id: UUID
    created_at: datetime.datetime
    wallets: list[WalletBase]
    transactions: list[TransactionBase]


class AddCoin(CustomBaseModel):
    wallet_id: int
    ammount: Decimal
    rem: bool


class RemoveCoin(AddCoin):
    pass
