import os
import pytest
from pydantic import ValidationError
from app.schemas.folio import FolioCreate
from tests.helpers.read_test_data import load_test_json

CWD_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.unit
@pytest.mark.schema
class TestFolioBase:
    def test_valid_combination_valid(self):
        valid_folio_data = load_test_json(CWD_DIR, "valid_folio")
        folio = FolioCreate(**valid_folio_data)

        assert folio.name == valid_folio_data["name"]
        assert folio.category == valid_folio_data["category"]
        assert folio.subcategory == valid_folio_data["subcategory"]

    def test_valid_combination_empty_name(self):
        data = load_test_json(CWD_DIR, "valid_folio")
        data["name"] = ""

        with pytest.raises(ValueError, match="Name cannot be empty"):
            FolioCreate(**data)

    def test_valid_combination_name_too_long(self):
        data = load_test_json(CWD_DIR, "valid_folio")
        data["name"] = "x" * 51

        with pytest.raises(ValueError, match="Name cannot exceed 50 characters"):
            FolioCreate(**data)

    def test_valid_combination_empty_category(self):
        data = load_test_json(CWD_DIR, "valid_folio")
        data["category"] = ""

        with pytest.raises(ValidationError) as exc_info:
            FolioCreate(**data)

        assert "Input should be" in str(exc_info.value)
        assert "input_value=''" in str(exc_info.value)

    def test_valid_combination_invalid_category(self):
        data = load_test_json(CWD_DIR, "valid_folio")
        data["category"] = "invalid_category"

        with pytest.raises(ValidationError) as exc_info:
            FolioCreate(**data)

        assert "Input should be" in str(exc_info.value)
        assert "input_value='invalid_category'" in str(exc_info.value)

    def test_valid_combination_subcategory_too_long(self):
        data = load_test_json(CWD_DIR, "valid_folio")
        data["subcategory"] = "x" * 51

        with pytest.raises(ValueError, match="Subcategory cannot exceed 50 characters"):
            FolioCreate(**data)
    

# import os
# import pytest
# from app.schemas.setting import SettingCreate
# from pydantic import ValidationError
# from tests.helpers.read_test_data import load_test_json

# CWD_DIR = os.path.dirname(os.path.abspath(__file__))

# @pytest.mark.unit
# @pytest.mark.schema
# def test_valid_setting_create_schema():
#     valid_setting_data = load_test_json(CWD_DIR, "valid_setting")
#     valid_key = valid_setting_data.get("key")
#     valid_value = valid_setting_data.get("value")
#     valid_category = valid_setting_data.get("category")

#     setting = SettingCreate(**valid_setting_data)
    
#     assert setting.key == valid_key
#     assert setting.value == valid_value
#     assert setting.category == valid_category

# @pytest.mark.unit
# @pytest.mark.schema
# def test_invalid_setting_category():
#     valid_setting_data = load_test_json(CWD_DIR, "valid_setting")

#     valid_key = valid_setting_data.get("key")
#     valid_value = valid_setting_data.get("value")
#     invalid_category = "invalid_category"
#     data = {"key": valid_key, "value": valid_value, "category": invalid_category}

#     with pytest.raises(ValidationError):
#         SettingCreate(**data)

# @pytest.mark.unit
# @pytest.mark.schema
# def test_missing_field_in_setting():
#     valid_setting_data = load_test_json(CWD_DIR, "valid_setting")
#     del valid_setting_data["key"]

#     with pytest.raises(ValidationError):
#         SettingCreate(**valid_setting_data)
