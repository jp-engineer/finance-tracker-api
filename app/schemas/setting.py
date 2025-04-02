from pydantic import BaseModel, model_validator, ValidationError
from app.schemas.enums import SettingCategoryEnum
import pycountry

DATE_FORMATS = {"dd-mm-yyyy", "mm-dd-yyyy", "yyyy-mm-dd"}
DAYS_LONG = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
DAYS_SHORT = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}

class SettingBase(BaseModel):
    key: str
    value: str
    category: SettingCategoryEnum

    @model_validator(mode="after")
    def validate_combination(self) -> "SettingBase":
        k = self.key
        v = self.value
        c = self.category

        if c == "general" and k == "country_code":
            if not pycountry.countries.get(alpha_2=v.upper()):
                raise ValueError(f"Invalid country code: {v}")
        
        elif c == "view" and k == "default_currency":
            if not pycountry.currencies.get(alpha_3=v.upper()):
                raise ValueError(f"Invalid currency code: {v}")
        
        elif c == "view" and k == "date_format":
            if v.lower() not in {"dd-mm-yyyy", "mm-dd-yyyy", "yyyy-mm-dd"}:
                raise ValueError(f"Invalid date format: {v}")
        
        elif c == "view" and k == "week_starts_on":
            if v.lower() not in DAYS_LONG and v.lower() not in DAYS_SHORT:
                raise ValueError(f"Invalid week start day: {v}")
        
        return self

class SettingCreate(SettingBase): pass

class SettingRead(SettingBase):
    id: int

    model_config = {
        "from_attributes": True
    }