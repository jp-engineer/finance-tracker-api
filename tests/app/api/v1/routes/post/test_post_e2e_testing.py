import pytest
pytestmark = [
    pytest.mark.api,
    pytest.mark.api_e2e_testing
]

ROUTE = "/e2e-testing"

class TestAPIIndex:
    def test_post_init_blank_test_db(self, e2e_client, api_prefix):
        response = e2e_client.post(f"{api_prefix}{ROUTE}/db/post-init-db")
        
        assert response.status_code == 200

    def test_post_seed_db_settings_data(self, e2e_client, api_prefix):
        response = e2e_client.post(f"{api_prefix}{ROUTE}/db/post-seed-settings")
        
        assert response.status_code == 200
    
    def test_post_seed_db_all_data(self, e2e_client, api_prefix):
        response = e2e_client.post(f"{api_prefix}{ROUTE}/db/post-seed-data")
        
        assert response.status_code == 200
