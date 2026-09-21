import sys
import os

from decimal import Decimal
from datetime import date

import requests
import xml.etree.ElementTree as ET
import psycopg

import logging

logging.basicConfig (
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

with open("/run/secrets/password") as f:
    DB_PASSWORD = f.read().strip()
    
DB_NAME = os.environ["DB_NAME"],
DB_USER = os.environ["DB_USER"],
DB_HOST = os.environ.get("DB_HOST", "db")



# Место под будущие функции



if __name__ == "__main__":
    load(date.today())