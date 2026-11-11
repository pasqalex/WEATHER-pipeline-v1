import requests
import os
import sys
from dotenv import load_dotenv

def dataExtract() -> dict:
    load_dotenv()

    token = os.getenv("OPENWEATHER_TOKEN")

    if not token:
        raise ValueError("Token not found in .env")

    url = "https://api.openweathermap.org/data/2.5/weather"
    block = {
        "lat": 43.0,
        "lon": 141.35,
        "units": "metric",
        "lang": "en",
        "appid": token
    }

    response = requests.get(url, params=block, timeout=20)

    response.raise_for_status()

    return response.json()


def saveRawData(data: dict, filepath: str):
    import json

    with open(filepath, "w", encoding="utf-8") as rawFile:
        json.dump(data, rawFile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    try:
        print("Start extraction...")
        weather = dataExtract()
        saveRawData(weather, "<your path to file>")
        print("Success!")
    except Exception as er:
        print(f"Error: {er}")
        sys.exit(1)
