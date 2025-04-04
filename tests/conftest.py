import os
import pytest
from fastapi.testclient import TestClient
from main import app
from app.config import APP_CFG
from app.db.database import init_db, seed_settings, load_db_config
from app.utils.setup_templated_files import setup_templates
from app.utils.file_settings_functions import update_all_user_settings

TEMPLATE_SETTINGS_PATH = "app/templates/user-settings.yml"
DEFAULTS_SETTINGS_PATH = "app/defaults/default-settings.yml"
TEST_USER_SETTINGS_PATH = "tests/app/user/test_user-settings.yml"

@pytest.fixture
def client_without_db():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def client_with_empty_db():
    with TestClient(app) as c:
        init_db()
        yield c

@pytest.fixture
def client():
    with TestClient(app) as c:
        setup_templates(TEMPLATE_SETTINGS_PATH, TEST_USER_SETTINGS_PATH)
        init_db()
        db_settings = load_db_config(DEFAULTS_SETTINGS_PATH, TEST_USER_SETTINGS_PATH)
        seed_settings(db_settings)
        update_all_user_settings(TEST_USER_SETTINGS_PATH, db_settings)
        yield c

        os.remove(TEST_USER_SETTINGS_PATH)

@pytest.fixture(scope="module")
def api_prefix():
    return f"/api/{APP_CFG['API_VERSION']}"

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
