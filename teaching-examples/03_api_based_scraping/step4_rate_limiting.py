"""
Step 4: Complete Scraper with Rate Limiting
============================================

Goal: Production-ready async scraper with rate limiting and Pydantic

Concepts:
- Semaphore for concurrency control
- Rate limiting (be nice to servers!)
- Pydantic validation
- Complete error handling
- Multiple export formats

Try it:
1. Run this file: python step4_rate_limiting.py
2. Notice the controlled concurrency
3. Check the output files

Best Practices Applied:
- Max 5 concurrent requests (semaphore)
- Validates data with Pydantic
- Handles errors gracefully
- Exports to JSON and CSV
"""

import aiohttp
import asyncio
import json
import pandas as pd
from typing import List
from models import StockData
import time

class CafeFAsyncCrawler:
    """
    Production-ready async crawler for CafeF stock data
    """
    
    API_URL = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx"
    
    def __init__(self, symbol: str = "VNINDEX", max_concurrent: int = 5):
        """
        Args:
            symbol: Stock symbol to scrape
            max_concurrent: Maximum concurrent requests (rate limiting)
        """
        self.symbol = symbol
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def fetch_page(self, session: aiohttp.ClientSession, page_index: int) -> List[StockData]:
        """Fetch a single page with rate limiting"""
        
        # Semaphore ensures max_concurrent requests at a time
        async with self.semaphore:
            params = {
                "Symbol": self.symbol,
                "StartDate": "",
                "EndDate": "",
                "PageIndex": page_index,
                "PageSize": 20
            }
            
            try:
                async with session.get(self.API_URL, params=params, headers=self.headers) as response:
                    data = await response.json(content_type=None)
                    
                    if not data.get("Success"):
                        print(f"  ⚠️  Page {page_index}: API returned success=false")
                        return []
                    
                    records = data.get("Data", {}).get("Data", [])
                    
                    # Validate with Pydantic
                    validated = []
                    for record in records:
                        try:
                            stock_data = StockData(**record)
                            validated.append(stock_data)
                        except Exception as e:
                            # Skip invalid records
                            continue
                    
                    print(f"  ✅ Page {page_index}: {len(validated)} valid records")
                    return validated
                    
            except Exception as e:
                print(f"  ❌ Page {page_index}: {e}")
                return []
    
    async def crawl(self, total_pages: int = 10) -> List[StockData]:
        """Crawl multiple pages with rate limiting"""
        print("=" * 70)
        print(f"CAFEF ASYNC CRAWLER - {self.symbol}")
        print(f"Fetching {total_pages} pages with max 5 concurrent requests")
        print("=" * 70)
        print()
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_page(session, i) for i in range(1, total_pages + 1)]
            results = await asyncio.gather(*tasks)
            
            # Flatten
            all_data = [item for page in results for item in page]
            return all_data

def main():
    start_time = time.time()
    
    # Windows async fix
    if __import__("sys").platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Create crawler and run
    crawler = CafeFAsyncCrawler(symbol="VNINDEX", max_concurrent=5)
    data = asyncio.run(crawler.crawl(total_pages=10))
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 70)
    print("CRAWLING COMPLETE")
    print("=" * 70)
    print(f"Total records: {len(data)}")
    print(f"Time taken: {elapsed:.2f} seconds")
    print(f"Speed: {len(data) / elapsed:.1f} records/second")
    print()
    
    if not data:
        print("❌ No data collected!")
        return
    
    # Export to JSON
    json_file = "vnindex_final.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json_data = [d.model_dump() for d in data]
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"💾 JSON saved: {json_file}")
    
    # Export to CSV
    df = pd.DataFrame([d.model_dump() for d in data])
    csv_file = "vnindex_final.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"💾 CSV saved: {csv_file}")
    
    # Stats
    print()
    print("=" * 70)
    print("DATA PREVIEW")
    print("=" * 70)
    print(df.head(3).to_string())
    
    print()
    print("🎉 Complete! You've built a production-ready async scraper!")
    print()
    print("=" * 70)
    print("SPEED COMPARISON:")
    print("=" * 70)
    print("  Selenium (Level 2):  ~30-60 seconds for 200 records")
    print("  Async API (Level 3): ~5-10 seconds for 200 records")
    print("  ⚡ That's 5-6x faster!")
    print("=" * 70)

if __name__ == "__main__":
    main()
