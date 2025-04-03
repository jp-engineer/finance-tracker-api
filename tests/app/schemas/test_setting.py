import os
import pytest
from app.schemas.setting import SettingCreate
from app.schemas.enums import SettingCategoryEnum
from pydantic import ValidationError
from tests.helpers.read_test_json import load_test_json

CWD_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.unit
def test_valid_setting_create_schema():
    valid_setting_data = load_test_json(CWD_DIR, "valid_setting")
    setting = SettingCreate(**valid_setting_data)
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
