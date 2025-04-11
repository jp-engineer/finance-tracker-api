import pytest

from tests.helpers import load_test_data_file


pytestmark = [
    pytest.mark.api,
    pytest.mark.api_PUT,
    pytest.mark.api_settings,
]


@pytest.fixture
def api_prefix(api_prefix):
    return f"{api_prefix}/settings"


def test_put_all_settings(client, api_prefix):
    all_settings_dict = load_test_data_file("api", "test_put_all_settings.json")
    response = client.put(f"{api_prefix}/put-all-settings", json=all_settings_dict)
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == True


def test_put_general_setting(client, api_prefix):
    general_settings_dict = {
        "key": "default_currency",
        "value": "usd"
        }
    response = client.put(f"{api_prefix}/general/put-setting", json=general_settings_dict)
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] != {}


def test_put_developer_setting(client, api_prefix):
    developer_settings_dict = {
        "key": "start_date",
        "value": "2025-04-10"
        }
    response = client.put(f"{api_prefix}/developer/put-setting", json=developer_settings_dict)
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] != {}


def test_put_viewer_setting(client, api_prefix):
    viewer_settings_dict = {
        "key": "user_name",
        "value": "Testy Mc Test Face"
        }
    response = client.put(f"{api_prefix}/view/put-setting", json=viewer_settings_dict)
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] != {}