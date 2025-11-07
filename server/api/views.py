from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import generics
from api.serializer import StockSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from catalog.models import Stock, UserLeagueStock, League
from api.utils import getLeagueNetWorths, getOwnedStocks, getTotalStockValue

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


class ViewAllStockWeeklyProfits(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None):
        # Put this in a util function so i can call it in viewLeagueData to get all stock weekly profits (Then we can delete this API)
        owned_stocks = getOwnedStocks(league_id, request.user)
        stocks = []

        for stock in owned_stocks:
            weekly_profit = (stock.price_at_start_of_week - stock.stock.current_price) * stock.shares
            data = {
                "ticker":stock.stock.ticker,
                "weekly_profit":weekly_profit,
            }
            stocks.append(data)
        return Response(stocks)

class ViewLeagueData(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None): 
        league_net_worth = getLeagueNetWorths(league_id, request.user)
        
class LeagueView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    # Creating a new league
    #TODO FINISH THIS
    def post(self, request, league_name, start_date, format=None):
        end_date = start_date + timedelta(weeks=8)
        league = League.objects.create(name=league_name, start_date=start_date, end_date=end_date)

    # Viewing Data in a league
    def get(self, request, league_id):
        print("TEMP")


