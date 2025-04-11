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
    
    assert response_dict["success"] == True
    assert response_dict["message"] != None


def test_post_seed_db_settings_data(client, api_prefix):
    settings_dict = load_test_data_file("api/test_seed_settings_data.json")
    response = client.post(f"{api_prefix}/db/post-seed-settings", json=settings_dict)

    response_dict = response.json()
    
    assert response_dict["success"] == True


def test_post_seed_test_data(client, api_prefix):
    settings_dict = load_test_data_file("api/test_seed_test_data.json")
    response = client.post(f"{api_prefix}/db/post-seed-test-data", json=settings_dict)

    response_dict = response.json()
    
    assert response_dict["success"] == True