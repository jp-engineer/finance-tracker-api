import os
import pytest
from fastapi.testclient import TestClient
from app.config import APP_CFG
from main import app
from app.db.database import engine_context, init_db, seed_settings

USER_SETTINGS_FILE = "app/user/user-settings.yml"

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def api_prefix():
    return f"/api/v1"

@pytest.fixture(scope="class")
def setup_test_db_with_settings():
    if os.path.exists(USER_SETTINGS_FILE):
        os.rename(USER_SETTINGS_FILE, USER_SETTINGS_FILE + ".prod.bak")

    db_path = APP_CFG["DB_PATH"]

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            pass

    with engine_context() as engine:
        init_db(engine=engine)
        seed_settings(engine=engine)
        yield engine

        if os.path.exists(USER_SETTINGS_FILE + ".prod.bak"):
            os.rename(USER_SETTINGS_FILE + ".prod.bak", USER_SETTINGS_FILE)

        engine.dispose()
        os.remove(db_path)
