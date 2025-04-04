import pytest
import os
import importlib
from fastapi.testclient import TestClient
from helpers.reload_config import reload_config_module_with_mode

TEMPLATE_SETTINGS_PATH = "app/templates/user-settings.yml"
DEFAULTS_SETTINGS_PATH = "app/defaults/default-settings.yml"
TEST_USER_SETTINGS_PATH = "tests/app/user/test_user-settings.yml"

def import_app_and_cfg():
    from main import app
    from app.config import APP_CFG

    imported = {
        "app": app,
        "APP_CFG": APP_CFG
    }

    return imported

def teardown_test_db():

@pytest.fixture
def client_without_db():
    imported = import_app_and_cfg()
    with TestClient(imported['app']) as c:
        yield c

@pytest.fixture
def client_with_empty_db():
    imported = import_app_and_cfg()
    from app.db.database import init_db
    with TestClient(imported['app']) as c:
        init_db()
        yield c

@pytest.fixture
def client():
    imported = import_app_and_cfg()
    from app.db.database import init_db, seed_settings, load_db_config, get_engine
    from app.utils.setup_templated_files import setup_templates
    from app.utils.file_settings_functions import update_all_user_settings

    with TestClient(imported['app']) as c:
        setup_templates(TEMPLATE_SETTINGS_PATH, TEST_USER_SETTINGS_PATH)
        init_db()
        
        db_settings = load_db_config(DEFAULTS_SETTINGS_PATH, TEST_USER_SETTINGS_PATH)
        seed_settings(db_settings)
        update_all_user_settings(TEST_USER_SETTINGS_PATH, db_settings)

        yield c

        os.remove(TEST_USER_SETTINGS_PATH)
        engine = get_engine()
        engine.dispose()
        os.remove(imported['APP_CFG']["DB_PATH"])

@pytest.fixture()
def e2e_client():
    cfg_mod = reload_config_module_with_mode("e2e_testing")

    import main
    importlib.reload(main)

    from app.db.database import init_db, get_engine
    from app.utils.setup_templated_files import setup_templates

    TEMPLATE_SETTINGS_PATH = "app/templates/user-settings.yml"
    TEST_USER_SETTINGS_PATH = "tests/app/user/test_user-settings.yml"

    with TestClient(main.app) as c:
        setup_templates(TEMPLATE_SETTINGS_PATH, TEST_USER_SETTINGS_PATH)
        init_db()

        yield c

        os.remove(TEST_USER_SETTINGS_PATH)
        engine = get_engine()
        engine.dispose()
        os.remove(cfg_mod.APP_CFG["DB_PATH"])

@pytest.fixture(scope="module")
def api_prefix():
    return f"/api/v1"
