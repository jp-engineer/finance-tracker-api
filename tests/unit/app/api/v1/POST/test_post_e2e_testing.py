import pytest

from tests.helpers import load_test_data_file


pytestmark = [
    pytest.mark.api,
    pytest.mark.api_POST,
    pytest.mark.api_e2e_testing,
]


@pytest.fixture
def api_prefix(api_prefix):
    return f"{api_prefix}/e2e-testing"


def test_post_init_blank_test_db(e2e_client, api_prefix):
    response = e2e_client.post(f"{api_prefix}/db/post-init-db")
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == True


def test_post_init_blank_test_db_invalid_mode(client, api_prefix):
    response = client.post(f"{api_prefix}/db/post-init-db")
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == False


def test_post_seed_db_settings_data(e2e_client, api_prefix):
    settings_dict = load_test_data_file("api", "test_seed_settings_data.json")
    response = e2e_client.post(f"{api_prefix}/db/post-seed-settings", json=settings_dict)

    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == True


def test_post_seed_db_settings_data_invalid_mode(client, api_prefix):
    settings_dict = load_test_data_file("api", "test_seed_settings_data.json")
    response = client.post(f"{api_prefix}/db/post-seed-settings", json=settings_dict)

    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == False


def test_post_seed_test_data(e2e_client_w_empty_db, api_prefix):
    settings_dict = load_test_data_file("api", "test_seed_test_data.json")
    response = e2e_client_w_empty_db.post(f"{api_prefix}/db/post-seed-test-data", json=settings_dict)

    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == True


def test_post_seed_test_data_invalid_mode(client, api_prefix):
    settings_dict = load_test_data_file("api", "test_seed_test_data.json")
    response = client.post(f"{api_prefix}/db/post-seed-test-data", json=settings_dict)

    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == False