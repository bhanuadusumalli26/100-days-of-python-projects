import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
pixela_endpoint = "https://pixe.la/v1/users"
TOKEN = os.getenv("PIXELA_TOKEN")
USERNAME = os.getenv("PIXELA_USERNAME")
GRAPH_ID = os.getenv("PIXELA_GRAPH_ID")

# Create a user (Uncomment to run once)
user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

# Create a graph (Uncomment to run once)
graph_endpoints = f"{pixela_endpoint}/{USERNAME}/graphs"
graph_config = {
    "id": GRAPH_ID,
    "name": "Cyclic Graph",
    "unit": "km",
    "type": "float",
    "color": "ajisai",
}
headers = {"X-USER-TOKEN": TOKEN}
# response = requests.post(url=graph_endpoints, json=graph_config, headers=headers)
# print(response.text)

# Create a pixel
pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
today = datetime.now()  # Automatically fetches today's date
pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "5.24",
}

# Uncomment to create a pixel
# response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
# print(response.text)

# Update a pixel
update_endpoint = (
    f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"
)
new_pixel_data = {"quantity": "7.54"}
# Uncomment to update a pixel
# response = requests.put(url=update_endpoint, json=new_pixel_data, headers=headers)
# print(response.text)

# Delete a pixel
delete_endpoint = (
    f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"
)
# Uncomment to delete a pixel
# response = requests.delete(url=delete_endpoint, headers=headers)
# print(response.text)
