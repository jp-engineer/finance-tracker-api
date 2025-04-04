import pytest
from pydantic import ValidationError
from app.schemas.setting import SettingCreate
from app.schemas.enums import SettingCategoryEnum

@pytest.mark.unit
@pytest.mark.db
@pytest.mark.models
class TestSettingClass:
    def test_setting_create_valid_data(self):
        setting = SettingCreate(
            key="currency",
            value="USD",
            category=SettingCategoryEnum.general
        )
        assert setting.key == "currency"
        assert setting.value == "USD"
        assert setting.category == SettingCategoryEnum.general

    def test_setting_create_invalid_enum(self):
        with pytest.raises(ValidationError):
            SettingCreate(
                key="currency",
                value="USD",
                category="not_a_valid_category"
            )
