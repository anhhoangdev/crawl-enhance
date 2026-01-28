"""
Step 3: Async Requests with aiohttp
====================================

Goal: Fetch multiple pages concurrently using asyncio

Concepts:
- Asynchronous programming (async/await)
- aiohttp for async HTTP requests
- Concurrent requests (much faster!)
- asyncio.gather for parallel execution

Try it:
1. Run this file: python step3_async_requests.py
2. Notice how fast it fetches 5 pages!
3. Try increasing total_pages and see the speed difference

WARNING: Don't set total_pages too high or you might get rate-limited!
"""

import aiohttp
import asyncio
import json
from typing import List, Dict
import time

# API configuration
API_URL = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx"
SYMBOL = "VNINDEX"

async def fetch_page(session: aiohttp.ClientSession, page_index: int) -> List[Dict]:
    """
    Fetch a single page of data asynchronously
    
    Args:
        session: aiohttp session (reusable connection)
        page_index: Which page to fetch
        
    Returns:
        List of records from that page
    """
    params = {
        "Symbol": SYMBOL,
        "StartDate": "",
        "EndDate": "",
        "PageIndex": page_index,
        "PageSize": 20
    }
    
    print(f"  Fetching page {page_index}...")
    
    try:
        async with session.get(API_URL, params=params) as response:
            data = await response.json(content_type=None)  # content_type=None handles any mime type
            
            if data.get("Success"):
                records = data.get("Data", {}).get("Data", [])
                print(f"  ✅ Page {page_index}: {len(records)} records")
                return records
            else:
                print(f"  ❌ Page {page_index}: Failed - {data.get('Message')}")
                return []
                
    except Exception as e:
        print(f"  ❌ Page {page_index}: Error - {e}")
        return []

async def fetch_all_pages(total_pages: int = 5) -> List[Dict]:
    """
    Fetch multiple pages concurrently
    
    Args:
        total_pages: How many pages to fetch
        
    Returns:
        Combined list of all records
    """
    print("=" * 70)
    print(f"FETCHING {total_pages} PAGES CONCURRENTLY")
    print("=" * 70)
    print()
    
    # Create a single session for all requests (connection pooling!)
    async with aiohttp.ClientSession() as session:
        # Create tasks for all pages
        tasks = [fetch_page(session, i) for i in range(1, total_pages + 1)]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)
        
        # Flatten the list (results is a list of lists)
        all_records = [record for page_records in results for record in page_records]
        
        return all_records

def main():
    start_time = time.time()
    
    # Run the async function
    # Note: On Windows, you might need to set the event loop policy
    if __import__("sys").platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Fetch 5 pages concurrently
    records = asyncio.run(fetch_all_pages(total_pages=5))
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Total records: {len(records)}")
    print(f"Time taken: {elapsed:.2f} seconds")
    print(f"Speed: {len(records) / elapsed:.1f} records/second")
    print()
    
    # Save to file
    output_file = "vnindex_async.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved to: {output_file}")
    print()
    print("=" * 70)
    print("⚡ ASYNC IS FAST!")
    print("   Try comparing this to Selenium's speed!")
    print("=" * 70)

if __name__ == "__main__":
    main()
    print("\nNext step: Add rate limiting to be respectful to the server")
