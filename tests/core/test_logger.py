import logging
import os

from core.logger import get_logger, setup_logging


def test_get_logger():
    logger = get_logger("test_module")
    assert logger.name == "test_module"
    assert isinstance(logger, logging.Logger)


def test_setup_logging_uses_config():
    # This tests that it actually loads the config file which sets root to WARNING
    # and 'tictactoe' to DEBUG.
    setup_logging()

    root_logger = logging.getLogger()
    assert root_logger.getEffectiveLevel() == logging.WARNING

    tictactoe_logger = get_logger("tictactoe")
    assert tictactoe_logger.getEffectiveLevel() == logging.DEBUG


def test_logs_directory_created():
    setup_logging()
    assert os.path.exists("logs")
