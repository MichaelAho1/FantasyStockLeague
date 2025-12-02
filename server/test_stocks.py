# Test script to check stocks and API

import os
import django

# Setup Django FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasyStockLeauge.settings')
django.setup()

from catalog.models import Stock
from catalog.stock_utils import get_current_stock_price, get_stock_closing_price
from datetime import date, timedelta

print("=" * 50)
print("STOCK DATABASE CHECK")
print("=" * 50)

# Check stocks in database
stock_count = Stock.objects.count()
print(f"\nTotal stocks in database: {stock_count}")

if stock_count > 0:
    print("\nExisting stocks:")
    for stock in Stock.objects.all()[:10]:
        print(f"  - {stock.ticker}: {stock.name} (Current: ${stock.current_price}, Start: ${stock.start_price})")
else:
    print("\nNo stocks found in database!")
    print("You need to run: python populate_stocks.py")

print("\n" + "=" * 50)
print("TESTING TWELVE DATA API")
print("=" * 50)

# Test API with a single stock
test_ticker = "AAPL"
print(f"\nTesting API with {test_ticker}...")

try:
    # Test current price
    print(f"Fetching current price for {test_ticker}...")
    current_price = get_current_stock_price(test_ticker)
    print(f"  ✓ Current price: ${current_price:.2f}")
except Exception as e:
    print(f"  ✗ Error getting current price: {e}")

try:
    # Test historical price (yesterday)
    test_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"Fetching closing price for {test_ticker} on {test_date}...")
    closing_price = get_stock_closing_price(test_ticker, test_date)
    print(f"  ✓ Closing price on {test_date}: ${closing_price:.2f}")
except Exception as e:
    print(f"  ✗ Error getting closing price: {e}")

print("\n" + "=" * 50)

