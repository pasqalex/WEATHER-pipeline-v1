import logging
import os

from logging.handlers import RotatingFileHandler
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
path = os.path.join(PROJECT_ROOT, "tmp", "logs")

def full_logs(record):
    return record.levelno in (logging.INFO, logging.WARNING)

def configure_logging() -> None:
    handler1 = logging.FileHandler(f"{path}INFO.log", delay=True)
    handler1.setLevel(logging.INFO)

    handler1 = RotatingFileHandler(
        filename=f"{path}INFO.log",
        maxBytes=1 * 10240 * 10240,
        backupCount=5,
        encoding="utf-8"
    )

    handler1.addFilter(full_logs)
    handler1.setFormatter(
    logging.Formatter(
            ("%(levelname)-4s | %(name)s | %(asctime)s | %(message)s")
        )
    )

    handler2 = logging.FileHandler(f"{path}ERRORS.log")
    handler2.setLevel(logging.ERROR)
    handler2.setFormatter(
        logging.Formatter(
            ("%(levelname)-8s | %(name)s | %(asctime)s | %(message)s")
        )
    )

    main_logger = logging.getLogger()
    main_logger.setLevel(logging.INFO)
    main_logger.addHandler(handler1)
    main_logger.addHandler(handler2)