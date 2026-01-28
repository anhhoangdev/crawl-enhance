import requests
from bs4 import BeautifulSoup
import re

print("Testing different selectors on Bonbanh...\n")
r = requests.get('https://bonbanh.com/oto/page,1?q=')
soup = BeautifulSoup(r.content, 'html.parser')

# Test 1: H3 tags (found 23)
h3_tags = soup.find_all('h3')
print(f"Method 1 - H3 tags: {len(h3_tags)}")
if h3_tags:
    for i, h3 in enumerate(h3_tags[:3], 1):
        link = h3.find('a')
        if link:
            print(f"  {i}. {h3.get_text()[:50]}")
            print(f"     URL: {link.get('href', 'N/A')[:60]}")

# Test 2: Links with /oto pattern
print(f"\nMethod 2 - Links with /oto:")
oto_links = soup.find_all('a', href=re.compile(r'/oto-'))
print(f"Found: {len(oto_links)}")
if oto_links:
    for i, link in enumerate(oto_links[:3], 1):
        print(f"  {i}. {link.get_text()[:50]}")
        print(f"     URL: {link.get('href', 'N/A')[:60]}")

# Test 3: Look for list items
print(f"\nMethod 3 - List items (li):")
li_items = soup.find_all('li')
print(f"Total LI: {len(li_items)}")

# Filter for car listings
car_lis = [li for li in li_items if li.find('h3')]
print(f"LI with H3: {len(car_lis)}")

if car_lis:
    print("\nSample car listing structure:")
    sample = car_lis[0]
    h3 = sample.find('h3')
    if h3:
        print(f"  Title: {h3.get_text()[:50]}")
    price_div = sample.find('div', class_='price')
    if price_div:
        print(f"  Price: {price_div.get_text()[:50]}")
