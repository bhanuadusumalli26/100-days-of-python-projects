import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch sensitive data from environment variables
API_KEY = os.getenv("NUTRITIONIX_API_KEY")
API_ID = os.getenv("NUTRITIONIX_API_ID")
END_POINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
BEARER_TOKEN = os.getenv("SHEETY_BEARER_TOKEN")
SHEET_ENDPOINT = os.getenv("SHEETY_ENDPOINT")

headers = {
    "Content-Type": "application/json",
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
}

exercise_text = input("Tell me which exercises you did: ")
NLP_config = {"query": exercise_text}

# Nutritionix API call to get exercise data
response = requests.post(END_POINT, json=NLP_config, headers=headers)
response.raise_for_status()
result = response.json()

# Sheety API headers
sheety_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Log exercises into Sheety
for exercise in result["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheet_response = requests.post(
        SHEET_ENDPOINT, json=sheet_inputs, headers=sheety_headers
    )
    sheet_response.raise_for_status()
    print(sheet_response.text)
