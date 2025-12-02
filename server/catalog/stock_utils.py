import os
from dotenv import load_dotenv
from datetime import date, timedelta, datetime
import requests

# Grab api key - use Twelve Data API key
load_dotenv()
api_key = os.getenv("STOCK_API_KEY", "f99e95eaa5da47d0b01313a81c685c9a")

def _require_api_key():
    if not api_key:
        raise RuntimeError("STOCK_API_KEY is not set in environment; cannot fetch stock prices")


def get_stock_closing_price(ticker: str, date: str):
    """Returns the closing performance of a stock as a float. Start date must be in the format
    'year-month-day' with leading 0s as needed. ex: '2025-06-23'"""
    _require_api_key()
    
    # Twelve Data API endpoint for time series - get last 30 days and find the date
    url = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=30&apikey={api_key}'
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Network error fetching closing price for {ticker}: {e}")
    
    # Check for API errors
    if 'status' in data and data['status'] == 'error':
        error_msg = data.get('message', 'Unknown error')
        raise RuntimeError(f"Twelve Data API error: {error_msg}")
    
    # Check if we have data - Twelve Data returns 'values' array
    if 'values' not in data or len(data['values']) == 0:
        # Try to get the most recent available date before the requested date
        # Go back up to 7 days to find a trading day
        for delta in range(1, 8):
            try_date = (datetime.strptime(date, '%Y-%m-%d').date() - timedelta(days=delta)).strftime('%Y-%m-%d')
            try:
                url_fallback = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=30&apikey={api_key}'
                r_fallback = requests.get(url_fallback, timeout=10)
                r_fallback.raise_for_status()
                data_fallback = r_fallback.json()
                
                if 'status' in data_fallback and data_fallback['status'] == 'error':
                    continue
                    
                if 'values' in data_fallback and len(data_fallback['values']) > 0:
                    # Find the date in the values
                    for value in data_fallback['values']:
                        value_datetime = value.get('datetime', '')
                        if value_datetime.startswith(try_date):
                            return float(value['close'])
                    # If date not found, return most recent
                    return float(data_fallback['values'][0]['close'])
            except Exception:
                continue
        raise RuntimeError(f"Could not retrieve closing price for {ticker} on {date}. No data available.")
    
    # Find the specific date in the values array
    for value in data['values']:
        value_datetime = value.get('datetime', '')
        if value_datetime.startswith(date):
            return float(value['close'])
    
    # If exact date not found, try to find most recent date before requested date
    for value in data['values']:
        value_datetime = value.get('datetime', '')
        value_date = value_datetime.split()[0] if ' ' in value_datetime else value_datetime
        if value_date and value_date <= date:
            return float(value['close'])
    
    # Fallback to most recent value
    if len(data['values']) > 0:
        return float(data['values'][0]['close'])
    
    raise RuntimeError(f"Could not retrieve closing price for {ticker} on {date}. Response: {data}")


def get_current_stock_price(ticker: str):
    """Returns the current price of a stock as a float."""
    _require_api_key()
    
    # Make API call
    url = f'https://api.twelvedata.com/price?symbol={ticker}&apikey={api_key}'
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Network error fetching price for {ticker}: {e}")
    
    # Check for API errors
    if 'status' in data and data['status'] == 'error':
        error_msg = data.get('message', 'Unknown error')
        raise RuntimeError(f"Twelve Data API error: {error_msg}")
    
    # Check if we have price data
    if 'price' in data:
        try:
            price = float(data['price'])
            return price
        except (ValueError, TypeError):
            pass
    
    # Fallback to time series if price endpoint doesn't work
    try:
        url_ts = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=1&apikey={api_key}'
        r_ts = requests.get(url_ts, timeout=10)
        r_ts.raise_for_status()
        data_ts = r_ts.json()
        
        if 'status' in data_ts and data_ts['status'] == 'error':
            error_msg = data_ts.get('message', 'Unknown error')
            raise RuntimeError(f"Twelve Data API error: {error_msg}")
        
        if 'values' in data_ts and len(data_ts['values']) > 0:
            price = float(data_ts['values'][0]['close'])
            return price
    except Exception:
        pass
    
    raise RuntimeError(f"Could not retrieve current price for {ticker}. Response: {data}")


def get_profit_float(ticker: str, start_date: str):
    """Returns the profit of a stock as a float from a certain date to today."""
    _require_api_key()
    
    # Get current price
    current_price = get_current_stock_price(ticker)
    
    # Get start date price
    start_price = get_stock_closing_price(ticker, start_date)
    
    total_profit = current_price - start_price
    return total_profit
