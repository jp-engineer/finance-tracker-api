import pytest
from app.config import APP_CFG
from main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def api_prefix():
    return f"/api/{APP_CFG['API_VERSION']}"

# import os

# from app.db.database import engine_context, init_db, seed_settings



# @pytest.fixture(scope="class")
# def setup_test_db_with_settings():
#     db_path = APP_CFG["DB_PATH"]

#     if os.path.exists(db_path):
#         try:
#             os.remove(db_path)
#         except PermissionError:
#             pass

#     with engine_context() as engine:
#         init_db(engine=engine)
#         seed_settings(engine=engine)
#         yield engine

#         engine.dispose()
#         os.remove(db_path)
