"""
Step 1: Basic HTTP Request
===========================

Goal: Fetch HTML content from a website using Python's requests library

Concepts:
- HTTP GET request
- Response object
- Basic HTML structure

Try it:
1. Run this file: python step1_basic_request.py
2. Observe the raw HTML output
3. Notice the HTML tags like <html>, <body>, <div>, etc.
"""

import requests

# Target URL - page 1 of car listings
url = "https://bonbanh.com/oto/page,1?q="

print("Fetching webpage...")
print(f"URL: {url}\n")

# Send GET request
response = requests.get(url)

# Check if request was successful
print(f"Status Code: {response.status_code}")  # 200 means success
print(f"Content Type: {response.headers['content-type']}\n")

# Print first 500 characters of HTML
print("=" * 50)
print("HTML PREVIEW (first 500 characters):")
print("=" * 50)
print(response.text[:500])
print("..." + "\n")

# Full HTML is available in response.text
print(f"Total HTML length: {len(response.text)} characters")

# Next step: We'll use BeautifulSoup to parse this HTML!
