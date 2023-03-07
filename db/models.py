import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    __tablename__ = "user_data"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    wallets = relationship("Wallet")
    transactions = relationship("Transaction")


class Wallet(Base):
    __tablename__ = "wallet_data"
    wallet_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_data.user_id"))
    balance = Column(Numeric, nullable=False)


class Transaction(Base):
    __tablename__ = "transaction_data"
    transaction_id = Column(Numeric, primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_data.user_id"))
    wallet_id = Column(Integer, ForeignKey("wallet_data.wallet_id"))
    ammount = Column(Numeric, nullable=False)
