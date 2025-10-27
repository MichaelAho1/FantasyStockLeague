from django.contrib.auth.models import User
from rest_framework import generics
from server.api.serializer import StockSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from catalog.models import Stock


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