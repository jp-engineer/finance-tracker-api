import os
import pytest
import yaml
from pathlib import Path
from app.utils.setup_templated_files import setup_templates
from tests.helpers.read_test_data import load_test_yaml

CWD_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(autouse=True)
def backup_prod_user_settings():
    prod_path = Path("app/user/user-settings.yml")
    backup_path = Path("app/user/user-settings.yml.bak")

    if os.path.exists(prod_path):
        prod_path.rename(backup_path)
        yield
        backup_path.rename(prod_path)
    else:
        yield
        if os.path.exists(backup_path):
            os.remove(backup_path)

@pytest.fixture
def temp_template_env(tmp_path):
    template_settings_dict = load_test_yaml(CWD_DIR, "template-user-settings")
    template_settings_str = yaml.dump(template_settings_dict)

    temp_templates_dir = tmp_path / "templates"
    temp_templates_dir.mkdir()

    template_file = temp_templates_dir / "user-settings.yml"
    template_file.write_text(template_settings_str)

    temp_user_settings_path = tmp_path / "user-settings.yml"

    return temp_user_settings_path, str(temp_templates_dir), template_settings_str.strip()

@pytest.fixture
def missing_template_env(tmp_path):
    empty_templates_dir = tmp_path / "templates"
    empty_templates_dir.mkdir()

    temp_user_settings_path = tmp_path / "user-settings.yml"

    return temp_user_settings_path, str(empty_templates_dir)

@pytest.mark.unit
@pytest.mark.templates
def test_setup_templates_creates_user_settings(temp_template_env):
    temp_user_settings_path, templates_dir, expected_content = temp_template_env

    assert not temp_user_settings_path.exists()

    setup_templates(str(temp_user_settings_path), templates_dir)

    assert temp_user_settings_path.exists()
    content = temp_user_settings_path.read_text().strip()
    assert content == expected_content

@pytest.mark.unit
@pytest.mark.templates
def test_setup_templates_raises_error_if_template_missing(missing_template_env):
    temp_user_settings_path, templates_dir = missing_template_env

    assert not temp_user_settings_path.exists()

    with pytest.raises(FileNotFoundError) as exc_info:
        setup_templates(str(temp_user_settings_path), templates_dir)

    assert "Template file" in str(exc_info.value)
