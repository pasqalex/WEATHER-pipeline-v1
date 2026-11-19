import os
import requests
import logging
import json
import yaml

from dotenv import load_dotenv
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime, timezone

from logging_config import configure_logging


load_dotenv()
configure_logging()
logger = logging.getLogger(__name__)


def extractData(configSource: dict, saveTo: str) -> str:
    """Download data from one API and save raw JSON to disk

    Reads source config file with URL, parameters, timeout and token.
    Retries on errors and raises on permanent failures.

    Args:
        configSource: config dictionary to one source from source.yml
        saveTo: absolute path to raw JSON

    Return:
        Path to the saved file
    """

    logger.info("START EXTRACTION...")

    url = configSource["url"]
    parameters = {**configSource["parameters"]}
    timeout = configSource["timeout"]

    token = None

    if configSource.get("token_env"):
        token = os.getenv(configSource.get("token_env"))
        if not token:
            raise ValueError("Token NOT FOUND in .env")
    
    logger.info("With parameters: %s, %s", parameters, timeout)
    if token:
        parameters["appid"] = token

    logger.info("Making a request to a URL: %s", url)

    with requests.Session() as session:
        retryStrategy = Retry(
            total=10,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        session.mount("https://", HTTPAdapter(max_retries=retryStrategy))
        session.mount("http://", HTTPAdapter(max_retries=retryStrategy))

        response = session.get(
            url,
            params=parameters,
            timeout=timeout
        )
        response.raise_for_status()

        if not response.content:
            raise ValueError("API return EMPTY file")
            
        logger.info("API return OK file")

        try:
            data = response.json()
            logger.info("JSON parsed SUCCESSFULLY")
        except requests.exceptions.JSONDecodeError as e:
            logger.error("Raw response: %s", response.text[:500])
            raise ValueError(f"API didn't return JSON") from e
            

        with open(saveTo, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

        logger.info("Data saved to %s", saveTo)
        
        return saveTo

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    configPath = os.path.join(PROJECT_ROOT, "config", "source.yml")
    rawDir = os.path.join(PROJECT_ROOT, "data", "raw")
    os.makedirs(rawDir, exist_ok=True)
    try:
        with open(configPath, "r", encoding="utf-8") as file:
            sources = yaml.safe_load(file)
            if not sources:
                raise ValueError(f"Config file at {configPath} is EMPTY")
    except FileNotFoundError:
        logger.error("Config file not found at %s", configPath)
        exit(1)

    successCount = 0
    failedSources = []

    startTime = datetime.now()
    
    dateNow = datetime.now(timezone.utc)

    for sourceName, config in sources.items(): 
        try:
            filePath = os.path.join(rawDir, f"{sourceName}-{dateNow.strftime('%Y-%m-%d_%H-%M')}.json")
            extractData(config, filePath)
            # loadToDB(filePath)
            successCount += 1
            logger.info("API [ %s ] -- done", sourceName)
        except Exception as e:
            logger.error("API [ %s ] -- failed with error: %s", sourceName, e)
            failedSources.append(sourceName)

    endTime = datetime.now()
    
    logger.info(f"Result: SUCCESS - {successCount}; FAILED - {len(failedSources)}; TIME - {endTime - startTime}")
    if failedSources:
        logger.warning("Failed API: [ %s ]", failedSources)