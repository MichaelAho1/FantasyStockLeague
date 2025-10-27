from django.db import models

# Create your models here.
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

class Stock(models.Model):
    """Model representing a specific stock."""
    ticker = models.ForeignKey('Ticker', on_delete=models.RESTRICT, null=True) # e.g. AAPL, GOOG
    name = models.CharField(max_length=200)  # name of stock (e.g. Nvidia, Apple)
    start_price = models.FloatField()
    current_price = models.FloatField()
    profit = models.FloatField()
    shares = models.IntegerField()
    # Might want an owner field
    
    def __str__(self):
        """String for representing the Model object."""
        return self.ticker


class Portfolio(models.Model):
    """Model representing a user's portfolio"""
    user = models.CharField(max_length=100)


class User(models.Model):
    """Model reresenting a user"""
    name = models.CharField(max_length=200)
    
    
class LeagueSettings(models.Model):
    """Model reresenting the settings for the league"""
    start_date = models.DateField()
    end_date = models.DateField()
