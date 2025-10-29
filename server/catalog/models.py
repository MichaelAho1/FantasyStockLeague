from django.db import models

# Create your models here.
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field


class Portfolio(models.Model):
    """Model representing a user's portfolio"""
    user = models.CharField(max_length=100)
    
    
class LeagueSettings(models.Model):
    """Model reresenting the settings for the league"""
    start_date = models.DateField()
    end_date = models.DateField()
    
    
class User(models.Model):
    """Model reresenting a user"""
    name = models.CharField(max_length=200)
    
    
class Stock(models.Model):
    """Model representing a specific stock."""
    user_id = models.ForeignKey(User, on_delete=models.SET_DEFAULT)
    ticker = models.CharField(primary_key = True)
    name = models.CharField(max_length=200)  # name of stock (e.g. Nvidia, Apple)
    start_price = models.FloatField()
    current_price = models.FloatField()
    profit = models.FloatField()
    shares = models.IntegerField()
    
    def __str__(self):
        """String for representing the Model object."""
        return self.ticker
    
