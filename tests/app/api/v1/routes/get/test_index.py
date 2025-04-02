import pytest

@pytest.mark.api
def test_get_index_init_message(client, api_prefix):
    response = client.get(f"{api_prefix}/get-init-message")
    assert response.status_code == 200
    assert response.json() == {"message": "finance-tracker API is running"}
