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
