import json
import logging.config
import logging
import os

def setup_logging(
    default_path="logging_config.json",
    default_level=logging.INFO,
    env_key="LOG_CFG"
):
    """
    Sets up logging configuration from a JSON file or environment variable.
    If the file is not found, defaults to basic logging with the specified level.
    """
    # Get path relative to this file's directory if not provided via env var
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, default_path)

    value = os.getenv(env_key, None)
    if value:
        path = value

    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def get_logger(name: str) -> logging.Logger:
    """Returns a logger instance with the given name."""
    return logging.getLogger(name)
