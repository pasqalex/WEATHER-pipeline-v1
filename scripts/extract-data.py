import os
import requests
import logging
import json
import yaml

from dotenv import load_dotenv
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime

from logging_config import configure_logging


load_dotenv()
configure_logging()
logger = logging.getLogger(__name__)


def extractData(configSource: dict, saveTo: str) -> str:
    
    url = configSource["url"]
    parameters = configSource["parameters"]
    timeout = configSource["timeout"]

    token = None

    if configSource.get("token_env"):
        token = os.getenv(configSource.get("token_env"))
        if not token:
            raise ValueError("Token NOT FOUND in .env")
    
    if token:
        parameters["appid"] = token

    logger.info("Making a request to a URL: %s", url)
    logger.debug("With parameters: %s, %s", parameters, timeout)

    session = requests.Session()

    retryStategy = Retry(
        total=10,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    session.mount("https://", HTTPAdapter(max_retries=retryStategy))
    session.mount("http://", HTTPAdapter(max_retries=retryStategy))

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
        raise ValueError("API didn't return JSON: \n [ %s ]", e)
        

    with open(saveTo, "w", encoding="utf-8") as file:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info("Data saved to %s", saveTo)
    
    return saveTo

if __name__ == "__main__":

    try:
        with open("../config/source.yml", "r", encoding="utf-8") as file:
            sources = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error("Config file not found at ../config/source.yml")

    successCount = 0
    failed_sources = []

    for source_name, config in sources.items():
        try:
            filePath = extractData(config, f"/home/pasqalex/pipelines/WEATHER-pipeline-v1/data/raw/{source_name}.json")
            # loadToDB(filePath)
            successCount += 1
            logger.info(f"API [ {source_name} ] -- done")
        except Exception as e:
            logger.error(f"API [ {source_name} ] -- failed with error: {e}")
            failed_sources.append(source_name)

    logger.info(f"Result: \n SUCCESS - {successCount} \n FAILED - {len(failed_sources)}")
    if failed_sources:
        logger.warning(f"Failed API: {failed_sources}")