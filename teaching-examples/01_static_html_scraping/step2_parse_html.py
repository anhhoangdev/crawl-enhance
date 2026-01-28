"""
Step 2: Parse HTML with BeautifulSoup
======================================

Goal: Parse HTML and extract car titles using CSS selectors

Concepts:
- BeautifulSoup HTML parser
- Finding elements by tag name
- Extracting text from elements

Try it:
1. Run this file: python step2_parse_html.py
2. You should see a list of car titles
3. Try changing 'h3' to other tags and see what happens!
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

# Fetch the webpage
url = "https://bonbanh.com/oto/page,1?q="
print(f"Fetching: {url}\n")

response = requests.get(url)
html_content = response.content  # Raw HTML bytes

# Parse HTML with BeautifulSoup
# 'html.parser' is Python's built-in parser (no extra install needed)
soup = BeautifulSoup(html_content, 'html.parser')

print("=" * 50)
print("EXTRACTING CAR TITLES")
print("=" * 50)

# Find all <h3> tags which contain the car titles
# On Bonbanh, each car listing has a <h3> with the title
h3_elements = soup.find_all('h3')

print(f"Found {len(h3_elements)} car listings\n")

# Extract and print the text from each title
for i, h3_element in enumerate(h3_elements, 1):
    title_text = h3_element.get_text(strip=True)  # strip=True removes extra whitespace
    print(f"{i:2d}. {title_text}")

print("\n[OK] Successfully extracted car titles!")
print("Next step: Extract more data (price, URL, etc.)")
