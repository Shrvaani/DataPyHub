import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

def fetch_weather_data(city: str):
    """Fetch current weather data for a given city."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url)
    data = r.json()

    if r.status_code != 200:
        raise Exception(f"API Error: {data.get('message', 'Unknown error')}")

    df = pd.DataFrame({
        "city": [city],
        "temp": [data["main"]["temp"]],
        "humidity": [data["main"]["humidity"]],
        "pressure": [data["main"]["pressure"]],
        "wind_speed": [data["wind"]["speed"]],
        "weather": [data["weather"][0]["description"]],
    })
    return df
