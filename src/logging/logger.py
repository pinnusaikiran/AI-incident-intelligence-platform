import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from src.logging.formatter import RequestFormatter


def configure_logging() -> None:

    # Create log directory
    LOGS_DIR=Path("logs")
    LOGS_DIR.mkdir(exist_ok=True)

    # Configure root logger
    root_logger=logging.getLogger()

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    LOG_LEVEL = logging.INFO

    root_logger.setLevel(LOG_LEVEL)

    # Configure handlers
    console_handler=logging.StreamHandler()

    application_handler = RotatingFileHandler(
    filename=LOGS_DIR/"application.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5
    )

    error_handler = RotatingFileHandler(filename=LOGS_DIR/"error.log",
                                        maxBytes=10*1024*1024,
                                        backupCount=5)

    # Configure formatters
    console_formatter=RequestFormatter("%(asctime)s | %(levelname)s | %(request_id)s | %(message)s")
    application_formatter = RequestFormatter(
    "%(asctime)s | %(levelname)s | %(request_id)s | %(filename)s | %(funcName)s | %(message)s")
    error_formatter=RequestFormatter("%(asctime)s | %(levelname)s | %(request_id)s |%(filename)s | %(funcName)s | %(name)s | %(message)s | %(process)d | %(thread)d")

    # Register handlers
    console_handler.setFormatter(console_formatter)
    application_handler.setFormatter(application_formatter)
    error_handler.setFormatter(error_formatter)

    error_handler.setLevel(logging.ERROR)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(application_handler)
    root_logger.addHandler(error_handler)





