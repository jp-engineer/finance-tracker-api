import os
import logging
from finance_tracker_shared.utils.setup_logging import setup_app_logging

FILE_LOG_LVL = os.environ.get("FILE_LOG_LEVEL", "DEBUG").strip().upper()
STREAM_LOG_LVL = os.environ.get("STREAM_LOG_LEVEL", "INFO").strip().upper()
setup_app_logging(FILE_LOG_LVL, STREAM_LOG_LVL)
logger = logging.getLogger(__name__)

logger.debug("Starting the application setup...")
