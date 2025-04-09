import pytest
from sqlalchemy.engine import Engine

from app.db.database import get_engine, engine_context

pytestmark = [
    pytest.mark.unit,
    pytest.mark.db
]

def test_get_engine_returns_engine():
    engine = get_engine()
    assert isinstance(engine, Engine)

def test_engine_context_yields_and_disposes():
    with engine_context() as engine:
        assert isinstance(engine, Engine)
