from pydantic import BaseModel, model_validator
import pycountry
from app.schemas.enums import SettingCategoryEnum

DATE_FORMATS = {"dd-mm-yyyy", "mm-dd-yyyy", "yyyy-mm-dd"}
DAYS_LONG = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
DAYS_SHORT = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}

class SettingBase(BaseModel):
    key: str
    value: str
    category: SettingCategoryEnum

    @model_validator(mode="after")
    def validate_combination(self) -> "SettingBase":
        key = self.key
        value = self.value
        category = self.category

        if category == "general" and key == "country_code":
            if not pycountry.countries.get(alpha_2=value.upper()):
                raise ValueError(f"Invalid country code: {value}")
        
        elif category == "view" and key == "default_currency":
            if not pycountry.currencies.get(alpha_3=value.upper()):
                raise ValueError(f"Invalid currency code: {value}")
        
        elif category == "view" and key == "date_format":
            if value.lower() not in {"dd-mm-yyyy", "mm-dd-yyyy", "yyyy-mm-dd"}:
                raise ValueError(f"Invalid date format: {value}")
        
        elif category == "view" and key == "week_starts_on":
            if value.lower() not in DAYS_LONG and value.lower() not in DAYS_SHORT:
                raise ValueError(f"Invalid week start day: {value}")
        
        return self

class SettingCreate(SettingBase):
    pass

class SettingRead(SettingBase):
    model_config = {
        "from_attributes": True
    }
