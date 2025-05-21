import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(log_level="INFO"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(level)
    # Remove all handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    handler = RotatingFileHandler(
        os.path.join(log_dir, "qsomapge.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def set_log_level(log_level):
    """
    Set Log Level at runtime
    """
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.getLogger().setLevel(level)