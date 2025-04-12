from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from finance_tracker_shared.schemas.enums import FolioCategoryEnum

from app.db.models.base_class import Base


class Folio(Base):
    __tablename__ = "folios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(Enum(FolioCategoryEnum), nullable=False)
    subcategory = Column(String, nullable=False)

    payments = relationship("TransactionPayment", back_populates="folio")
    expenses = relationship("TransactionExpense", back_populates="folio")