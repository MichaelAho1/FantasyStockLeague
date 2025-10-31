from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import path, reverse
import os
import requests
from dotenv import load_dotenv
from datetime import date

from catalog.stock_utils import get_current_stock_price, get_stock_closing_price

def response_not_found_view(request, exception=None):
    return HttpResponseNotFound("Page not found", status=404)

# redefine 404 error variable to our custom page
handler404 = response_not_found_view

load_dotenv()

api_key = os.getenv("STOCK_API_KEY")

def get_absolute_url(self):
    """Returns the url to access a particular genre instance."""
    return reverse('stock-detail', args=[str(self.id)])
    

def get_start_price(ticker: str, start_date: str):
    """Returns the daily performance of a stock. Start date must be in the format
    'year-month-day' with leading 0s as needed. ex: '2025-06-23'"""
    return get_stock_closing_price(ticker, start_date)
    
        
def get_current_price(ticker):
    """Returns the current price of a stock."""
    get_current_stock_price(ticker)
        

def get_total_profit(ticker, start_date):
    "Returns the daily performance of a stock"
    # TODO use api to calculate this
