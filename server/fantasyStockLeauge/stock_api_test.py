import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("STOCK_API_KEY")

# Replace "symbol=SYM" with whatever symbol you'd like to grab data from
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=GOOG&interval=5min&apikey=' + api_key
r = requests.get(url)
data = r.json()

print(data)
