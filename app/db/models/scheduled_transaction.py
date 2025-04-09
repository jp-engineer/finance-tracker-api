from sqlalchemy import Enum, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base
from finance_tracker_shared.schemas.enums import TransactionTypeEnum

class ScheduledTransaction(Base):
    __tablename__ = "scheduled_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)
    recurring_transaction_id = Column(Integer, ForeignKey("recurring_transactions.id"), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    scheduled_date = Column(Date, nullable=False)
    pending = Column(Boolean, default=True)

    folio_id = Column(Integer, ForeignKey("folios.id"), nullable=True)
    to_account_id = Column(Integer, ForeignKey("accounts_all.id"), nullable=True)
    from_account_id = Column(Integer, ForeignKey("accounts_all.id"), nullable=True)

    transaction_id = Column(Integer, ForeignKey("transactions_all.id"), nullable=True)

    recurring_transaction = relationship("RecurringTransaction", backref="scheduled_transactions")
    transaction = relationship("TransactionAll", backref="scheduled_transaction")
