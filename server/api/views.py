from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import generics
from api.serializer import StockSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from catalog.models import LeagueParticipant, Stock, UserLeagueStock, League
from api.utils import getCurrentOpponent, getUserWeeklyStockProfits, getOwnedStocks, getTotalStockValue

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ViewAllStocks(generics.ListCreateAPIView):
    serializer_class = StockSerializer
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        stocks = []
        for stock in Stock.objects.all():
            data = {
                "ticker":stock.ticker,
                "name":stock.name,
                "start_price":stock.start_price,
                "current_price":stock.current_price,
            }
            stocks.append(data)
        return Response(stocks)


class ViewAllOwnedStocks(generics.ListCreateAPIView):
    #serializer_class = UserLeagueStockSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None):
        owned_stocks = getOwnedStocks(league_id, request.user)
        stocks = []

        for stock in owned_stocks:
            data = {
                "shares":stock.shares,
                "current_price":stock.stock.current_price,
                "start_price":stock.stock.start_price,
                "ticker":stock.stock.ticker,
                "name":stock.name,
            }
            stocks.append(data)
        return Response(stocks)

class ViewUserWeeklyProfits(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None):
        stocks = getUserWeeklyStockProfits(league_id, request.user)
        return Response(stocks)

class ViewOpponentWeeklyProfits(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None):
        stocks = getUserWeeklyStockProfits(league_id, getCurrentOpponent(league_id, request.user))
        return Response(stocks)
        
class LeagueView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    # Creating a new league
    def post(self, request, league_name, start_date, format=None):
        end_date = start_date + timedelta(weeks=7)
        League.objects.create(name=league_name, start_date=start_date, end_date=end_date)

    # Viewing Data in a league
    def get(self, request, league_id):
        current_league = League.objects.get(league_id=league_id)
        league_participants = LeagueParticipant.objects.get(League=current_league)
        leagueUserData = []
        for league_participant in league_participants:
            total_profit = 0
            for stock in getOwnedStocks(league_id, league_participant.user):
                total_profit += (stock.price_at_start_of_week - stock.stock.current_price) * stock.shares
            data = {
                "user":league_participant.user,
                "wins":league_participant.wins,
                "losses":league_participant.losses,
                "net_worth": getTotalStockValue(league_id, league_participant.user) + league_participant.current_balance,
                "weekly_profit": total_profit,
                # Still needs schedule
            }
            leagueUserData.append(data)
        return Response(leagueUserData)

class ViewAllLeagues(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        #if a user is a superuser then get all leagues
        #if a user is normal then get all leagues there in and there permissions
        print("temp")
# Buy stocks
# Sell stocks


