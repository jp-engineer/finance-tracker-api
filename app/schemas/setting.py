from pydantic import BaseModel
from app.schemas.enums import SettingCategoryEnum

class SettingBase(BaseModel):
    key: str
    value: str
    category: SettingCategoryEnum

class SettingCreate(SettingBase):
    pass

class SettingRead(SettingBase):
    id: int

    class Config:
        orm_mode = True
