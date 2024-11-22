import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY="23JPRO1PSJ6IZHR5"
NEWS_API_KEY="aa36b6420f8c428e956075dd9dec4520"
auth_token = "48ed6e94ffcae52b70fb7de3631e5196"
account_sid = "AC25519d68fc8a4ad3cb644f419990d62e"
stock_params={
     "function":"TIME_SERIES_DAILY",
     "symbol":STOCK_NAME,
     "apikey":STOCK_API_KEY,
 }
response=requests.get(STOCK_ENDPOINT,params=stock_params)
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items() ]
yesterday_data=data_list[0]
yesterday_closing_price=yesterday_data['4. close']
day_before_yesterday_day=data_list[1]
day_before_yesterday_day_closing_price=day_before_yesterday_day['4. close']
difference=abs(float(yesterday_closing_price)-float(day_before_yesterday_day_closing_price))
diff_percent=(difference/float(yesterday_closing_price))*100
if diff_percent>1:
   news_params={
      "apiKey": NEWS_API_KEY,
      "qInTitle":COMPANY_NAME,
   }
   news_response=requests.get(NEWS_ENDPOINT,params=news_params)
   articles=news_response.json()["articles"]
   three_articles=articles[:3]
formatted_articles=[f"Headline:{article['title']}.\nBrief:{article ['description']}"for article in three_articles]
client = Client(account_sid, auth_token)
for article in formatted_articles:
    message=client.messages.create(
        body=article,
        from_='+19375304293',
        to='+198498915364',
    )