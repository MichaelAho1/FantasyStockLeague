from django.contrib.auth.models import User 
from rest_framework import serializers
from catalog.models import Stock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["ticker", "name", "start_price", "current_price"]
