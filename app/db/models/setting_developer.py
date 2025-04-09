from sqlalchemy import Column, Integer, String
from app.db.models import Base

class SettingDeveloper(Base):
    __tablename__ = "settings_developer"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False, unique=True)
    norm_key = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False)
    
