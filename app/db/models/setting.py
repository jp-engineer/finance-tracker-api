# from sqlalchemy import Column, Integer, String, Enum
# from app.db.models.base_class import Base
# from app.schemas.enums import SettingCategoryEnum

# class Setting(Base):
#     __tablename__ = "settings"

#     id = Column(Integer, primary_key=True, index=True)
#     key = Column(String, nullable=False, unique=True)
#     value = Column(String, nullable=False)
#     category = Column(Enum(SettingCategoryEnum), nullable=False)
