import os
from twilio.rest import Client
import requests

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# Load sensitive data from environment variables
api_key = os.getenv("OWM_API_KEY")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
from_phone = os.getenv("TWILIO_FROM_PHONE")
to_phone = os.getenv("RECIPIENT_PHONE")

weather_params = {
    "lat": 19.0760,  # Latitude for location
    "lon": 72.8777,  # Longitude for location
    "appid": api_key,  # API Key
    "cnt": 4,         # Number of forecasts to retrieve
}

# Fetch weather data

# Fetch weather data
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

# Initialize the rain detection flag
will_rain = False

# Check weather conditions
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:  # Weather codes < 700 indicate rain
        will_rain = True
        break  # Exit the loop if rain is detected

# Send SMS if it will rain
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☂️",
        from_='',  # Your Twilio number
        to=''        # Recipient's number
    )
    print(f"Message Status: {message.status}")


