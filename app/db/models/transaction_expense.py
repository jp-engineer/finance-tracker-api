from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class TransactionExpense(Base):
    __tablename__ = "transactions_expense"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions_all.id"), unique=True)
    from_account_id = Column(Integer, ForeignKey("accounts_all.id"), nullable=False)
    folio_id = Column(Integer, ForeignKey("folios.id"), nullable=False)

    from_account = relationship("AccountAll", back_populates="expenses_sent")
    folio = relationship("Folio", back_populates="expenses")
    transaction = relationship("TransactionAll", back_populates="expense")
