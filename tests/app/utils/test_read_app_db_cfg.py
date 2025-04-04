# import pytest
# from app.db.database import init_db, engine_context
# from app.utils.read_app_db_cfg import get_db_cfg_dict
# from app.config import APP_CFG
# from app.utils.read_app_db_cfg import check_entry_in_settings_table

# @pytest.mark.unit
# @pytest.mark.db
# def test_check_entry_returns_false_for_empty_table(tmp_path, monkeypatch):
#     db_path = tmp_path / "no_data.db"
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

#     init_db()

#     with engine_context() as engine:
#         result = check_entry_in_settings_table(engine)
#         assert result is False

# @pytest.mark.unit
# @pytest.mark.db
# def test_get_db_cfg_before_db_creation(tmp_path, monkeypatch):
#     fake_db_path = tmp_path / "fake.db"
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(fake_db_path))

#     cfg = get_db_cfg_dict()
#     assert cfg["EXISTS"] is False
#     assert cfg["HAS_TABLES"] is False
#     assert cfg["DB_PATH"] == str(fake_db_path)
#     assert cfg["TABLES"] == []

# @pytest.mark.unit
# @pytest.mark.db
# def test_get_db_cfg_after_db_creation(tmp_path, monkeypatch):
#     db_path = tmp_path / "test.db"
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

#     init_db()

#     cfg = get_db_cfg_dict()
#     assert cfg["EXISTS"] is True
#     assert cfg["HAS_TABLES"] is True
#     assert "settings" in cfg["TABLES"]
