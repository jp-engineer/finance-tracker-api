import pytest


pytestmark = [
    pytest.mark.api,
    pytest.mark.api_DELETE,
    pytest.mark.api_e2e_testing,
]


@pytest.fixture
def api_prefix(api_prefix):
    return f"{api_prefix}/e2e-testing"


def test_delete_test_db(e2e_client, api_prefix):
    response = e2e_client.delete(f"{api_prefix}/db/delete-test-db")
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == True

def test_delete_test_db_invalid_mode(client, api_prefix):
    response = client.delete(f"{api_prefix}/db/delete-test-db")
    response_dict = response.json()
    
    assert response.status_code == 200
    assert response_dict["data"] == False