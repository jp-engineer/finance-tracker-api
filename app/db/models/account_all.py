from sqlalchemy import Column, Integer, String, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base
from finance_tracker_shared.schemas.enums import AccountTypeEnum
from app.db.models.account_credit import AccountCredit
from app.db.models.account_debit import AccountDebit
from app.db.models.account_independent import AccountIndependent
from app.db.models.transaction_transfer import TransactionTransfer
from app.db.models.transaction_payment import TransactionPayment
from app.db.models.transaction_expense import TransactionExpense

class AccountAll(Base):
    __tablename__ = "accounts_all"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, nullable=False)
    currency = Column(String, default="gbp")
    starting_balance = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    account_type = Column(Enum(AccountTypeEnum), nullable=False)

    payments_received = relationship(
        "TransactionPayment",
        back_populates="to_account",
        foreign_keys=[TransactionPayment.to_account_id]
    )

    expenses_sent = relationship(
        "TransactionExpense",
        back_populates="from_account",
        foreign_keys=[TransactionExpense.from_account_id]
    )

    transfers_sent = relationship(
        "TransactionTransfer",
        back_populates="from_account",
        foreign_keys=[TransactionTransfer.from_account_id]
    )

    transfers_received = relationship(
        "TransactionTransfer",
        back_populates="to_account",
        foreign_keys=[TransactionTransfer.to_account_id]
    )

    credit_account = relationship(
        "AccountCredit",
        back_populates="account",
        uselist=False,
        foreign_keys=[AccountCredit.account_id]
    )

    debit_account = relationship(
        "AccountDebit",
        back_populates="account",
        uselist=False,
        foreign_keys=[AccountDebit.account_id]
    )

    independent_account = relationship(
        "AccountIndependent",
        back_populates="account",
        uselist=False,
        foreign_keys=[AccountIndependent.account_id]
    )
