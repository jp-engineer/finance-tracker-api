## move to setup_db
import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, clear_mappers
from app.config import APP_CFG
from app.db import models
from app.db.database import Base
from app.db.utils.seed_db import seed_db_with_data

from tests.helpers import load_test_data_file

pytestmark = [
    pytest.mark.unit,
    pytest.mark.db,
    pytest.mark.utils
]

def test_seed_db_with_data_correctly_seeds_db(db_without_data):
    mock_data = load_test_data_file("app", "test_seed_db_valid_data.json")
    seed_db_with_data(mock_data, engine=db_without_data)

    with Session(db_without_data) as session:
        tx = session.query(models.TransactionAll).filter_by(id=1).first()
        sched = session.query(models.ScheduledTransaction).filter_by(id=1).first()

        assert tx is not None
        assert tx.amount == 59.99

        assert sched is not None
        assert sched.amount == 35.00

def test_seed_db_with_data_validates_model_class(db_without_data):
    bad_data = {
        "NotARealModel": [{"id": 1, "some_field": "test"}]
    }

    with pytest.raises(ValueError):
        seed_db_with_data(bad_data, engine=db_without_data)

def test_seed_db_with_data_handles_invalid_data(db_without_data):
    bad_data = {
        "TransactionAll": [{"id": 2, "invalid_field": "oops"}]
    }

    with pytest.raises(ValueError):
        seed_db_with_data(bad_data, engine=db_without_data)
