# Write code here to populate a stock model

from django.forms import ValidationError
from catalog.models import LeagueParticipant, Matchup, Stock, League, UserLeagueStock
from catalog.views import get_start_price, get_current_price

def create_new_stock(ticker: str, name: str, start_date: str):
    """Creates a new stock in the database.
    Ticker in the format of a stock ticker, name as whatever the stock's full name is.
    Start date in format: year-month-day ex: 2025-08-09."""
    
    # Set the stock's ticker and name
    stock = Stock(ticker=ticker, name=name)
    
    # Set the stock's data from the api
    stock.start_price = get_start_price(stock.ticker, start_date)
    stock.current_price = get_current_price(stock.ticker)
    
    # Save to the database using django orm
    stock.save()
    return stock


def update_stock_price(stock_list):
    """Call current price on all stocks and return the updated list."""
    for stock in stock_list:
        stock.current_price = get_current_price(stock.ticker)
        stock.save()
        
    return stock_list
    

def create_matchup(league, week_number, participant1, participant2, start_of_week_net_worth1, start_of_week_net_worth2):
    """Creates a matchup and saves it to the database. Returns the matchup as needed."""
    matchup = Matchup(league=league, 
                      week_number=week_number, 
                      participant1=participant1, 
                      participant2=participant2, 
                      start_of_week_net_worth1=start_of_week_net_worth1, 
                      start_of_week_net_worth2=start_of_week_net_worth2)
    
    matchup.save()
    return matchup
    
# Below is some extra code for creating models

# def create_new_league(name, start_date, end_date, initial_balance=10000.00):
#     """Creates new league settings to use for a league."""
#     settings = League(start_date=start_date,
#                              end_date=end_date,
#                              name=name,
#                              initial_balance=initial_balance
#                              is_active=True)
    
#     # Test to make sure the user entered a valid start and end date
#     try:
#         settings.clean()
#         settings.save()
#         return settings
#     except ValidationError as e:
#         print(f"Validation Error: {e}")
#         return None
    
    
# def create_new_league_participant(league, user, wins, losses):
#     """Creates new League Participant."""
#     participant = LeagueParticipant(league=league, user=user, wins=wins, losses=losses)
    
#     # Save sets the current balance
#     participant.save()
#     return participant


# def create_new_user_league_stock(league_participant, stock, shares, start_of_week):
#     """Creates a new user league stock. Start date needs to be in format 'Year-Month-Day' ex:
#     2025-10-04"""
#     userLeagueStock = UserLeagueStock(league_participant=league_participant, stock=stock, shares=shares)
    
#     # Grabs price from start of the week
#     userLeagueStock.price_at_start_of_week = get_stock_closing_price(start_of_week)
    
#     userLeagueStock.save()
    