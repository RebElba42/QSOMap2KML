import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(debug=False):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(log_level)
    # Remove all handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    # File handler only, no console
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