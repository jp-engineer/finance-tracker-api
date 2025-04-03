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
        
        assert response.status_code == 200
        pass
