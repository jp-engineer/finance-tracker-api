import pytest

@pytest.mark.api
@pytest.mark.api_index
class TestAPIIndex:
    @pytest.fixture(autouse=True, scope="class")
    def _init_db(self, setup_test_db_with_settings):
        pass

    def test_get_index_init_message(self, client, api_prefix):
        response = client.get(f"{api_prefix}/get-init-message")
        
        assert response.status_code == 200
        assert response.json() == {"message": "finance-tracker API is running"}

    def test_get_index_app_config_items(self, client, api_prefix):
        response = client.get(f"{api_prefix}/get-app-config")
        response_dict = response.json()

        assert response.status_code == 200
        assert response_dict["API_VERSION"][0] == "v"
        assert response_dict["API_VERSION"][1:].isdigit()
        assert response_dict["MODE"] == "test"
        assert response_dict["DB_PATH"] == "tests\\app\\db\\test-finances.db"
        assert response_dict["SEED_DIR"] == "tests\\app\\db\\seed"

    def test_get_index_db_config(self, client, api_prefix):
        response = client.get(f"{api_prefix}/get-db-config")
        response_dict = response.json()

        assert response.status_code == 200
        assert response_dict["DB_PATH"] == "tests\\app\\db\\test-finances.db"
        assert response_dict["EXISTS"] == True
        assert response_dict["HAS_TABLES"] == True
        assert response_dict["TABLES"] == ["settings"]
        assert response_dict["TABLES_COUNT"] == 1
        assert response_dict["HAS_DATA"] == True

@pytest.mark.api
@pytest.mark.api_index
def test_get_index_db_config_with_no_db(client, api_prefix):
    response = client.get(f"{api_prefix}/get-db-config")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["EXISTS"] is False
    assert response_dict["HAS_TABLES"] is False
    assert response_dict["HAS_DATA"] is False
    assert response_dict["TABLES"] == []
    assert response_dict["TABLES_COUNT"] == 0
