# setup logging
import os
from finance_tracker_shared.utils.setup_logging import setup_app_logging

FILE_LOG_LVL = os.environ.get("FILE_LOG_LEVEL", "DEBUG").strip().upper()
STREAM_LOG_LVL = os.environ.get("STREAM_LOG_LEVEL", "INFO").strip().upper()
setup_app_logging(
    file_level=FILE_LOG_LVL,
    stream_level=STREAM_LOG_LVL
)


from app.core.setup_app import create_app

app = create_app()
