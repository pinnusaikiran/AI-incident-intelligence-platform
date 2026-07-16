import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from contextvars import ContextVar


def configure_logging():

    logs_dir=Path("logs")
    logs_dir.mkdir(exist_ok=True)

    request_id = ContextVar("request_id")
    root_logger=logging.getLogger()

    root_logger.setLevel(logging.INFO)

    console_handler=logging.StreamHandler()

    application_handler = RotatingFileHandler(
    filename="logs/application.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5
    )

    error_handler = RotatingFileHandler(filename="logs/error.log",
                                        maxBytes=10*1024*1024,
                                        backupCount=5)

    console_formatter=logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    application_formatter=logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s |%(name)s | %(message)s")
    error_formatter=logging.Formatter("%(asctime)s | %(levelname)s |%(filename)s | %(funcName)s | %(name)s | %(message)s | %(process)d | %(thread)d")

    console_handler.setFormatter(console_formatter)
    application_handler.setFormatter(application_formatter)
    error_handler.setFormatter(error_formatter)

    

    root_logger.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(application_handler)
    root_logger.addHandler(error_handler)