import os
from twilio.rest import Client
import requests

# OpenWeatherMap API endpoint
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# Load sensitive data from environment variables
api_key = os.getenv("OWM_API_KEY")        # OpenWeatherMap API Key
auth_token = os.getenv("TWILIO_AUTH_TOKEN")  # Twilio Auth Token
account_sid = os.getenv("TWILIO_ACCOUNT_SID")  # Twilio Account SID
from_phone = os.getenv("TWILIO_FROM_PHONE")   # Twilio From Phone Number
to_phone = os.getenv("RECIPIENT_PHONE")       # Recipient's Phone Number

# Weather parameters
weather_params = {
    "lat": 19.0760,  # Latitude (Mumbai)
    "lon": 72.8777,  # Longitude (Mumbai)
    "appid": api_key,  # OpenWeatherMap API Key
    "cnt": 4,         # Number of forecast intervals to retrieve
}

try:
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
            from_=from_phone,  # Your Twilio phone number
            to=to_phone        # Recipient's phone number
        )
        print(f"Message sent successfully! Message SID: {message.sid}")
    else:
        print("No rain expected today!")

except Exception as e:
    print(f"An error occurred: {e}")



