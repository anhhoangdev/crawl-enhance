"""
Step 4: Complete Crawler with Pydantic Validation
==================================================

Goal: Add data validation and export to JSON

Concepts:
- Pydantic models for data validation
- Type checking and validation
- JSON export
- Error handling

Try it:
1. Run this file: python step4_with_models.py
2. Check the output file: car_listings.json
3. Try modifying the CarListing model to add more fields
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from models import CarListing

def fetch_car_listings(page=1):
    """Fetch and parse car listings from Bonbanh"""
    url = f"https://bonbanh.com/oto/page,{page}?q="
    print(f"Fetching page {page}...")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all LI elements with H3 (car listings)
    all_lis = soup.find_all('li')
    car_listings = [li for li in all_lis if li.find('h3')]
    listings = []
    
    for container in car_listings[:10]:  # Limit to 10 for demo
        try:
            # Extract title from H3
            h3_elem = container.find('h3')
            if not h3_elem:
                continue
            
            title = h3_elem.get_text(strip=True)
            
            # Extract URL
            link = h3_elem.find('a')
            url_raw = link.get('href', '') if link else ''
            full_url = f"https://bonbanh.com{url_raw}" if url_raw and not url_raw.startswith('http') else url_raw
            
            # Extract price
            price_elem = container.find('div', class_='price') or container.find('span', class_='price')
            price = price_elem.get_text(strip=True) if price_elem else "Contact"
            
            year = 0
            year_match = re.search(r'\b(20\d{2}|19\d{2})\b', title)
            if year_match:
                year = int(year_match.group(1))
            
            # Create Pydantic model (validates automatically!)
            car = CarListing(
                title=title,
                price=price,
                url=full_url,
                year=year
            )
            
            listings.append(car)
            
        except Exception as e:
            # Skip invalid listings
            print(f"Skipped listing due to error: {e}")
            continue
    
    return listings

def main():
    print("=" * 70)
    print("COMPLETE WEB SCRAPER WITH PYDANTIC VALIDATION")
    print("=" * 70)
    print()
    
    # Scrape data
    cars = fetch_car_listings(page=1)
    
    print(f"\n[OK] Successfully scraped {len(cars)} car listings")
    
    # Save to JSON
    output_file = "car_listings.json"
    with open(output_file, "w", encoding="utf-8") as f:
        # Convert Pydantic models to dictionaries
        car_dicts = [car.model_dump() for car in cars]
        json.dump(car_dicts, f, ensure_ascii=False, indent=2)
    
    print(f"[SAVED] Output file: {output_file}")
    
    # Print sample
    if cars:
        print("\n" + "=" * 70)
        print("SAMPLE OUTPUT:")
        print("=" * 70)
        print(cars[0].model_dump_json(indent=2))

if __name__ == "__main__":
    main()
    print("\n[COMPLETE] You've built a working web scraper!")
