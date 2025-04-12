from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base_class import Base


class TransactionTransfer(Base):
    __tablename__ = "transactions_transfer"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions_all.id"), unique=True)
    from_account_id = Column(Integer, ForeignKey("accounts_all.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("accounts_all.id"), nullable=False)

    from_account = relationship(
        "AccountAll",
        foreign_keys=[from_account_id],
        back_populates="transfers_sent"
    )

    to_account = relationship(
        "AccountAll",
        foreign_keys=[to_account_id],
        back_populates="transfers_received"
    )

    transaction = relationship(
        "TransactionAll",
        back_populates="transfer"
    )