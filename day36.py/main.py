import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")  # Virtual number
RECIPIENT_PHONE = os.getenv("RECIPIENT_PHONE")  # The recipient's phone number

# Stock API parameters
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

# Fetch stock data
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for key, value in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday_day = data_list[1]
day_before_yesterday_day_closing_price = day_before_yesterday_day["4. close"]

# Calculate price difference
difference = abs(
    float(yesterday_closing_price) - float(day_before_yesterday_day_closing_price)
)
diff_percent = (difference / float(yesterday_closing_price)) * 100

# If the stock price changed more than 1%, fetch news and send SMS
if diff_percent > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [
        f"Headline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles
    ]

    # Initialize Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_PHONE_NUMBER,  # Twilio Virtual Number
            to=RECIPIENT_PHONE,  # Recipient's phone number
        )
        print(f"Message sent: {message.sid}")
