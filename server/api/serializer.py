from datetime import timedelta
from django.contrib.auth.models import User 
from rest_framework import serializers
from catalog.models import League, Stock

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}} 

    def create(self, validated_data): 
        user = User.objects.create_user(**validated_data)
        return user

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["ticker", "name", "start_price", "current_price"]

class LeaguesSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['league_id', 'name', 'start_date', 'end_date']
        read_only_fields = ['league_id', 'end_date']
    
    def create(self, validated_data):
        start_date = validated_data["start_date"]
        validated_data["end_date"] = start_date + timedelta(weeks=7)
        return super().create(validated_data)