# Force an API update to test last_api_call_time

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasyStockLeauge.settings')
django.setup()

from catalog.models import Stock
from catalog.stock_utils import get_current_stock_price, _update_last_api_call_time, _can_make_api_call
from django.utils import timezone

print("=" * 60)
print("FORCING API UPDATE TO TEST last_api_call_time")
print("=" * 60)

# Check current state
stocks = Stock.objects.all()
print(f"\nTotal stocks in database: {stocks.count()}")

if stocks.count() == 0:
    print("\nNo stocks found! Please run populate_stocks.py first.")
    exit(1)

print("\nCurrent last_api_call_time values:")
for stock in stocks[:5]:
    print(f"  {stock.ticker}: {stock.last_api_call_time}")

# Check if we can make API call
can_call = _can_make_api_call()
print(f"\nCan make API call (30 min cooldown check): {can_call}")

if not can_call:
    last_call = Stock.objects.exclude(last_api_call_time__isnull=True).order_by('-last_api_call_time').first()
    if last_call:
        time_since = timezone.now() - last_call.last_api_call_time
        print(f"Last API call was {time_since.total_seconds() / 60:.1f} minutes ago")
        print(f"Need to wait {30 - (time_since.total_seconds() / 60):.1f} more minutes")

# Force update by manually calling the API for one stock
print("\n" + "-" * 60)
print("Forcing API call for first stock...")
first_stock = stocks.first()
print(f"Stock: {first_stock.ticker}")

try:
    # This will make an API call and update last_api_call_time
    price = get_current_stock_price(first_stock.ticker, use_cache=False)
    print(f"Got price: ${price}")
    
    # Also manually update all stocks
    _update_last_api_call_time()
    
    print("\nAfter API call:")
    for stock in Stock.objects.all()[:5]:
        print(f"  {stock.ticker}: last_api_call_time = {stock.last_api_call_time}")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

