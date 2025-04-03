import os
import pytest
from app.schemas.setting import SettingCreate
from pydantic import ValidationError
from tests.helpers.read_test_data import load_test_json

CWD_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.unit
@pytest.mark.schema
def test_valid_setting_create_schema():
    valid_setting_data = load_test_json(CWD_DIR, "valid_setting")
    valid_key = valid_setting_data.get("key")
    valid_value = valid_setting_data.get("value")
    valid_category = valid_setting_data.get("category")

    setting = SettingCreate(**valid_setting_data)
    
    assert setting.key == valid_key
    assert setting.value == valid_value
    assert setting.category == valid_category

@pytest.mark.unit
@pytest.mark.schema
def test_invalid_setting_category():
    valid_setting_data = load_test_json(CWD_DIR, "valid_setting")

    valid_key = valid_setting_data.get("key")
    valid_value = valid_setting_data.get("value")
    invalid_category = "invalid_category"
    data = {"key": valid_key, "value": valid_value, "category": invalid_category}

    with pytest.raises(ValidationError):
        SettingCreate(**data)

@pytest.mark.unit
@pytest.mark.schema
def test_missing_field_in_setting():
    valid_setting_data = load_test_json(CWD_DIR, "valid_setting")
    del valid_setting_data["key"]

    with pytest.raises(ValidationError):
        SettingCreate(**valid_setting_data)
