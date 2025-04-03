import pytest

route_prefix = "/settings"

@pytest.mark.api
@pytest.mark.api_settings
class TestAPIIndex:
    @pytest.fixture(autouse=True, scope="class")
    def _init_db(self, setup_test_db_with_settings):
        pass

    def test_get_all_settings(self, client, api_prefix):
        response = client.get(f"{api_prefix}{route_prefix}/get-all-settings")
        response_json = response.json()

        assert response.status_code == 200

        assert "general" in response_json
        assert "country_code" in response_json["general"]

        assert "view" in response_json
        assert "user_name" in response_json["view"]
        assert "week_starts_on" in response_json["view"]
        assert "date_format" in response_json["view"]
        assert "default_currency" in response_json["view"]
        assert "default_currency_symbol" in response_json["view"]
        
        assert "developer" in response_json
        assert "start_date" in response_json["developer"]

    def test_get_setting_by_category_and_key(self, client, api_prefix):
        response = client.get(f"{api_prefix}{route_prefix}/get-setting-by-category-and-key/general/country_code")
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["key"] == "country_code"
        assert response_json["category"] == "general"
        assert response_json["value"] == "gb"
