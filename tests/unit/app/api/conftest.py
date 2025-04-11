import os
import pytest
from fastapi.testclient import TestClient
from main import app
from app.db.utils.setup_db import setup_database, init_db
from app.config import APP_CFG
from tests.helpers import reload_config_module

# from app.config import APP_CFG
# from app.db.utils.setup_db import setup_database
# from tests.helpers import reload_main_module

@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    test_seed_file = os.path.join("tests", "unit", "app", "db", "seed", "test_sample.json")

    monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", test_seed_file)
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    setup_database()

    with TestClient(app) as c:
        yield c

@pytest.fixture()
def e2e_client(monkeypatch):
    test_seed_file = os.path.join("tests", "data", "e2e", "db", "seed", "test_seed.json")

    monkeypatch.setitem(APP_CFG, "MODE", "e2e_testing")
    monkeypatch.setitem(APP_CFG, "DB_PATH", os.path.join("tests", "data", "e2e", "db", "test-finances.db"))
    monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", test_seed_file)
    monkeypatch.setitem(APP_CFG, "DELETE_DB", "true")

    setup_database()

    with TestClient(app) as c:
        yield c

@pytest.fixture()
def e2e_client_w_empty_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test-temp-finances.db"

    monkeypatch.setitem(APP_CFG, "MODE", "e2e_testing")
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    init_db()

    with TestClient(app) as c:
        yield c