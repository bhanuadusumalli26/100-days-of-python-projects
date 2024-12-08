import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DataManager:
    SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_PRICES_ENDPOINT"]
    SHEETY_USERS_ENDPOINT = os.environ["SHEETY_USERS_ENDPOINT"]

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.SHEETY_PRICES_ENDPOINT)
        response.raise_for_status()
        self.destination_data = response.json()["sheet1"]
        return self.destination_data

    def update_destination_codes(self):
        for destination in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": destination["iataCode"],
                }
            }
            response = requests.put(
                url=f"{self.SHEETY_PRICES_ENDPOINT}/{destination['id']}", json=new_data
            )
            response.raise_for_status()

    def get_customer_emails(self):
        response = requests.get(url=self.SHEETY_USERS_ENDPOINT)
        response.raise_for_status()
        return response.json()["users"]
