import pytest
pytestmark = [
    pytest.mark.unit,
    pytest.mark.utils
]
import os

from app.utils.setup_templated_files import setup_templates

def test_setup_templates_creates_user_file(tmp_path):
    template_file = tmp_path / "template-settings.yml"
    user_file = tmp_path / "user-settings.yml"

    template_file.write_text("general:\n  currency: USD\n")

    assert not user_file.exists()

    setup_templates(str(template_file), str(user_file))

    assert user_file.exists()
    assert user_file.read_text() == "general:\n  currency: USD\n"


def test_setup_templates_does_not_overwrite_existing_user_file(tmp_path):
    template_file = tmp_path / "template-settings.yml"
    user_file = tmp_path / "user-settings.yml"

    template_file.write_text("general:\n  currency: USD\n")
    user_file.write_text("general:\n  currency: GBP\n")

    setup_templates(str(template_file), str(user_file))

    assert user_file.read_text() == "general:\n  currency: GBP\n"


def test_setup_templates_raises_if_template_missing(tmp_path):
    template_file = tmp_path / "missing-template.yml"
    user_file = tmp_path / "user-settings.yml"

    assert not template_file.exists()

    with pytest.raises(FileNotFoundError) as exc_info:
        setup_templates(str(template_file), str(user_file))

    assert "Template file" in str(exc_info.value)
