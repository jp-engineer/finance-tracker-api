from contextlib import contextmanager
from sqlalchemy import create_engine

from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)


@contextmanager
def engine_context():
    engine = get_engine()
    try:
        yield engine
    finally:
        engine.dispose()


def get_engine() -> object:
    db_url = f"sqlite:///{APP_CFG['DB_PATH']}"
    logger.debug(f"Creating database engine for URL: {db_url}")
    engine = create_engine(db_url, echo=False, future=True)

    return engine