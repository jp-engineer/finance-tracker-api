import enum
from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base

class SettingCategoryEnum(enum.Enum):
    GENERAL = "general"
    VIEW = "view"
    DEVELOPER = "developer"

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False)
    category = Column(Enum(SettingCategoryEnum), nullable=False)

