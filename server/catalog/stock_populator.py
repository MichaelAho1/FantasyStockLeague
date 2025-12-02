# Write code here to populate a stock model

from django.forms import ValidationError
from catalog.models import LeagueParticipant, Stock, League, UserLeagueStock
from catalog.views import get_daily_closing_price
from catalog.stock_utils import get_current_stock_price

def create_new_stock(ticker: str, name: str, start_date: str):
    """Creates a new stock in the database.
    Ticker in the format of a stock ticker, name as whatever the stock's full name is.
    Start date in format: year-month-day ex: 2025-08-09."""
    from django.utils import timezone
    from datetime import date
    
    # Set the stock's ticker and name
    stock = Stock(ticker=ticker, name=name)
    
    # Set the stock's data from the api
    stock.start_price = get_daily_closing_price(stock.ticker, start_date)
    stock.current_price = get_current_stock_price(stock.ticker)
    
    # Set day_start_price to the most recent closing price (yesterday or most recent trading day)
    # This represents the price at the start of the current trading day
    try:
        from datetime import timedelta
        today = date.today()
        # Try to get yesterday's closing price
        for delta in range(1, 8):
            try_date = (today - timedelta(days=delta)).strftime('%Y-%m-%d')
            try:
                closing_price = get_daily_closing_price(stock.ticker, try_date)
                stock.day_start_price = closing_price
                stock.day_start_date = today
                break
            except Exception:
                continue
        
        # If we couldn't get a closing price, use current price as fallback
        if stock.day_start_price is None:
            stock.day_start_price = stock.current_price
            stock.day_start_date = today
    except Exception:
        # Fallback: use current price
        stock.day_start_price = stock.current_price
        stock.day_start_date = date.today()
    
    # Set last_api_call_time since we just made API calls
    stock.last_api_call_time = timezone.now()
    
    # Save to the database using django orm
    stock.save()
    return stock


def update_stock_prices(stock_list):
    """Call current price on all stocks and return the updated list.
    Also updates day_start_price if it's a new trading day."""
    from catalog.views import get_daily_closing_price
    from django.utils import timezone
    from datetime import date, timedelta
    
    today = date.today()
    
    for stock in stock_list:
        try:
            # Check if we need to update day_start_price (new trading day)
            if stock.day_start_date is None or stock.day_start_date < today:
                # Try to get yesterday's closing price for today's start price
                try:
                    # Get most recent closing price (yesterday or most recent trading day)
                    closing_price = None
                    for delta in range(1, 8):
                        try_date = (today - timedelta(days=delta)).strftime('%Y-%m-%d')
                        try:
                            closing_price = get_daily_closing_price(stock.ticker, try_date)
                            if closing_price is not None:
                                stock.day_start_price = closing_price
                                stock.day_start_date = today
                                break
                        except Exception:
                            continue
                    
                    # If we couldn't get closing price, use existing current_price from DB as fallback
                    # Don't make another API call here - we'll update current_price below anyway
                    if stock.day_start_price is None or stock.day_start_date != today:
                        if stock.current_price:
                            stock.day_start_price = stock.current_price
                            stock.day_start_date = today
                except Exception:
                    # If all else fails, keep existing day_start_price
                    pass
            
            # Get current price from API
            try:
                new_price = get_current_stock_price(stock.ticker)
                # Only update if we got a valid numeric response
                if new_price is not None:
                    stock.current_price = new_price
                    # Update last_api_call_time since we made an API call
                    stock.last_api_call_time = timezone.now()
                    stock.save()
            except RuntimeError as e:
                # If API error (like rate limit), skip this stock and continue
                # Don't crash the whole update process
                if "API credits" in str(e) or "rate limit" in str(e).lower():
                    # Skip this stock if we're out of API credits
                    continue
                # For other errors, also skip but don't spam errors
                pass
        except Exception as e:
            # Log and continue so a single failing symbol or missing API key
            # doesn't abort the entire update process.
            import traceback
            traceback.print_exc()

    return stock_list
    