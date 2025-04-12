import pytest


pytestmark = [
    pytest.mark.api,
    pytest.mark.api_GET,
    pytest.mark.api_settings
]


@pytest.fixture
def api_prefix(api_prefix):
    return f"{api_prefix}/settings"


def test_get_all_settings(client, api_prefix):
    response = client.get(f"{api_prefix}/get-all-settings")
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] != None


def test_get_setting_by_key_and_category_from_db(client, api_prefix):
    category = "general"
    key = "default_currency"
    response = client.get(f"{api_prefix}/{category}/get-setting-by-key/{key}")
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] != None