import os
from datetime import date
import pytest
from tests.helpers.read_test_data import load_test_json

CWD_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTE = "/settings"

@pytest.mark.api
@pytest.mark.api_settings
class TestAPIIndex:
    @pytest.fixture(autouse=True, scope="function")
    def _init_db(self, setup_test_db_with_settings):
        pass

    def test_get_all_settings(self, client, api_prefix):
        settings_data = load_test_json(CWD_DIR, "put_settings")
        settings_data["developer"]["start_date"] = date.today().strftime("%Y-%m-%d")
        response = client.put(f"{api_prefix}{ROUTE}/put-all-settings")
        response_dict = response.json()

        assert response.status_code == 200
        assert len(response_dict) == len(settings_data)
        assert response_dict["general"] == settings_data["general"]
        assert response_dict["developer"] == settings_data["developer"]
        assert response_dict["view"] == settings_data["view"]
