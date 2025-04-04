from sqlalchemy import Column, Integer, String, Enum
from app.schemas.enums import FolioCategoryEnum
from app.db.models.base_class import Base

class Folio(Base):
    __tablename__ = "Folios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(Enum(FolioCategoryEnum), nullable=False)
    subcategory = Column(String, nullable=False)
