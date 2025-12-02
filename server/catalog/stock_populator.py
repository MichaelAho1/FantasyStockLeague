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
    
    # Set the stock's ticker and name
    stock = Stock(ticker=ticker, name=name)
    
    # Set the stock's data from the api
    stock.start_price = get_daily_closing_price(stock.ticker, start_date)
    stock.current_price = get_current_stock_price(stock.ticker, use_cache=False)
    
    # Set last_api_call_time since we just made API calls
    stock.last_api_call_time = timezone.now()
    
    # Save to the database using django orm
    stock.save()
    return stock


def update_stock_prices(stock_list):
    """Call current price on all stocks and return the updated list.
    Respects 30-minute API call cooldown - if cooldown is active, uses cached prices."""
    from catalog.stock_utils import _can_make_api_call
    
    # Check if we can make API calls (30-minute cooldown)
    can_make_api_call = _can_make_api_call()
    
    if not can_make_api_call:
        print("API call cooldown active (30 minutes). Using cached prices from database.")
        return stock_list  # Return stocks without updating (they already have cached prices)
    
    # We can make API calls, update all stocks
    print("Updating stock prices via API...")
    from django.utils import timezone
    
    for stock in stock_list:
        try:
            # We already checked the cooldown, but still use use_cache=True to respect it
            # in case the cooldown state changed between the check and the call
            new_price = get_current_stock_price(stock.ticker, use_cache=True)
            # Only update if we got a valid numeric response
            if new_price is not None:
                stock.current_price = new_price
                # Update last_api_call_time since we made an API call
                # (get_current_price should have updated it, but ensure it's set)
                stock.last_api_call_time = timezone.now()
                stock.save()
        except Exception as e:
            # Log and continue so a single failing symbol or missing API key
            # doesn't abort the entire update process.
            import traceback
            print(f"Error updating {stock.ticker}: {e}")
            print(traceback.format_exc())

    return stock_list
    