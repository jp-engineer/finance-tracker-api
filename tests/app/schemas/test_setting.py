import pytest
from app.schemas.setting import SettingCreate
from app.schemas.enums import SettingCategoryEnum
from pydantic import ValidationError

@pytest.mark.unit
def test_valid_setting_create_schema():
    data = {
        "key": "country_code",
        "value": "GB",
        "category": "general"
    }
    setting = SettingCreate(**data)
    assert setting.key == "country_code"
    assert setting.value == "GB"
    assert setting.category == SettingCategoryEnum.general

@pytest.mark.unit
def test_invalid_setting_category():
    data = {
        "key": "auto_save",
        "value": "true",
        "category": "invalid"
    }
    with pytest.raises(ValidationError):
        SettingCreate(**data)

@pytest.mark.unit
def test_missing_field_in_setting():
    data = {
        "value": "en",
        "category": "general"
    }
    with pytest.raises(ValidationError):
        SettingCreate(**data)
