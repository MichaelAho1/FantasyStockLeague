from django.contrib.auth.models import User
from rest_framework import generics
from api.serializer import StockSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from catalog.models import Stock, UserLeagueStocks


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
    #serializer_class = UserLeagueStocksSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        current_user = request.user
        owned_stocks = (UserLeagueStocks.objects.filter(current_user))
        stocks = []
        for stock in owned_stocks:
            data = {
                "price_bought":stock.price_bought,
                "shares":stock.shares,
                "current_price":stock.stock.current_price,
                "start_price":stock.stock.start_price,
                "ticker":stock.stock.ticker,
                "name":stock.name,
            }
            stocks.append(data)
        return Response(stocks)

