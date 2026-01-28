"""
Step 3: Extract Multiple Data Fields
=====================================

Goal: Extract title, price, URL, and year from car listings

Concepts:
- CSS selectors for different elements
- Extracting attributes (href)
- Regular expressions for pattern matching
- Storing data in dictionaries

Try it:
1. Run this file: python step3_extract_data.py
2. Notice how we extract different types of data
3. Try adding more fields (look at the HTML in your browser!)
"""

import sys
import os

# Fix Windows console encoding for Vietnamese characters
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import requests
from bs4 import BeautifulSoup
import re

# Fetch and parse
url = "https://bonbanh.com/oto/page,2?q="
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all list items (li) that contain car listings
# On Bonbanh, car listings are in <li> elements with <h3> tags
all_lis = soup.find_all('li')
car_listings = [li for li in all_lis if li.find('h3')]

print("=" * 70)
print("EXTRACTING STRUCTURED DATA")
print("=" * 70)

cars = []  # List to store all car data

# Process each car listing (limit to first 5 for demo)
for container in car_listings[:5]:
    # Extract title from H3
    h3_elem = container.find('h3')
    if not h3_elem:
        continue
    
    title = h3_elem.get_text(strip=True)
    
    # Extract URL from link in H3
    link = h3_elem.find('a')
    url_raw = link.get('href', '') if link else ''
    full_url = f"https://bonbanh.com{url_raw}" if url_raw and not url_raw.startswith('http') else url_raw
    
    # Extract price (look for price class or text)
    price_elem = container.find('div', class_='price') or container.find('span', class_='price')
    price = price_elem.get_text(strip=True) if price_elem else "Contact"
    
    # Extract year using regex from title
    year = 0
    year_match = re.search(r'\b(20\d{2}|19\d{2})\b', title)
    if year_match:
        year = int(year_match.group(1))
    
    # Store in dictionary
    car_data = {
        "title": title,
        "price": price,
        "url": full_url,
        "year": year
    }
    
    cars.append(car_data)

# Print results
print(f"\nExtracted data for {len(cars)} cars:\n")

for i, car in enumerate(cars, 1):
    print(f"--- Car {i} ---")
    print(f"Title: {car['title']}")
    print(f"Price: {car['price']}")
    print(f"Year:  {car['year']}")
    print(f"URL:   {car['url'][:60]}...")
    print()

print("[OK] Successfully extracted structured data!")
print("Next step: Add validation using Pydantic models")
