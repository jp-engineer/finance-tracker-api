import os
import logging
import tempfile
from app.utils.setup_app_logging import setup_app_logging

def test_setup_app_logging_creates_log_file_and_handlers():
    temp_log_dir = tempfile.mkdtemp()
    log_file_name = "test-ft-api.log"
    log_path = os.path.join(temp_log_dir, log_file_name)

    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    setup_app_logging(log_dir=temp_log_dir, log_file=log_file_name)

    assert os.path.isfile(log_path)

    handlers = logger.handlers
    assert len(handlers) == 2
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in handlers)

    test_message = "This is a test log entry."
    logger.debug(test_message)

    with open(log_path, "r", encoding="utf-8") as f:
        log_contents = f.read()
        assert test_message in log_contents
