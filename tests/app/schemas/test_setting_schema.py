import pytest
pytestmark = [
    pytest.mark.unit,
    pytest.mark.schema
]

from pydantic import ValidationError
from app.schemas.setting import SettingCreate
from app.schemas.enums import SettingCategoryEnum

class TestSettingBase:
    def test_validate_combination_valid_country_code(self):
        setting = SettingCreate(
            key="country_code",
            value="GB",
            category=SettingCategoryEnum.general
        )
        assert setting.value == "GB"

    def test_validate_combination_invalid_country_code(self):
        with pytest.raises(ValidationError, match="Invalid country code: XX"):
            SettingCreate(
                key="country_code",
                value="XX",
                category=SettingCategoryEnum.general
            )

    def test_validate_combination_valid_currency_code(self):
        setting = SettingCreate(
            key="default_currency",
            value="USD",
            category=SettingCategoryEnum.view
        )
        assert setting.value == "USD"

    def test_validate_combination_invalid_currency_code(self):
        with pytest.raises(ValidationError, match="Invalid currency code: FAKE"):
            SettingCreate(
                key="default_currency",
                value="FAKE",
                category=SettingCategoryEnum.view
            )

    def test_validate_combination_valid_date_format(self):
        setting = SettingCreate(
            key="date_format",
            value="yyyy-mm-dd",
            category=SettingCategoryEnum.view
        )
        assert setting.value == "yyyy-mm-dd"

    def test_validate_combination_invalid_date_format(self):
        with pytest.raises(ValidationError, match="Invalid date format: 04/04/2025"):
            SettingCreate(
                key="date_format",
                value="04/04/2025",
                category=SettingCategoryEnum.view
            )

    def test_validate_combination_validate_combination_valid_week_start_day(self):
        setting = SettingCreate(
            key="week_starts_on",
            value="monday",
            category=SettingCategoryEnum.view
        )
        assert setting.value == "monday"

    def test_validate_combination_invalid_week_start_day(self):
        with pytest.raises(ValidationError, match="Invalid week start day: funday"):
            SettingCreate(
                key="week_starts_on",
                value="funday",
                category=SettingCategoryEnum.view
            )

    def test_validate_combination_valid_enum_category(self):
        setting = SettingCreate(
            key="currency",
            value="USD",
            category=SettingCategoryEnum.general
        )
        assert setting.category == SettingCategoryEnum.general

    def test_validate_combination_invalid_enum_category(self):
        with pytest.raises(ValidationError):
            SettingCreate(
                key="currency",
                value="USD",
                category="not_a_valid_category"
            )
