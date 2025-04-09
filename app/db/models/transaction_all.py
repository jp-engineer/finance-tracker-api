from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base
from finance_tracker_shared.schemas.enums import TransactionTypeEnum

class TransactionAll(Base):
    __tablename__ = "transactions_all"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=True)
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)
    paid = Column(Boolean, default=True)
    recurring_transaction_id = Column(Integer, ForeignKey("recurring_transactions.id"), nullable=True)

    payment = relationship("TransactionPayment", back_populates="transaction", uselist=False)
    expense = relationship("TransactionExpense", back_populates="transaction", uselist=False)
    transfer = relationship("TransactionTransfer", back_populates="transaction", uselist=False)
