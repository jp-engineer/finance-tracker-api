import pytest
pytestmark = [
    pytest.mark.unit,
    pytest.mark.utils
]
import yaml
from app.utils.shared import read_yaml_file

def test_read_yaml_file_returns_data(tmp_path):
    test_file = tmp_path / "test.yml"
    content = {
        "general": {"currency": "USD"},
        "developer": {"start_date": "2025-04-04"}
    }

    with open(test_file, "w", encoding="utf-8") as f:
        yaml.dump(content, f)

    result = read_yaml_file(str(test_file))

    assert isinstance(result, dict)
    assert result["general"]["currency"] == "USD"
    assert result["developer"]["start_date"] == "2025-04-04"

def test_read_yaml_file_file_not_found_returns_empty_dict(tmp_path):
    missing_file = tmp_path / "does_not_exist.yml"
    result = read_yaml_file(str(missing_file))

    assert isinstance(result, dict)
    assert result == {}
