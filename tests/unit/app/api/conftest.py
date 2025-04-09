import pytest
from fastapi.testclient import TestClient
from main import app
from app.config import APP_CFG

# from app.config import APP_CFG
# from app.db.utils.setup_db import setup_database
# from tests.helpers import reload_main_module

@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))
    with TestClient(app) as c:
        yield c

# @pytest.fixture()
# def client_w_test_db(tmp_path, monkeypatch):
#     db_path = tmp_path / "test_seeded.db"
#     db_seed_path = "tests/data/app/test_fixture_db_valid_data.json"
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))
#     monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", db_seed_path)

#     setup_database()
#     with TestClient(app) as c:
#         yield c

# @pytest.fixture()
# def client_w_empty_e2e_db(tmp_path, monkeypatch):
#     db_path = tmp_path / "test_e2e_blank.db"
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))
#     monkeypatch.setitem(APP_CFG, "MODE", "e2e_testing")

#     reload_main_module()
#     from main import app
#     with TestClient(app) as c:
#         yield c
