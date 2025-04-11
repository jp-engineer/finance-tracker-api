import os
import json

import pytest

from tests.helpers import reload_config_module

from app.config import APP_CFG
from app.config import validate_file


def test_validate_file_with_valid_json_file_provided(tmp_path):
    valid_json_file = tmp_path / "valid.json"
    valid_file_path_str = str(valid_json_file)
    valid_json_file.write_text('{"key": "value"}')

    result = validate_file(valid_file_path_str, "json")
    
    assert result == str(valid_json_file)
    

def test_validate_file_with_valid_json_file_found(tmp_path):
    valid_json_file = tmp_path / "valid.json"
    valid_file_path_str = str(valid_json_file)[:-5]
    valid_json_file.write_text('{"key": "value"}')

    result = validate_file(valid_file_path_str, "json")
    
    assert result == valid_file_path_str + ".json"


def test_validate_file_with_valid_yaml_file_provided(tmp_path):
    valid_yaml_file = tmp_path / "valid.yaml"
    valid_file_path_str = str(valid_yaml_file)
    valid_yaml_file.write_text("key: value")

    result = validate_file(valid_file_path_str, "yaml")
    
    assert result == str(valid_yaml_file)


def test_validate_file_with_valid_yaml_file_found(tmp_path):
    valid_yaml_file = tmp_path / "valid.yml"
    valid_file_path_str = str(valid_yaml_file)[:-4]
    valid_yaml_file.write_text("key: value")

    result = validate_file(valid_file_path_str, "yaml")
    
    assert result == valid_file_path_str + ".yml"


def test_validate_file_with_invalid_file_provided(tmp_path):
    invalid_file = tmp_path / "invalid.txt"
    invalid_file.write_text("This is not a valid file type.")

    result = validate_file(str(invalid_file), "json")
    
    assert result is None


def test_api_version(api_version):
    assert APP_CFG["API_VERSION"] == api_version


def test_mode_in_prod():
    assert APP_CFG["MODE"] == "prod"


def test_mode_in_dev(monkeypatch):
    monkeypatch.setenv("MODE", "dev")
    config = reload_config_module()
    
    assert config.APP_CFG["MODE"] == "dev"


def test_mode_in_e2e_testing(monkeypatch):
    monkeypatch.setenv("MODE", "e2e_testing")
    config = reload_config_module()
    
    assert config.APP_CFG["MODE"] == "e2e_testing"


def test_mode_with_invalid_value(monkeypatch):
    monkeypatch.setenv("MODE", "invalid_mode")

    with pytest.raises(SystemExit):
        config = reload_config_module()


def test_db_path_in_prod():
    assert APP_CFG["DB_PATH"] == os.path.join("app", "db", "finances.db")


def test_db_path_in_dev(monkeypatch):
    monkeypatch.setenv("MODE", "dev")
    config = reload_config_module()
    
    assert config.APP_CFG["DB_PATH"] == os.path.join("app", "db", "dev-finances.db")


def test_db_path_in_e2e_testing(monkeypatch):
    monkeypatch.setenv("MODE", "e2e_testing")
    config = reload_config_module()
    
    assert config.APP_CFG["DB_PATH"] == os.path.join("tests", "data", "e2e", "db", "test-finances.db")


def test_db_seed_file_in_prod_when_provided(monkeypatch, tmp_path):
    seed_dir = tmp_path / "app" / "db" / "seed"
    seed_dir.mkdir(parents=True)
    seed_file = seed_dir / "custom_seed.json"
    seed_file.write_text(json.dumps({"Setting": []}))

    monkeypatch.setenv("DB_SEED_FILE", str(seed_file))
    monkeypatch.chdir(tmp_path)

    config = reload_config_module()

    assert config.APP_CFG["DB_SEED_FILE"].endswith("custom_seed.json")
    assert os.path.exists(config.APP_CFG["DB_SEED_FILE"])


def test_db_seed_file_in_prod_when_not_provided(monkeypatch, tmp_path):
    monkeypatch.delenv("DB_SEED_FILE", raising=False)
    monkeypatch.setenv("MODE", "prod")

    seed_dir = tmp_path / "app" / "db" / "seed"
    seed_dir.mkdir(parents=True)

    monkeypatch.chdir(tmp_path)

    config = reload_config_module()

    assert config.APP_CFG["DB_SEED_FILE"] is None


