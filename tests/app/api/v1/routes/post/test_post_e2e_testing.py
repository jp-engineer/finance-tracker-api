import pytest
pytestmark = [
    pytest.mark.api,
    pytest.mark.api_e2e_testing
]

from app.db.utils.get_db_functions import get_all_settings_from_db
from tests.helpers.read_test_data import check_test_db_path_exists, load_test_data_file

ROUTE = "/e2e-testing"

class TestAPIIndex:
    def test_post_init_blank_test_db(self, e2e_client, api_prefix):
        response = e2e_client.post(f"{api_prefix}{ROUTE}/db/post-init-db")
        db_exists = check_test_db_path_exists()

        assert response.status_code == 200
        assert db_exists is True

    def test_post_seed_db_settings_data(self, e2e_client, api_prefix):
        post_settings = load_test_data_file("test_post_e2e_testing_settings_data.json")
        response = e2e_client.post(f"{api_prefix}{ROUTE}/db/post-seed-settings", json=post_settings)
        
        seeded_settings = get_all_settings_from_db()
        assert response.status_code == 200
        assert seeded_settings == post_settings

    def test_post_seed_db_all_data(self, e2e_client, api_prefix):
        post_settings = load_test_data_file("test_post_e2e_testing_all_data.json")
        response = e2e_client.post(f"{api_prefix}{ROUTE}/db/post-seed-data", json=post_settings)        
        assert response.status_code == 200
