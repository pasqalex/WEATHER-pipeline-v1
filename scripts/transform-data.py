import sys
import os
import pandas

from datetime import datetime

# Default logging procedure
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Handler and his friends
handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | [%(levelname)-8s] | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
)
logger.addHandler(handler)



logger.debug("Debug lvl")
logger.info("INFO lvl")
logger.warning("WARNING lvl")
logger.error("ERROR lvl")
logger.critical("CRITICAL lvl")


# def func():
#     pass #ToDo

# def finc():
#     pass #ToDo

# if __name__ == "__main__":
#     try:
#         pass #ToDo
#     except pass #ToDo