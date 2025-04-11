import os
import shutil

import pytest

from app.db.utils.setup_db import setup_database, init_db
from app.config import APP_CFG

from tests.helpers import reload_config_module



@pytest.fixture()
def api_version():
    return "v1"


@pytest.fixture()
def api_prefix(api_version):
    return f"/api/{api_version}"


@pytest.fixture()
def empty_db(monkeypatch, tmp_path):
    db_file = tmp_path / "test_finances.db"

    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_file))
    init_db()

    yield db_file


@pytest.fixture()
def seeded_db(monkeypatch, tmp_path):
    db_file = tmp_path / "test_finances.db"
    test_seed_loc = "tests/unit/app/db/seed/test_sample.json"

    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_file))
    monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", test_seed_loc)

    setup_database()

    yield db_file


