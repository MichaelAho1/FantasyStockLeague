from catalog.models import League, Stock, UserLeagueStock, LeagueParticipant

def getOwnedStocks(league_id, user):
    current_league = League.objects.get(league_id=league_id)
    return UserLeagueStock.objects.filter(league_participant__user=user,league_participant__league=current_league)

def getTotalStockValue(league_id, user):
    owned_stocks = getOwnedStocks(league_id, user)
    total = 0
    for stock in owned_stocks:
        total += stock.shares * stock.stock.current_price
    return total

def getLeagueNetWorths(league_id, user):
    current_league = League.objects.get(league_id=league_id)
    league_participants = LeagueParticipant.objects.get(League=current_league)
    netWorths = {}
    for league_participant in league_participants:
        netWorths[league_participant] = getTotalStockValue(league_id, user) + league_participant.current_balance

    return netWorths