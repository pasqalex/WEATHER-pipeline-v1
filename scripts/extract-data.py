import os
import sys
import requests
import json
import logging

from dotenv import load_dotenv
from datetime import datetime
from logging_config import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

def extractData() -> dict:
    load_dotenv()
    token = os.getenv("OPENWEATHER_TOKEN")

    if not token:
        raise ValueError("Check TOKEN in .env! I can't see it!")

    logger.info("Token in bank.")

    url = "https://api.openweathermap.org/data/2.5/weather"
    parameters = {
        "lat": 43.0,
        "lon": 143.35,
        "lang": "en",
        "units": "metric",
        "appid": token
    }

    response = requests.get(url, params=parameters, timeout=10)

    response.raise_for_status()

    if not response.content:
        raise ValueError("Server return empty file!")
    
    logger.info("File isn't empty.")

    try:
        data = response.json()
        logger.info("JSON parsed successfully.")
    except requests.exceptions.JSONDecodeError:
        raise ValueError("Server didn't return JSON!")

    return data

def saveRawData(data: dict, filepath: str):
    with open(filepath, "w", encoding="utf-8") as rawFile:
        json.dump(data, rawFile, ensure_ascii=False, indent=4)
        logger.info("File saved!")
        
if __name__ == "__main__":
    fileName = f"rawDataWeather-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    path = f"<your path to file>{fileName}"

    try:
        logger.info("Start extraction...")
        weather = extractData()
        saveRawData(weather, path)
        logger.info("Success!")
    except Exception as er:
        logger.exception("Script dead!")
        sys.exit(1)