import os
from datetime import date
import pytest
from app.db.utils.get_db_functions import get_all_settings_from_db
from tests.helpers.read_test_data import load_test_json

CWD_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTE = "/settings"

@pytest.mark.api
@pytest.mark.api_settings
class TestAPIIndex:
    @pytest.fixture(autouse=True, scope="class")
    def _init_db(self, setup_test_db_with_settings):
        pass

    def test_put_all_settings(self, client, api_prefix):
        settings_data = load_test_json(CWD_DIR, "put_settings")
        settings_data["developer"]["start_date"] = date.today().strftime("%Y-%m-%d")
        response = client.put(f"{api_prefix}{ROUTE}/put-all-settings", json=settings_data)
        response_dict = response.json()

        assert response.status_code == 200

        db_settings = get_all_settings_from_db()
        assert db_settings["general"] == settings_data["general"]
        assert db_settings["developer"] == settings_data["developer"]
        assert db_settings["view"] == settings_data["view"]
