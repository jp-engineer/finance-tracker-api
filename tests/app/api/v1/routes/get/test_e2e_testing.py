import pytest
pytestmark = [
    pytest.mark.api,
    pytest.mark.api_e2e_testing
]

ROUTE = "/e2e-testing"

class TestAPIIndex:
    def test_get_e2e_mode_check(self, e2e_client, api_prefix):
        response = e2e_client.get(f"{api_prefix}{ROUTE}/get-e2e-mode-check")
        
        assert response.status_code == 200
