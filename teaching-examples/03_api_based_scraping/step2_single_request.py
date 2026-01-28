"""
Step 2: Make a Single API Request
==================================

Goal: Fetch data directly from the CafeF API using requests

Concepts:
- Direct API calls (no browser needed!)
- URL parameters
- JSON parsing
- API response structure

Try it:
1. Run this file: python step2_single_request.py
2. See how much faster this is than Selenium!
3. Try changing the parameters
"""

import requests
import json

print("=" * 70)
print("CALLING CAFEF API DIRECTLY")
print("=" * 70)
print()

# The API endpoint we discovered in step1
api_url = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx"

# Parameters for the request
params = {
    "Symbol": "VNINDEX",      # Stock symbol
    "StartDate": "",          # Empty = all dates
    "EndDate": "",            # Empty = all dates
    "PageIndex": 1,           # Page number
    "PageSize": 20            # Items per page
}

print("API URL:", api_url)
print("Parameters:", json.dumps(params, indent=2))
print()

# Make the request
print("Sending request...")
response = requests.get(api_url, params=params)

print(f"Status Code: {response.status_code}")
print()

# Parse JSON response
data = response.json()

# Check if successful
if data.get("Success"):
    print("✅ API call successful!")
    
    # Extract the actual data
    records = data.get("Data", {}).get("Data", [])
    print(f"Received: {len(records)} records")
    print()
    
    # Print first record
    if records:
        print("=" * 70)
        print("FIRST RECORD:")
        print("=" * 70)
        print(json.dumps(records[0], indent=2, ensure_ascii=False))
        print()
        
        # Show what fields are available
        print("=" * 70)
        print("AVAILABLE FIELDS:")
        print("=" * 70)
        for key in records[0].keys():
            print(f"  - {key}")
        
else:
    print("❌ API call failed!")
    print(f"Message: {data.get('Message')}")

print()
print("=" * 70)
print("⚡ Note: This is MUCH faster than Selenium!")
print("   No browser launch, no waiting for page load!")
print("=" * 70)
print()
print("Next step: Use async to fetch multiple pages in parallel")
