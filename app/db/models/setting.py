from sqlalchemy import Column, Integer, String, Enum
from app.schemas.enums import SettingCategoryEnum
from app.db.base_class import Base

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False)
    category = Column(Enum(SettingCategoryEnum), nullable=False)
