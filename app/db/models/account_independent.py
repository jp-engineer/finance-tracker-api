from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class AccountIndependent(Base):
    __tablename__ = "accounts_independent"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts_all.id"), unique=True)

    account = relationship("AccountAll", back_populates="independent_account")
