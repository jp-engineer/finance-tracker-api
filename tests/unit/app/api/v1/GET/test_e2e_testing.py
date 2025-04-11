import pytest

pytestmark = [
    pytest.mark.api,
    pytest.mark.api_GET,
    pytest.mark.api_e2e_testing,
]


@pytest.fixture
def api_prefix(api_prefix):
    return f"{api_prefix}/e2e-testing"


def test_get_e2e_mode_check(e2e_client, api_prefix):
    response = e2e_client.get(f"{api_prefix}/")
    response_dict = response.json()
    
    assert response_dict["success"] == True
    assert response_dict["data"] != None