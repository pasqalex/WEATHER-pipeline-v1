import os
import sys
import requests
import json
import logging

from load_data import loadToDB

from dotenv import load_dotenv
from datetime import datetime
from logging_config import configure_logging

load_dotenv()
configure_logging()

extract_logger = logging.getLogger(__name__)

def extractData() -> dict:
    token = os.getenv("OPENWEATHER_TOKEN")
    if not token:
        raise ValueError("Check TOKEN in .env! I can't see it!")

    extract_logger.info("Token in bank.")

    url = "https://api.openweathermap.org/data/2.5/weather"
    parameters = {
        "lat": 43.0,
        "lon": 143.35,
        "lang": "en",
        "units": "metric",
        "appid": token
    }

    response = requests.get(url, params=parameters, timeout=(3, 10))

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