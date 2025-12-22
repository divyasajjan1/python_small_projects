# Weather Forecast vs. Real-Time Observation

## Project Overview
This project compares weather forecasts with real-time observations at your location. Using the OpenWeatherMap API, it retrieves hourly forecast data and checks if rain is expected around the current local time. The script then allows the user to input their own observation (whether it is raining at their location) and compares it with the forecast to check consistency.

## Features
- Fetch hourly weather forecast from OpenWeatherMap API.
- Convert forecast timestamps to local timezone automatically.
- Compare forecast rain with the user’s actual observation.
- Display clear messages indicating whether the forecast matches reality.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd <repo-folder>

2. Create a virtual environment and activate it
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # OR
    venv\Scripts\activate     # Windows

3. Install required packages
   pip install -r requirements.txt

4. Create a .env file in the project root and add your OpenWeatherMap API key
    OPENWEATHER_API_KEY=your_api_key_here

## Usage
1. Run the script:
    python weather_api.py

2. When prompted, input whether it is raining at your location:
    Did it rain at your location right now? (yes/no):

3. The script will display:

    Forecasted rain at your current time
    Your observation
    Whether the forecast matches your observation

## Dependencies

requests — for API calls
python-dotenv — for loading API keys from .env

## Notes

Forecast is based on the hourly API and considers a ±30-minute window around the current local time.

Ensure your system clock and timezone are correct for accurate comparison.


