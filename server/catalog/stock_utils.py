import os
from dotenv import load_dotenv
from datetime import date, timedelta
from datetime import datetime
from django.utils import timezone
import requests

# Grab api key - use Twelve Data API key
load_dotenv()
api_key = os.getenv("STOCK_API_KEY", "d0025d1477344b428a9b4a7e55b187ef")

API_CALL_COOLDOWN_MINUTES = 30

def _require_api_key():
    if not api_key:
        raise RuntimeError("STOCK_API_KEY is not set in environment; cannot fetch stock prices")

def _get_last_api_call_time():
    """Get the timestamp of the last API call from the database.
    Returns the most recent last_api_call_time from any stock."""
    try:
        from catalog.models import Stock
        # Get the most recent API call time from any stock
        most_recent_stock = Stock.objects.exclude(last_api_call_time__isnull=True).order_by('-last_api_call_time').first()
        if most_recent_stock and most_recent_stock.last_api_call_time:
            return most_recent_stock.last_api_call_time
    except Exception as e:
        print(f"Warning: Could not get last API call time from database: {e}")
    return None

def _update_last_api_call_time():
    """Update the timestamp of the last API call for all stocks in the database."""
    try:
        from catalog.models import Stock
        current_time = timezone.now()
        # Update all stocks' last_api_call_time to the current time
        updated_count = Stock.objects.all().update(last_api_call_time=current_time)
        print(f"Updated last_api_call_time for {updated_count} stocks to {current_time}")
    except Exception as e:
        print(f"Warning: Could not update last API call time in database: {e}")
        import traceback
        traceback.print_exc()

def _can_make_api_call():
    """Check if we can make an API call (30 minutes have passed since last call)."""
    last_call = _get_last_api_call_time()
    if last_call is None:
        return True  # No previous call, allow it
    
    time_since_last_call = timezone.now() - last_call
    return time_since_last_call >= timedelta(minutes=API_CALL_COOLDOWN_MINUTES)

def _get_cached_price_from_db(ticker: str):
    """Get the current price from the database for a stock."""
    try:
        from catalog.models import Stock
        stock = Stock.objects.get(ticker=ticker)
        return float(stock.current_price)
    except Stock.DoesNotExist:
        return None
    except Exception:
        return None

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


def get_current_stock_price(ticker: str, use_cache=True):
    """Returns the current price of a stock as a float.
    If use_cache=True and less than 30 minutes have passed since last API call,
    returns cached price from database instead of making API call."""
    _require_api_key()
    
    # Check if we can make an API call (30-minute cooldown)
    if use_cache and not _can_make_api_call():
        # Use cached price from database
        cached_price = _get_cached_price_from_db(ticker)
        if cached_price is not None:
            print(f"Using cached price for {ticker} (API call cooldown active)")
            return cached_price
        # If no cached price available, proceed with API call anyway
    
    # Make API call
    url = f'https://api.twelvedata.com/price?symbol={ticker}&apikey={api_key}'
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        # If API call fails and we have cached data, use it
        if use_cache:
            cached_price = _get_cached_price_from_db(ticker)
            if cached_price is not None:
                print(f"API call failed for {ticker}, using cached price")
                return cached_price
        raise RuntimeError(f"Network error fetching price for {ticker}: {e}")
    
    # Check for API errors
    if 'status' in data and data['status'] == 'error':
        # If API error and we have cached data, use it
        if use_cache:
            cached_price = _get_cached_price_from_db(ticker)
            if cached_price is not None:
                print(f"API error for {ticker}, using cached price")
                return cached_price
        error_msg = data.get('message', 'Unknown error')
        raise RuntimeError(f"Twelve Data API error: {error_msg}")
    
    # Check if we have price data
    if 'price' in data:
        try:
            price = float(data['price'])
            # Update cache timestamp since we made a successful API call
            _update_last_api_call_time()
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
            # Update cache timestamp since we made a successful API call
            _update_last_api_call_time()
            return price
    except Exception as e:
        pass
    
    # If all else fails and we have cached data, use it
    if use_cache:
        cached_price = _get_cached_price_from_db(ticker)
        if cached_price is not None:
            print(f"Could not get price from API for {ticker}, using cached price")
            return cached_price
    
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
