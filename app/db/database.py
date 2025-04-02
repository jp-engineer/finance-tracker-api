import os
from sqlalchemy import create_engine
from app.db.base_class import Base
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)

def get_engine():
    db_url = f"sqlite:///{APP_CFG['DB_PATH']}"
    logger.debug(f"Creating database engine with URL: {db_url}")
    return create_engine(db_url, echo=False, future=True)

def init_db():
    from app.db.models import setting  # local import to avoid circular import
    if not os.path.exists(APP_CFG["DB_PATH"]):
        logger.debug(f"Database file does not exist. Creating: {APP_CFG['DB_PATH']}")
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
