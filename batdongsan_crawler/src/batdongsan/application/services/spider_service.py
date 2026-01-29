"""
Application Layer - Crawler Service

Orchestrates the crawling process using domain interfaces.
Depends on abstractions, not implementations (DIP).
"""
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin

from batdongsan.domain.entities import (
    PropertyListing, CrawlResult, ListingType, PropertyType
)
from batdongsan.domain.interfaces import (
    IHttpClient, IParser, IStorage, IUrlFrontier, CrawlUrl, UrlType
)
from batdongsan.infrastructure.config import settings


@dataclass
class CrawlStats:
    """Statistics for the crawl operation"""
    started_at: datetime = field(default_factory=datetime.now)
    pages_crawled: int = 0
    listings_found: int = 0
    details_crawled: int = 0
    errors: int = 0
    
    @property
    def elapsed_seconds(self) -> float:
        return (datetime.now() - self.started_at).total_seconds()
    
    @property
    def pages_per_minute(self) -> float:
        elapsed = self.elapsed_seconds
        return (self.pages_crawled / elapsed * 60) if elapsed > 0 else 0


class SpiderService:
    """
    Full spider service with async workers.
    
    Orchestrates:
    - URL frontier management
    - Concurrent HTTP requests
    - HTML parsing
    - Data storage
    """
    
    BASE_URL = settings.base_url
    
    def __init__(
        self,
        http_client: IHttpClient,
        parser: IParser,
        storage: IStorage,
        frontier: IUrlFrontier,
        max_concurrent: int = 3,
        crawl_details: bool = False,
    ):
        """
        Initialize the spider service.
        
        Args:
            http_client: HTTP client for fetching pages
            parser: HTML parser for extracting data
            storage: Storage for persisting data
            frontier: URL frontier for queue management
            max_concurrent: Maximum concurrent requests
            crawl_details: Whether to also crawl detail pages
        """
        self._http_client = http_client
        self._parser = parser
        self._storage = storage
        self._frontier = frontier
        self._max_concurrent = max_concurrent
        self._crawl_details = crawl_details
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._stats = CrawlStats()
        
    def add_seed_urls(
        self,
        listing_types: List[str] = None,
        property_types: List[str] = None,
        locations: List[str] = None,
        max_pages: int = 10,
    ) -> int:
        """
        Add seed URLs to the frontier.
        
        Args:
            listing_types: ["ban", "cho-thue"]
            property_types: Property type slugs
            locations: Location slugs
            max_pages: Pages per category
            
        Returns:
            Number of URLs added
        """
        if listing_types is None:
            listing_types = ["ban"]
        if property_types is None:
            property_types = ["can-ho-chung-cu", "nha-rieng"]
            
        count = 0
        
        for listing_type in listing_types:
            for prop_type in property_types:
                base_path = f"/{listing_type}-{prop_type}"
                
                if locations:
                    for location in locations:
                        for page in range(1, max_pages + 1):
                            url = f"{self.BASE_URL}{base_path}-{location}"
                            if page > 1:
                                url += f"/p{page}"
                            if self._frontier.add(CrawlUrl(
                                url=url,
                                url_type=UrlType.LISTING_PAGE,
                                metadata={"listing_type": listing_type, "property_type": prop_type}
                            )):
                                count += 1
                else:
                    for page in range(1, max_pages + 1):
                        url = f"{self.BASE_URL}{base_path}"
                        if page > 1:
                            url += f"/p{page}"
                        if self._frontier.add(CrawlUrl(
                            url=url,
                            url_type=UrlType.LISTING_PAGE,
                            metadata={"listing_type": listing_type, "property_type": prop_type}
                        )):
                            count += 1
                            
        return count
    
    async def _process_listing_page(self, crawl_url: CrawlUrl) -> List[PropertyListing]:
        """Process a listing page"""
        html = await self._http_client.get(crawl_url.url)
        if not html:
            return []
            
        listings = self._parser.parse_listing_page(html, crawl_url.metadata)
        
        # Add detail URLs to frontier if enabled
        if self._crawl_details:
            for listing in listings:
                self._frontier.add(CrawlUrl(
                    url=listing.url,
                    url_type=UrlType.DETAIL_PAGE,
                    priority=2,
                    metadata={"listing_id": listing.id}
                ))
                
        return listings
    
    async def _process_detail_page(self, crawl_url: CrawlUrl) -> Optional[PropertyListing]:
        """Process a detail page"""
        html = await self._http_client.get(crawl_url.url)
        if not html:
            return None
            
        return self._parser.parse_detail_page(html, crawl_url.url)
    
    async def _worker(self, worker_id: int) -> None:
        """Worker coroutine for processing URLs"""
        while True:
            crawl_url = self._frontier.get()
            
            if crawl_url is None:
                await asyncio.sleep(0.5)
                if self._frontier.is_empty():
                    break
                continue
                
            try:
                async with self._semaphore:
                    if crawl_url.url_type == UrlType.LISTING_PAGE:
                        listings = await self._process_listing_page(crawl_url)
                        for listing in listings:
                            self._storage.save(listing)
                            self._stats.listings_found += 1
                        print(f"[W{worker_id}] {crawl_url.url[:50]}... -> {len(listings)} listings")
                        
                    elif crawl_url.url_type == UrlType.DETAIL_PAGE:
                        listing = await self._process_detail_page(crawl_url)
                        if listing:
                            self._storage.save(listing)
                            self._stats.details_crawled += 1
                            
                    self._stats.pages_crawled += 1
                    
            except Exception as e:
                print(f"[W{worker_id}] Error: {e}")
                self._stats.errors += 1
                
            finally:
                self._frontier.complete(crawl_url.url)
    
    async def run(self) -> CrawlResult:
        """
        Run the spider.
        
        Returns:
            CrawlResult with statistics
        """
        print("=" * 50)
        print("BatDongSan Spider")
        print("=" * 50)
        print(f"URLs in queue: {len(self._frontier)}")
        print(f"Concurrent: {self._max_concurrent}")
        print("=" * 50)
        
        self._semaphore = asyncio.Semaphore(self._max_concurrent)
        self._stats = CrawlStats()
        
        try:
            # Create workers
            workers = [
                asyncio.create_task(self._worker(i))
                for i in range(self._max_concurrent)
            ]
            
            # Progress monitor
            async def monitor():
                while not self._frontier.is_empty() or any(not w.done() for w in workers):
                    print(f"\n[Stats] Pages: {self._stats.pages_crawled} | "
                          f"Listings: {self._stats.listings_found} | "
                          f"Errors: {self._stats.errors} | "
                          f"Queue: {len(self._frontier)} | "
                          f"Speed: {self._stats.pages_per_minute:.1f}/min")
                    await asyncio.sleep(10)
                    
            monitor_task = asyncio.create_task(monitor())
            
            # Wait for workers
            await asyncio.gather(*workers)
            monitor_task.cancel()
            
        finally:
            self._storage.close()
            await self._http_client.close()
            
        # Final stats
        print("\n" + "=" * 50)
        print("COMPLETE")
        print("=" * 50)
        print(f"Pages: {self._stats.pages_crawled}")
        print(f"Listings: {self._stats.listings_found}")
        print(f"Errors: {self._stats.errors}")
        print(f"Time: {self._stats.elapsed_seconds:.1f}s")
        
        return CrawlResult(
            success=True,
            total_found=self._stats.listings_found,
            pages_crawled=self._stats.pages_crawled,
            errors=self._stats.errors,
            duration_seconds=self._stats.elapsed_seconds,
        )
