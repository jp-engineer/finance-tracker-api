from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class TransactionPayment(Base):
    __tablename__ = "transactions_payment"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions_all.id"), unique=True)
    to_account_id = Column(Integer, ForeignKey("accounts_all.id"), nullable=False)
    folio_id = Column(Integer, ForeignKey("folios.id"), nullable=False)

    to_account = relationship("AccountAll", back_populates="payments_received")
    folio = relationship("Folio", back_populates="payments")
    transaction = relationship("TransactionAll", back_populates="payment")
