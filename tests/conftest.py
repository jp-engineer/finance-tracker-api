import os
import gc
import pytest
from fastapi.testclient import TestClient
from main import app
from app.db.database import engine_context, init_db
from app.config import APP_CFG

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def api_prefix():
    return f"/api/v1"

@pytest.fixture(scope="class")
def setup_test_db_with_settings():
    db_path = APP_CFG["DB_PATH"]

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            pass

    with engine_context() as engine:
        init_db(engine=engine)
        yield engine

        gc.collect()
        engine.dispose()
        os.remove(db_path)
