import pytest
from app.config import APP_CFG

from app.core.read_db_cfg import (
#    check_entries_present_in_settings_table
    get_db_cfg_dict
)

pytestmark = [
    pytest.mark.unit, 
    pytest.mark.db,
    pytest.mark.core
]

# def test_check_entries_present_in_settings_table_returns_true(db_with_single_setting):
#     assert check_entries_present_in_settings_table(db_with_single_setting) is True

# def test_check_entries_present_in_settings_table_returns_false(db_without_data):
#     assert check_entries_present_in_settings_table(db_without_data) is False

# def test_get_db_cfg_dict_with_db_exists(db_with_single_setting):
#     cfg = get_db_cfg_dict()

#     assert cfg["EXISTS"] is True
#     assert cfg["HAS_TABLES"] is True
#     assert "settings" in cfg["TABLES"]
#     assert cfg["TABLES_COUNT"] >= 1
#     assert cfg["HAS_DATA"] is True

def test_get_db_cfg_dict_with_db_does_not_exist(monkeypatch, tmp_path):
    fake_path = tmp_path / "nonexistent.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(fake_path))

    cfg = get_db_cfg_dict()

    assert cfg["EXISTS"] is False
    assert cfg["HAS_TABLES"] is False
    assert cfg["TABLES"] == []
    assert cfg["TABLES_COUNT"] == 0
    assert cfg["HAS_DATA"] is False
