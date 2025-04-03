import pytest
from app.db.utils.get_db_functions import get_all_settings_from_db

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
