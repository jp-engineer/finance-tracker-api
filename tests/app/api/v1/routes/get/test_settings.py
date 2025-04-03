import os
from datetime import date
import pytest
from tests.helpers.read_test_data import load_test_json

CWD_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTE = "/settings"

@pytest.mark.api
@pytest.mark.api_settings
class TestAPIIndex:
    @pytest.fixture(autouse=True, scope="class")
    def _init_db(self, setup_test_db_with_settings):
        pass

    def test_get_all_settings(self, client, api_prefix):
        settings_data = load_test_json(CWD_DIR, "all_settings")
        settings_data["developer"]["start_date"] = date.today().strftime("%Y-%m-%d")
        response = client.get(f"{api_prefix}{ROUTE}/get-all-settings")
        response_dict = response.json()

        assert response.status_code == 200
        assert len(response_dict) == len(settings_data)
        assert response_dict["general"] == settings_data["general"]
        assert response_dict["developer"] == settings_data["developer"]
        assert response_dict["view"] == settings_data["view"]


    def test_get_setting_by_category_and_key(self, client, api_prefix):
        response = client.get(f"{api_prefix}{ROUTE}/get-setting-by-category-and-key/general/country_code")
        response_dict = response.json()

        assert response.status_code == 200
        assert response_dict["key"] == "country_code"
        assert response_dict["category"] == "general"
        assert response_dict["value"] == "gb"
