import pytest
from sqlalchemy.exc import OperationalError

from app.db.database import get_engine
from app.config import APP_CFG

from app.core.read_db_cfg import (
    check_entries_present_in_settings_general_table,
    get_db_cfg_dict
)


pytestmark = [
    pytest.mark.unit, 
    pytest.mark.db,
    pytest.mark.core
]


def test_check_entries_present_in_settings_table(seeded_db):
    engine = get_engine()

    assert check_entries_present_in_settings_general_table(engine) is True


def test_check_entries_present_in_settings_table_with_non_existent_db(monkeypatch, tmp_path):
    fake_path = tmp_path / "nonexistent.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(fake_path))

    engine = get_engine()

    with pytest.raises(OperationalError):
        check_entries_present_in_settings_general_table(engine)

    
def test_get_db_cfg_dict(seeded_db):
    db_path = seeded_db
    cfg = get_db_cfg_dict()

    expected = {
        "DB_PATH": str(db_path),
        "EXISTS": True,
        "HAS_TABLES": True,
        "TABLES": ['accounts_all', 'accounts_credit', 'accounts_debit', 'accounts_independent', 
                   'folios', 'recurring_transactions', 'scheduled_transactions', 
                   'settings_developer', 'settings_general', 'settings_view', 
                   'transactions_all', 'transactions_expense', 'transactions_payment', 'transactions_transfer'],
        "TABLES_COUNT": 14,
        "HAS_DATA": True
    }

    assert cfg == expected


def test_get_db_cfg_dict_with_non_existent_db(monkeypatch, tmp_path):
    fake_path = tmp_path / "nonexistent.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(fake_path))

    cfg = get_db_cfg_dict()

    expected = {
        "DB_PATH": str(fake_path),
        "EXISTS": False,
        "HAS_TABLES": False,
        "TABLES": [],
        "TABLES_COUNT": 0,
        "HAS_DATA": False
    }

    assert cfg == expected