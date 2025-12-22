#Use weather api to find rain on that day at any time and check it with your 
#time, did it rain at the same time at your place?

import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timezone, timedelta

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
LAT = 42.3149      # Windsor, ON
LON = -83.0364
#url = "https://api.openweathermap.org/data/2.5/forecast/hourly"
#url = "https://api.openweathermap.org/data/2.5/weather"
url = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "lat": LAT,
    "lon": LON,
    "appid": api_key,
    "units": "metric"
}

response = requests.get(url, params=params)
data = response.json()

if "list" not in data:
    print("Unexpected API response:")
    print(data)
    exit()

current_time = datetime.now().astimezone()  # local timezone aware
tolerance = timedelta(minutes=30)
rain_found = False

for hour in data["list"]:
    timestamp = hour["dt"]
    forecast_time_local = datetime.fromtimestamp(hour["dt"], tz=timezone.utc).astimezone()

    if abs(forecast_time_local - current_time) <= tolerance:
        rain_amount = hour.get("rain", {}).get("3h", 0)
        rain_probability = hour.get("pop", 0)

        print(f"Forecast for your current time ({forecast_time_local}):")
        print(f"Rain (mm) : {rain_amount}")
        print(f"Rain Probability: {rain_probability}")
        print("-" * 40)

        if rain_amount > 0 or rain_probability > 0.5:
            rain_found = True
        break

if rain_found:
    print("🌧️ Forecast indicates rain at your current time.")
else:
    print("☀️ No rain forecasted at your current time.")

# Ask the user if it rained at their location
user_input = input("Did it rain at your location right now? (yes/no): ").strip().lower()

# Convert input to boolean
if user_input in ["yes", "y"]:
    my_observation = True
else:
    my_observation = False

# Compare API forecast with user's observation
if rain_found and my_observation:
    print("✅ Forecast and your observation both indicate rain.")
elif not rain_found and not my_observation:
    print("✅ Forecast and your observation both indicate no rain.")
elif rain_found and not my_observation:
    print("⚠️ Forecast predicted rain, but you observed no rain.")
else:
    print("⚠️ Forecast predicted no rain, but you observed rain.")
