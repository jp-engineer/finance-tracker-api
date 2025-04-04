import os
import pytest
from tests.helpers.reload_config import reload_config_module_with_mode

@pytest.mark.unit
def test_prod_mode_paths(monkeypatch):
    monkeypatch.setenv("MODE", "prod")
    config = reload_config_module_with_mode("prod")
    
    assert config.MODE == "prod"
    assert config.DB_FILENAME == "finances.db"
    assert config.DB_PATH == os.path.join("app", "db", "finances.db")
    assert config.SEED_DIR == os.path.join("app", "db", "seed")

@pytest.mark.unit
def test_dev_mode_paths(monkeypatch):
    monkeypatch.setenv("MODE", "dev")
    config = reload_config_module_with_mode("dev")

    assert config.MODE == "dev"
    assert config.DB_FILENAME == "dev-finances.db"
    assert config.DB_PATH == os.path.join("app", "db", "dev-finances.db")
    assert config.SEED_DIR == os.path.join("app", "db", "seed")

@pytest.mark.unit
def test_test_mode_paths(monkeypatch):
    monkeypatch.setenv("MODE", "test")
    config = reload_config_module_with_mode("test")

    assert config.MODE == "test"
    assert config.DB_FILENAME == "test-finances.db"
    assert config.DB_PATH == os.path.join("tests", "app", "db", "test-finances.db")
    assert config.SEED_DIR == os.path.join("tests", "app", "db", "seed")

@pytest.mark.unit
def test_e2e_testing_mode_paths(monkeypatch):
    monkeypatch.setenv("MODE", "e2e_testing")
    config = reload_config_module_with_mode("e2e_testing")

    assert config.MODE == "e2e_testing"
    assert config.DB_FILENAME == "test-finances.db"
    assert config.DB_PATH == os.path.join("tests", "app", "db", "test-finances.db")
    assert config.SEED_DIR == os.path.join("tests", "app", "db", "seed")

@pytest.mark.unit
def test_invalid_mode_exits(monkeypatch):
    monkeypatch.setenv("MODE", "invalid")

    with pytest.raises(SystemExit) as exc_info:
        reload_config_module_with_mode("invalid")
    
    assert exc_info.type == SystemExit
    assert str(exc_info.value) == "1"
    