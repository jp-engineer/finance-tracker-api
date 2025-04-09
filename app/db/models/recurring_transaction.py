from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base
from finance_tracker_shared.schemas.enums import TransactionTypeEnum

class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    variable = Column(Boolean, default=False)
    estimate = Column(Float, nullable=True)

    expires = Column(Boolean, nullable=False)
    expires_after = Column(Integer, nullable=True)
    expires_on = Column(Date, nullable=True)

    ignores_bank_holidays = Column(Boolean, default=False)
    ignores_weekends = Column(Boolean, default=False)
    pays_early = Column(Boolean, default=False)

    freq_per_week = Column(Integer, nullable=True)
    freq_per_month = Column(Integer, nullable=True)
    freq_per_year = Column(Integer, nullable=True)

    week_payment_days = Column(String, nullable=True)
    month_payment_days = Column(String, nullable=True)
    month_payment_dates = Column(String, nullable=True)
    year_payment_dates = Column(String, nullable=True)

    folio_id = Column(Integer, ForeignKey("folios.id"), nullable=True)
    to_account_id = Column(Integer, ForeignKey("accounts_all.id"), nullable=True)
    from_account_id = Column(Integer, ForeignKey("accounts_all.id"), nullable=True)

    folio = relationship("Folio", backref="recurring_transactions")
    to_account = relationship("AccountAll", foreign_keys=[to_account_id], backref="recurring_transactions_in")
    from_account = relationship("AccountAll", foreign_keys=[from_account_id], backref="recurring_transactions_out")

    transactions = relationship("TransactionAll", backref="recurring_transaction")
