# Test script to check and update last_api_call_time

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasyStockLeauge.settings')
django.setup()

from catalog.models import Stock
from django.utils import timezone

print("=" * 50)
print("Testing last_api_call_time field")
print("=" * 50)

# Check if field exists
try:
    stocks = Stock.objects.all()
    print(f"\nTotal stocks: {stocks.count()}")
    
    if stocks.count() > 0:
        print("\nCurrent stocks and their last_api_call_time:")
        for stock in stocks[:5]:
            print(f"  {stock.ticker}: last_api_call_time = {stock.last_api_call_time}")
        
        # Try to update the field
        print("\nUpdating last_api_call_time for all stocks...")
        current_time = timezone.now()
        updated_count = Stock.objects.all().update(last_api_call_time=current_time)
        print(f"Updated {updated_count} stocks")
        
        # Check again
        print("\nAfter update:")
        for stock in Stock.objects.all()[:5]:
            print(f"  {stock.ticker}: last_api_call_time = {stock.last_api_call_time}")
    else:
        print("\nNo stocks found in database!")
        print("Run populate_stocks.py first to create stocks.")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)

