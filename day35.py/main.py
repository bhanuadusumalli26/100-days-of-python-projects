import os
from twilio.rest import Client
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Validate environment variables
required_vars = [
    "OWM_API_KEY",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_ACCOUNT_SID",
    "TWILIO_VIRTUAL_NUMBER",
    "TWILIO_VERIFIED_NUMBER",
    "RECIPIENT_PHONE",
    "OWM_Endpoint",
]

for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Environment variable {var} is missing")

# Fetch environment variables
api_key = os.getenv("OWM_API_KEY")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
from_phone = os.getenv("TWILIO_VIRTUAL_NUMBER")
to_phone = os.getenv("RECIPIENT_PHONE")
OWM_Endpoint = os.getenv("OWM_Endpoint")

# Weather parameters (you can adjust the location if needed)
weather_params = {
    "lat": 19.0760,  # Latitude (Mumbai)
    "lon": 72.8777,  # Longitude (Mumbai)
    "appid": api_key,
    "cnt": 4,  # Number of forecast intervals (3-hour intervals)
}

try:
    # Fetch weather data
    response = requests.get(OWM_Endpoint, params=weather_params)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    weather_data = response.json()

    # Initialize rain detection flag
    will_rain = any(
        int(hour_data["weather"][0]["id"]) < 700 for hour_data in weather_data["list"]
    )

    # Send SMS if rain is expected
    if will_rain:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="It's going to rain today. Remember to bring an ☂️",
            from_=from_phone,  # Your Twilio phone number
            to=to_phone,  # Recipient's phone number
        )
        print(f"Message sent successfully! Message SID: {message.sid}")
    else:
        print("No rain expected today!")

except requests.exceptions.RequestException as e:
    print(
        "Error fetching weather data. Please check your network connection or API key."
    )
except Exception as e:
    print(f"An unexpected error occurred: {e}")
