import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)

Base = declarative_base()

def get_engine():
    db_url = f"sqlite:///{APP_CFG['DB_PATH']}"
    return create_engine(db_url, echo=False, future=True)

def init_db():
    if not os.path.exists(APP_CFG["DB_PATH"]):
        logger.info(f"Database file {APP_CFG['DB_PATH']} not found. Creating a new database.")
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
