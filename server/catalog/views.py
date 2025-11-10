from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import path, reverse
import os
import requests
from dotenv import load_dotenv
from datetime import date

from catalog.stock_utils import get_current_stock_price, get_profit_float, get_stock_closing_price

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
    
        
def get_current_price(ticker: str):
    """Returns the current price of a stock."""
    return get_current_stock_price(ticker)
        

def get_stock_profit(ticker: str, start_date: str):
    """Returns the current profit (as a float) of a stock since a start date. Start date should be
    In the format year-month-day ex: '2025-06-23'"""
    # TODO use api to calculate this
    return get_profit_float(ticker, start_date)
