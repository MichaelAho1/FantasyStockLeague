from datetime import timezone
import uuid
from django.db import models

# Create your models here.
from django.forms import ValidationError
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.contrib.auth.models import User # Use django user
    
class Stock(models.Model):
    """Model representing a specific stock."""
    # Ticker as primary key
    ticker = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=200)
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ticker} - {self.name}"
    
    @property
    def profit(self):
        return (self.current_price - self.start_price) * self.shares
    
    
class LeagueSetting(models.Model):
    """Model representing the settings for the league"""
    league_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, default="Trading League")
    start_date = models.DateField() # This will be selected by the user on creating a league
    end_date = models.DateField() # This should be autopopulated (8 weeks after start day)
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} ({self.league_id})"
    
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")
    
    def create(self):
        if not self.schedules.exists():  
            for week in range(1, 9): 
                LeagueSchedule.objects.create(weekNumber=week, League=self)

    @property
    def is_ongoing(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class LeagueParticipant(models.Model):
    """Links users to leagues and tracks their performance"""
    league = models.ForeignKey(LeagueSetting, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='league_participations')
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ['league', 'user']
    
    def __str__(self):
        return f"{self.user.username} in {self.league.name}"
    
    def save(self, *args, **kwargs):
        # Set initial balance when first created
        if not self.pk:
            self.current_balance = self.league.initial_balance
            self.total_value = self.league.initial_balance
        super().save(*args, **kwargs)

class UserLeagueStocks(models.Model):
    """Links league participant to a stock"""
    LeagueParticipant = models.ForeignKey(LeagueParticipant, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    priceBought = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    shares = models.DecimalField(decimal_places=2, default=0.01, max_digits=10)

    def __str__(self):
        return f"{self.LeagueParticipant} in {self.stock}"

class LeagueSchedule(models.Model):
    """Model representing a leagues schedule"""
    weekNumber = models.PositiveIntegerField()
    League = models.ForeignKey(LeagueSetting, on_delete=models.CASCADE, related_name="schedules")

    # This needs to be actual matchups (User vs User) instead of just char fields
    matchup1 = models.CharField(max_length=100, blank=True, null=True)
    matchup2 = models.CharField(max_length=100, blank=True, null=True)
    matchup3 = models.CharField(max_length=100, blank=True, null=True)
    matchup4 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ['League', 'weekNumber']
        ordering = ['weekNumber']

    def __str__(self):
        return f"Week {self.weekNumber} - {self.League.name}"