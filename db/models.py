import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column("wl_id", Integer, ForeignKey("wallet_data.wallet_id")),
    Column("tr_id", Integer, ForeignKey("transaction_data.transaction_id")),
)


class User(Base):
    __tablename__ = "user_data"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    wallets = relationship("Wallet")


class Wallet(Base):
    __tablename__ = "wallet_data"
    wallet_id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_data.user_id"))
    balance = Column(Numeric, nullable=False)
    transactions = relationship("Transaction", secondary=association_table)


class Transaction(Base):
    __tablename__ = "transaction_data"
    transaction_id = Column(Integer, primary_key=True, nullable=False)
    from_wallet_id = Column(UUID(as_uuid=True))
    to_wallet_id = Column(UUID(as_uuid=True))
    ammount = Column(Numeric, nullable=False)
