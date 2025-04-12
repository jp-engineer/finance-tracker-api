from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base_class import Base


class AccountCredit(Base):
    __tablename__ = "accounts_credit"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts_all.id"), unique=True)
    credit_limit = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    minimum_payment_pct = Column(Float, nullable=False)
    due_date = Column(Integer, nullable=False)

    account = relationship("AccountAll", back_populates="credit_account")