def test_db_seed_file_in_dev_when_provided(monkeypatch, tmp_path):
    monkeypatch.setenv("MODE", "dev")

    seed_dir = tmp_path / "app" / "db" / "seed"
    seed_dir.mkdir(parents=True)
    seed_file = seed_dir / "custom_seed.json"
    seed_file.write_text(json.dumps({"Setting": []}))

    monkeypatch.setenv("DB_SEED_FILE", seed_file.name)
    monkeypatch.chdir(tmp_path)

    config = reload_config_module()

    assert config.APP_CFG["DB_SEED_FILE"].endswith("custom_seed.json")
    assert os.path.exists(config.APP_CFG["DB_SEED_FILE"])


def test_db_seed_file_in_dev_when_not_provided_loads_dev_seed_if_exists(monkeypatch, tmp_path):
    monkeypatch.setenv("MODE", "dev")

    seed_dir = tmp_path / "app" / "db" / "seed"
    seed_dir.mkdir(parents=True)
    dev_seed_file = seed_dir / "dev_seed.json"
    dev_seed_file.write_text(json.dumps({"Setting": []}))

    monkeypatch.chdir(tmp_path)

    config = reload_config_module()

    assert config.APP_CFG["DB_SEED_FILE"].endswith("dev_seed.json")
    assert os.path.exists(config.APP_CFG["DB_SEED_FILE"])


def test_db_seed_file_in_e2e_when_provided(monkeypatch, tmp_path):
    monkeypatch.setenv("MODE", "e2e_testing")

    seed_dir = tmp_path / "tests" / "e2e" / "app" / "db" / "seed"
    seed_dir.mkdir(parents=True)
    seed_file = seed_dir / "custom_seed.json"
    seed_file.write_text(json.dumps({"Setting": []}))

    monkeypatch.setenv("DB_SEED_FILE", str(seed_file))
    monkeypatch.chdir(tmp_path)

    config = reload_config_module()

    assert config.APP_CFG["DB_SEED_FILE"].endswith("custom_seed.json")
    assert os.path.exists(config.APP_CFG["DB_SEED_FILE"])


def test_db_seed_file_in_e2e_when_not_provided_loads_test_seed(monkeypatch):
    monkeypatch.setenv("MODE", "e2e_testing")
    config = reload_config_module()

    assert config.APP_CFG["DB_SEED_FILE"].endswith("test_seed.json")
    assert os.path.exists(config.APP_CFG["DB_SEED_FILE"])


def test_settings_file_in_prod_when_provided(monkeypatch, tmp_path):
    settings_dir = tmp_path / "app" / "user"
    settings_dir.mkdir(parents=True)
    settings_file = settings_dir / "custom.yml"
    settings_file.write_text("view:\n  theme: dark")

    monkeypatch.setenv("SETTINGS_FILE", str(settings_file))
    monkeypatch.chdir(tmp_path)

    config = reload_config_module()

    assert config.APP_CFG["SETTINGS_FILE"].endswith("custom.yml")
    assert os.path.exists(config.APP_CFG["SETTINGS_FILE"])


def test_settings_file_in_prod_when_not_provided(monkeypatch, tmp_path):
    monkeypatch.delenv("SETTINGS_FILE", raising=False)
    monkeypatch.setenv("MODE", "prod")

    monkeypatch.chdir(tmp_path)
    config = reload_config_module()

    assert config.APP_CFG["SETTINGS_FILE"] == os.path.join("app", "user", "user_settings.yml")


def test_settings_file_in_dev_when_provided(monkeypatch, tmp_path):
    monkeypatch.setenv("MODE", "dev")

    settings_dir = tmp_path / "app" / "user"
    settings_dir.mkdir(parents=True)
    settings_file = settings_dir / "custom.yml"
    settings_file.write_text("view:\n  theme: dark")

    monkeypatch.setenv("SETTINGS_FILE", str(settings_file))
    monkeypatch.chdir(tmp_path)

    config = reload_config_module()

    assert config.APP_CFG["SETTINGS_FILE"].endswith("custom.yml")
    assert os.path.exists(config.APP_CFG["SETTINGS_FILE"])


def test_settings_file_in_dev_when_not_provided(monkeypatch, tmp_path):
    monkeypatch.setenv("MODE", "dev")

    user_dir = tmp_path / "app" / "user"
    user_dir.mkdir(parents=True)
    default_file = user_dir / "dev_user_settings.yml"
    default_file.write_text("general:\n  currency: EUR")

    monkeypatch.chdir(tmp_path)

    config = reload_config_module()

    assert config.APP_CFG["SETTINGS_FILE"].endswith("dev_user_settings.yml")
    assert os.path.exists(config.APP_CFG["SETTINGS_FILE"])


def test_templates_settings_dir():
    assert APP_CFG["TEMPLATE_SETTINGS_DIR"] == os.path.join("app", "templates")


def test_default_settings_dir():
    assert APP_CFG["DEFAULT_SETTINGS_DIR"] == os.path.join("app", "defaults")