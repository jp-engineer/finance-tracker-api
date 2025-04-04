from datetime import date
import pytest
from app.db.utils.get_db_functions import get_all_settings_from_db, get_setting_from_db

USER_SETTINGS_FILE = "app/user/user-settings.yml"

@pytest.mark.unit
@pytest.mark.db
class TestGetDBFunctions:
    @pytest.fixture(autouse=True, scope="class")
    def _setup_db(self, setup_test_db_with_settings):
        pass

    def test_get_all_settings_from_db(self):
        settings = get_all_settings_from_db()

        assert isinstance(settings, dict)
        assert "general" in settings
        assert "developer" in settings
        assert "view" in settings

        assert "country_code" in settings["general"]

        assert "user_name" in settings["view"]
        assert "week_starts_on" in settings["view"]
        assert "date_format" in settings["view"]
        assert "default_currency" in settings["view"]
        assert "default_currency_symbol" in settings["view"]

        assert "start_date" in settings["developer"]

    def test_get_setting_from_db(self):
        setting = get_setting_from_db("general", "country_code")
        today = date.today().strftime("%Y-%m-%d")

        assert isinstance(setting, dict)
        assert setting["key"] == "country_code"
        assert setting["category"] == "general"
        assert setting["value"] == "gb"

        setting = get_setting_from_db("view", "user_name")
        assert setting is not None
        assert setting["key"] == "user_name"
        assert setting["category"] == "view"
        assert setting["value"] == "pal"

        setting = get_setting_from_db("developer", "start_date")
        assert setting is not None
        assert setting["key"] == "start_date"
        assert setting["category"] == "developer"
        assert setting["value"] == today

    def test_get_setting_from_db_invalid(self):
        setting = get_setting_from_db("general", "invalid_key")
        assert setting is None

        setting = get_setting_from_db("invalid_category", "country_code")
        assert setting is None
