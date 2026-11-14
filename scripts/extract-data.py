import os
import sys
import requests
import json
import logging
import yaml

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv
from datetime import datetime

from logging_config import configure_logging
from load_data import loadToDB

load_dotenv()
configure_logging()
extract_logger = logging.getLogger(__name__)


def load_sources(config_path: str = "../config/source.yml") -> dict:
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def extractData() -> dict:

    sources = load_sources("../config/source.yml")
    OPENweather_config = sources["openweather"]

    token = os.getenv("OPENWEATHER_TOKEN")
    if not token:
        raise ValueError("Check TOKEN in .env! I can't see it!")

    extract_logger.info("Token in bank.")

    url = OPENweather_config["url"]
    parameters = OPENweather_config["parameters"].copy()
    parameters["appid"] = token
    timeout = OPENweather_config["timeout"]

    session = requests.Session()
    retry_strategy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    response = session.get(
        url, 
        params=parameters, 
        timeout=timeout
    )

    response.raise_for_status()

    if not response.content:
        raise ValueError("Server return empty file!")
    
    extract_logger.info("File isn't empty.")

    try:
        data = response.json()
        extract_logger.info("JSON parsed successfully.")
    except requests.exceptions.JSONDecodeError as e:
        extract_logger.error("Server didn't return JSON: %s", e)

    return data

def saveRawData(data: dict, filepath: str):
    with open(filepath, "w", encoding="utf-8") as rawFile:
        json.dump(data, rawFile, ensure_ascii=False, indent=4)
        extract_logger.info("File saved!")
    extract_logger.info(f"File saved to: {filepath}")
    return filepath
        
if __name__ == "__main__":
    fileName = f"rawDataWeather-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    path = f"<path to your file>{fileName}"

    try:
        extract_logger.info("Start extraction...")
        weather = extractData()
        file_path = saveRawData(weather, path)
        loadToDB(file_path)
        extract_logger.info("Success!")
    except Exception as er:
        extract_logger.exception("Script dead!")
        sys.exit(1)