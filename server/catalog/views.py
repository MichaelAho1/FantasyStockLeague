from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import path

def response_not_found_view(request, exception=None):
    return HttpResponseNotFound("Page not found", status=404)

# redefine 404 error variable to our custom page
handler404 = response_not_found_view

def get_absolute_url(self):
    """Returns the url to access a particular genre instance."""
    return reverse('stock-detail', args=[str(self.id)])
    
def get_daily_performance(self):
    "Returns the daily performance of a stock"
    # TODO use api to grab daily performance
        
def get_weekly_performance(self):
    "Returns the daily performance of a stock"
    # TODO use api to grab daily performance
        
def get_monthly_performance(self):
    "Returns the daily performance of a stock"
    # TODO use api to grab daily performance
