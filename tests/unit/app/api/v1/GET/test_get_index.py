import pytest

pytestmark = [
    pytest.mark.api,
    pytest.mark.api_GET,
    pytest.mark.api_index
]

def test_get_index_init_message(client, api_prefix):
    response = client.get(f"{api_prefix}/")
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["message"] != None

def test_get_index_app_config(client, api_prefix):
    response = client.get(f"{api_prefix}/app/get-config")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["data"] != None

def test_get_index_db_config(client, api_prefix):
    response = client.get(f"{api_prefix}/db/get-config")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["data"] != None