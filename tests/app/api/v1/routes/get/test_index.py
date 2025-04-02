import pytest
from tests.helpers.reload_config import reload_config_module_with_mode

@pytest.mark.api
def test_get_index_init_message(client, api_prefix):
    response = client.get(f"{api_prefix}/get-init-message")
    assert response.status_code == 200
    assert response.json() == {"message": "finance-tracker API is running"}

@pytest.mark.api
def test_get_index_app_config_contains_correct_keys(client, api_prefix):
    response = client.get(f"{api_prefix}/get-app-config")
    response_json = response.json()

    assert response.status_code == 200
    assert "API_VERSION" in response_json
    assert "MODE" in response_json
    assert "DB_PATH" in response_json
    assert "SEED_DIR" in response_json

@pytest.mark.api
def test_get_index_app_config_contains_valid_values(client, api_prefix):
    response = client.get(f"{api_prefix}/get-app-config")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["API_VERSION"][0] == "v"
    assert response_json["API_VERSION"][1:].isdigit()
    assert response_json["MODE"] == "test"
    assert response_json["DB_PATH"] == "tests\\app\\db\\test-finances.db"
    assert response_json["SEED_DIR"] == "tests\\app\\db\\seed"
