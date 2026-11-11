import os
import sys
import requests
import json

from dotenv import load_dotenv
from datetime import datetime

def extractData() -> dict:
    load_dotenv()
    token = os.getenv("OPENWEATHER_TOKEN")

    if not token:
        raise ValueError("Check TOKEN in .env! I can't see it!")

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
    
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        raise ValueError("Server didn't return JSON!")

    return data

def saveRawData(data: dict, filepath: str):
    with open(filepath, "a", encoding="utf-8") as rawFile:
        json.dump(data, rawFile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fileName = f"rawDataWeather-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    path = f"<your path to file>/{fileName}"

    try:
        print("Start extraction...")
        weather = extractData()
        saveRawData(weather, path)
        print("Success!")
    except Exception as er:
        raise ValueError(f"Error: {er}")
