from datetime import timezone
from django.db import models

# Create your models here.
from django.forms import ValidationError
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.contrib.auth.models import User # Use django user


class Portfolio(models.Model):
    """Model representing a user's portfolio"""
    user = models.OneToOneField(
        User,  # django user
        on_delete=models.CASCADE,
        related_name='portfolio'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Portfolio for {self.user.username}"
    
    
class Stock(models.Model):
    """Model representing a specific stock."""
    user = models.ForeignKey(
        User,  # django user
        on_delete=models.CASCADE,
        related_name='stocks',
        null=True,
        blank=True
    )
    # Ticker as primary key
    ticker = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=200)
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    shares = models.IntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ticker} - {self.name}"
    
    @property
    def profit(self):
        return (self.current_price - self.start_price) * self.shares
    
    
class LeagueSetting(models.Model):
    """Model representing the settings for the league"""
    name = models.CharField(max_length=100, default="Trading League")
    start_date = models.DateField()
    end_date = models.DateField()
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")
    
    @property
    def is_ongoing(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class LeagueParticipant(models.Model):
    """Links users to leagues and tracks their performance"""
    league = models.ForeignKey(LeagueSetting, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='league_participations')
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    rank = models.IntegerField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['league', 'user']
        ordering = ['-total_value']
    
    def __str__(self):
        return f"{self.user.username} in {self.league.name}"
    
    def save(self, *args, **kwargs):
        # Set initial balance when first created
        if not self.pk:
            self.current_balance = self.league.initial_balance
            self.total_value = self.league.initial_balance
        super().save(*args, **kwargs)
    
    @property
    def profit(self):
        return self.total_value - self.league.initial_balance
