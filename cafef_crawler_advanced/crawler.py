import aiohttp
import asyncio
from typing import List, Optional
from models import StockData
import json

class AsyncCafeFCrawler:
    BASE_URL = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx"
    
    def __init__(self, symbol: str = "VNINDEX", max_concurrency: int = 5):
        self.symbol = symbol
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*"
        }

    async def fetch_page(self, session: aiohttp.ClientSession, page_index: int, page_size: int = 20) -> List[StockData]:
        """Fetch a single page of data"""
        params = {
            "Symbol": self.symbol,
            "StartDate": "",
            "EndDate": "",
            "PageIndex": page_index,
            "PageSize": page_size
        }
        
        async with self.semaphore:
            try:
                # print(f"Fetching page {page_index}...")
                async with session.get(self.BASE_URL, params=params, headers=self.headers) as response:
                    response.raise_for_status()
                    # CafeF sometimes returns text/plain for JSON
                    try:
                        data = await response.json(content_type=None)
                    except Exception as e:
                        text = await response.text()
                        print(f"Error parsing JSON on page {page_index}: {e}")
                        print(f"Response snippet: {text[:200]}")
                        return []
                    
                    if not data.get("Success"):
                        print(f"Error on page {page_index}: API returned Success=False. Message: {data.get('Message')}")
                        return []
                        
                    items = data.get("Data", {}).get("Data", [])
                    return [StockData(**item) for item in items]
            except Exception as e:
                print(f"Failed to fetch page {page_index}: {e}")
                return []

    async def crawl(self, total_pages: int = 5, page_size: int = 20) -> List[StockData]:
        """Crawl multiple pages in parallel"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(1, total_pages + 1):
                tasks.append(self.fetch_page(session, i, page_size))
            
            results = await asyncio.gather(*tasks)
            
            # Flatten list
            all_data = [item for page_result in results for item in page_result]
            return all_data

if __name__ == "__main__":
    # Test run
    async def main():
        crawler = AsyncCafeFCrawler()
        data = await crawler.crawl(total_pages=2)
        print(f"Fetched {len(data)} records")
        if data:
            print(data[0].model_dump_json(indent=2))
            
    if "win" in __import__("sys").platform:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
