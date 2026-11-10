import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("OPENWEATHER_TOKEN")

url = "https://api.openweathermap.org/data/2.5/weather"
parameters = {
    "lat": 43.0,
    "lon": 141.35,
    "units": "metric",
    "lang": "en",
    "appid": token
}

response = requests.get(url, params=parameters)
print(f"Status: {response.status_code}")

if (response.status_code == 200):
    data = response.json()

    city = data["name"]
    temperature = data["main"]["temp"]
    weather_desc = data["weather"][0]["description"]

    print(f"Weather in {city} now:")
    print(f"Temperature: {temperature} C")
    print(f"Now outside: {weather_desc}")
else:
    print("API error:", response.text)
