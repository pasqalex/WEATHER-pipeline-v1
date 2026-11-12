import logging

from datetime import datetime

path = "/home/pasqalex/pipelines/weatherPipe/tmp/"
fileName_DEBUG = f"dataWeatherExtract-DEBUG-{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
fileName_ERROR = f"dataWeatherExtract-ERROR-{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"

def full_logs(record):
    return record.levelno in (logging.INFO, logging.WARNING)

def configure_logging() -> None:
    handler1 = logging.FileHandler(f"{path}{fileName_DEBUG}", delay=True)
    handler1.setLevel(logging.INFO)
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
            ("%(levelname)-8s | %(logger)s | %(asctime)s | %(message)s")
        )
    )

    main_logger = logging.getLogger()
    main_logger.setLevel(logging.INFO)
    main_logger.addHandler(handler1)
    main_logger.addHandler(handler2)