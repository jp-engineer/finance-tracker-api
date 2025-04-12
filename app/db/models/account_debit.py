from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base_class import Base


class AccountDebit(Base):
    __tablename__ = "accounts_debit"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts_all.id"), unique=True)
    overdraft_limit = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)

    account = relationship("AccountAll", back_populates="debit_account")