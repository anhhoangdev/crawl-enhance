import asyncio
import json
import sys
import os
import pandas as pd
from crawler import AsyncCafeFCrawler

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

async def main():
    print("Starting Advanced CafeF VNINDEX Crawler (Async)...")
    
    # Initialize crawler
    # Fetch 50 pages * 20 items = 1000 days (~4 years)
    crawler = AsyncCafeFCrawler(max_concurrency=10)
    
    print("Crawling data...")
    data = await crawler.crawl(total_pages=50, page_size=20)
    
    print(f"\nSuccessfully crawled {len(data)} records.")
    
    if data:
        # Sort by date descending (just in case)
        # Note: Date string is dd/mm/yyyy, sorting string might be wrong if not parsed.
        # But for saving, it's fine.
        
        # Save to JSON
        json_file = "vnindex_advanced.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json_data = [d.model_dump() for d in data]
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"JSON data saved to {json_file}")
        
        # Save to CSV
        csv_file = "vnindex_advanced.csv"
        df = pd.DataFrame([d.model_dump() for d in data])
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"CSV data saved to {csv_file}")
        
        # Print sample
        print("\nSample Data:")
        print(df.head(3))

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
