import requests
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "1411bc433e82abdeb1a9f61b485c113d"
auth_token = "48ed6e94ffcae52b70fb7de3631e5196"
account_sid = "AC25519d68fc8a4ad3cb644f419990d62e"

weather_params = {
    "lat": 19.0760,  
    "lon": 72.8777,  
    "appid": api_key,  # API Key
    "cnt": 4,          # Number of forecasts to retrieve
}

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
        from_='+91 84989 15364',  # Your Twilio number
        to='+18777804236'        # Recipient's number
    )
    print(f"Message Status: {message.status}")

    