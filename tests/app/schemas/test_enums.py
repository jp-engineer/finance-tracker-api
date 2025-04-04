import pytest
pytestmark = [
    pytest.mark.unit,
    pytest.mark.schemas
]
from app.schemas.enums import SettingCategoryEnum, FolioCategoryEnum

def test_setting_category_enum_members():
    assert SettingCategoryEnum.general.value == "general"
    assert SettingCategoryEnum.view.value == "view"
    assert SettingCategoryEnum.developer.value == "developer"
    assert len(SettingCategoryEnum) == 3

def test_folio_category_enum_values_are_strings():
    for enum_member in FolioCategoryEnum:
        assert isinstance(enum_member.value, str)

def test_folio_category_enum_sample_values():
    assert FolioCategoryEnum.shopping.value == "Shopping"
    assert FolioCategoryEnum.bills_utilities.value == "Bills & Utilities"
    assert FolioCategoryEnum.housing.value == "Housing"
    assert FolioCategoryEnum.transportation.value == "Transportation"
    assert FolioCategoryEnum.health_fitness.value == "Health & Fitness"
    assert FolioCategoryEnum.entertainment.value == "Entertainment"
    assert FolioCategoryEnum.food_drink.value == "Food & Drink"
    assert FolioCategoryEnum.education.value == "Education"
    assert FolioCategoryEnum.work_career.value == "Work & Career"
    assert FolioCategoryEnum.income.value == "Income"
    assert FolioCategoryEnum.financial_services.value == "Financial Services"
    assert FolioCategoryEnum.gifts_donations.value == "Gifts & Donations"
    assert FolioCategoryEnum.travel.value == "Travel"
    assert FolioCategoryEnum.pets.value == "Pets"
    assert FolioCategoryEnum.home_services.value == "Home Services"
    assert FolioCategoryEnum.government_tax.value == "Government & Tax"
    assert FolioCategoryEnum.insurance.value == "Insurance"
    assert FolioCategoryEnum.investments.value == "Investments"
