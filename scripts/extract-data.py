import os
import requests
import logging
import json

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