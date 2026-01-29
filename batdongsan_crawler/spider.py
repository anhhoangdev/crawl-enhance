"""
Spider-based crawler for BatDongSan.com.vn
Features:
- URL frontier with priority queue
- Async crawling with rate limiting
- Detail page extraction
- Data pipeline (JSON, CSV export)
- Progress tracking & resume capability
"""
import sys
import asyncio
import json
import csv
import time
import random
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Set, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urljoin, urlparse
from collections import deque
import re

from bs4 import BeautifulSoup
from curl_cffi import requests as curl_requests
from curl_cffi.requests import AsyncSession

from models import PropertyListing, Location, PropertySpecs, ContactInfo

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class URLType(Enum):
    """Type of URL for prioritization"""
    LISTING_PAGE = 1    # Page with multiple listings
    DETAIL_PAGE = 2     # Individual property page
    CATEGORY_PAGE = 3   # Category/filter page


@dataclass
class CrawlURL:
    """URL item for the frontier queue"""
    url: str
    url_type: URLType
    priority: int = 1      # Lower = higher priority
    depth: int = 0         # Crawl depth from seed
    retries: int = 0       # Number of retry attempts
    metadata: Dict = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.url)
    
    def __eq__(self, other):
        return self.url == other.url


@dataclass
class CrawlStats:
    """Crawl statistics"""
    started_at: datetime = field(default_factory=datetime.now)
    pages_crawled: int = 0
    listings_found: int = 0
    details_crawled: int = 0
    errors: int = 0
    bytes_downloaded: int = 0
    
    def elapsed(self) -> float:
        return (datetime.now() - self.started_at).total_seconds()
    
    def pages_per_minute(self) -> float:
        elapsed = self.elapsed()
        return (self.pages_crawled / elapsed * 60) if elapsed > 0 else 0


class URLFrontier:
    """
    URL frontier with deduplication and priority queue
    """
    def __init__(self):
        self.queue: deque = deque()
        self.seen: Set[str] = set()
        self.pending: Set[str] = set()
        
    def add(self, crawl_url: CrawlURL) -> bool:
        """Add URL to frontier if not seen"""
        url_hash = self._normalize_url(crawl_url.url)
        if url_hash in self.seen:
            return False
        self.seen.add(url_hash)
        
        # Insert by priority (lower priority value = higher priority)
        # Simple approach: just append, could use heapq for better perf
        self.queue.append(crawl_url)
        return True
    
    def get(self) -> Optional[CrawlURL]:
        """Get next URL to crawl"""
        if not self.queue:
            return None
        url = self.queue.popleft()
        self.pending.add(url.url)
        return url
    
    def complete(self, url: str):
        """Mark URL as completed"""
        self.pending.discard(url)
        
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication"""
        # Remove trailing slashes, fragments, normalize
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def __len__(self):
        return len(self.queue)
    
    def is_empty(self) -> bool:
        return len(self.queue) == 0 and len(self.pending) == 0


class DataPipeline:
    """
    Pipeline for processing and exporting crawled data
    """
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.listings: List[PropertyListing] = []
        self._json_file = None
        self._csv_file = None
        self._csv_writer = None
        
    def start(self, filename_prefix: str = "batdongsan"):
        """Initialize output files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON Lines file (streaming)
        self._json_file = open(
            self.output_dir / f"{filename_prefix}_{timestamp}.jsonl",
            'w', encoding='utf-8'
        )
        
        # CSV file
        csv_path = self.output_dir / f"{filename_prefix}_{timestamp}.csv"
        self._csv_file = open(csv_path, 'w', encoding='utf-8', newline='')
        self._csv_writer = csv.writer(self._csv_file)
        self._csv_writer.writerow([
            'id', 'title', 'url', 'price', 'price_value', 'price_unit',
            'area', 'bedrooms', 'bathrooms', 'direction',
            'address', 'district', 'province',
            'listing_type', 'property_type', 'is_verified', 'is_vip',
            'posted_date', 'contact_name', 'contact_phone',
            'thumbnail', 'crawled_at'
        ])
        
    def process(self, listing: PropertyListing):
        """Process a single listing"""
        self.listings.append(listing)
        
        # Write to JSON Lines
        if self._json_file:
            self._json_file.write(listing.model_dump_json() + '\n')
            self._json_file.flush()
            
        # Write to CSV
        if self._csv_writer:
            self._csv_writer.writerow([
                listing.id,
                listing.title[:100] if listing.title else '',  # Truncate long titles
                listing.url,
                listing.price,
                listing.price_value,
                listing.price_unit,
                listing.specs.area if listing.specs else None,
                listing.specs.bedrooms if listing.specs else None,
                listing.specs.bathrooms if listing.specs else None,
                listing.specs.direction if listing.specs else None,
                listing.location.address if listing.location else None,
                listing.location.district if listing.location else None,
                listing.location.province if listing.location else None,
                listing.listing_type,
                listing.property_type,
                listing.is_verified,
                listing.is_vip,
                listing.posted_date,
                listing.contact.name if listing.contact else None,
                listing.contact.phone if listing.contact else None,
                listing.thumbnail,
                datetime.now().isoformat()
            ])
            self._csv_file.flush()
            
    def close(self):
        """Close output files"""
        if self._json_file:
            self._json_file.close()
        if self._csv_file:
            self._csv_file.close()
            
    def save_full_json(self, filename: str = "batdongsan_full.json"):
        """Save all listings as a single JSON file"""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(
                [l.model_dump() for l in self.listings],
                f, ensure_ascii=False, indent=2
            )
        return output_path


class BatDongSanSpider:
    """
    Full-featured spider for BatDongSan.com.vn
    
    Features:
    - Async crawling with curl-cffi
    - URL frontier with deduplication
    - Rate limiting & politeness
    - Detail page extraction
    - Data pipeline with JSON/CSV export
    - Progress tracking
    """
    
    BASE_URL = "https://batdongsan.com.vn"
    IMPERSONATE = "chrome120"
    
    # Property type slugs
    PROPERTY_TYPES = {
        "can-ho-chung-cu": "Căn hộ chung cư",
        "nha-rieng": "Nhà riêng",
        "nha-biet-thu": "Nhà biệt thự, liền kề",
        "nha-mat-pho": "Nhà mặt phố",
        "dat-nen": "Đất nền dự án",
        "dat": "Đất",
        "trang-trai": "Trang trại, khu nghỉ dưỡng",
        "kho-xuong": "Kho, nhà xưởng",
        "bat-dong-san-khac": "Bất động sản khác",
    }
    
    def __init__(
        self,
        max_concurrent: int = 5,
        delay_range: tuple = (1.5, 3.0),
        max_retries: int = 3,
        crawl_details: bool = True,
        output_dir: str = "output"
    ):
        """
        Initialize the spider
        
        Args:
            max_concurrent: Maximum concurrent requests
            delay_range: (min, max) seconds between requests
            max_retries: Maximum retry attempts per URL
            crawl_details: Whether to also crawl detail pages
            output_dir: Directory for output files
        """
        self.max_concurrent = max_concurrent
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.crawl_details = crawl_details
        
        self.frontier = URLFrontier()
        self.pipeline = DataPipeline(output_dir)
        self.stats = CrawlStats()
        
        self._session: Optional[AsyncSession] = None
        self._semaphore: Optional[asyncio.Semaphore] = None
        
    async def _get_session(self) -> AsyncSession:
        """Get or create async session"""
        if self._session is None:
            self._session = AsyncSession(impersonate=self.IMPERSONATE)
        return self._session
        
    async def _close_session(self):
        """Close the session"""
        if self._session:
            await self._session.close()
            self._session = None
            
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Referer": self.BASE_URL,
        }
        
    async def _fetch(self, url: str) -> Optional[str]:
        """Fetch a URL with rate limiting"""
        await asyncio.sleep(random.uniform(*self.delay_range))
        
        try:
            session = await self._get_session()
            response = await session.get(
                url,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            self.stats.bytes_downloaded += len(response.content)
            return response.text
        except Exception as e:
            print(f"[!] Error fetching {url}: {e}")
            return None
            
    def add_seed_urls(
        self,
        listing_types: List[str] = ["ban"],
        property_types: List[str] = None,
        locations: List[str] = None,
        max_pages: int = 10
    ):
        """
        Add seed URLs to the frontier
        
        Args:
            listing_types: ["ban", "cho-thue"]
            property_types: Property type slugs (None = all)
            locations: Location slugs (None = all)
            max_pages: Maximum pages per category
        """
        if property_types is None:
            property_types = list(self.PROPERTY_TYPES.keys())[:3]  # Top 3 by default
            
        for listing_type in listing_types:
            for prop_type in property_types:
                base_path = f"/{listing_type}-{prop_type}"
                
                if locations:
                    for location in locations:
                        for page in range(1, max_pages + 1):
                            url = f"{self.BASE_URL}{base_path}-{location}"
                            if page > 1:
                                url += f"/p{page}"
                            self.frontier.add(CrawlURL(
                                url=url,
                                url_type=URLType.LISTING_PAGE,
                                priority=1,
                                metadata={"listing_type": listing_type, "property_type": prop_type}
                            ))
                else:
                    for page in range(1, max_pages + 1):
                        url = f"{self.BASE_URL}{base_path}"
                        if page > 1:
                            url += f"/p{page}"
                        self.frontier.add(CrawlURL(
                            url=url,
                            url_type=URLType.LISTING_PAGE,
                            priority=1,
                            metadata={"listing_type": listing_type, "property_type": prop_type}
                        ))
                        
        print(f"[*] Added {len(self.frontier)} seed URLs to frontier")
        
    async def _process_listing_page(self, crawl_url: CrawlURL) -> List[PropertyListing]:
        """Process a listing page and extract property cards"""
        html = await self._fetch(crawl_url.url)
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'lxml')
        listings = []
        
        # Find property cards
        cards = soup.select('.js__card')
        
        if not cards:
            # Fallback selectors
            cards = soup.select('[class*="ProductItem"]') or \
                    soup.select('.product-item') or \
                    soup.select('article[class*="card"]')
        
        for card in cards:
            try:
                listing = self._parse_card(card, crawl_url.metadata)
                if listing:
                    listings.append(listing)
                    
                    # Add detail page to frontier if enabled
                    if self.crawl_details and listing.url:
                        self.frontier.add(CrawlURL(
                            url=listing.url,
                            url_type=URLType.DETAIL_PAGE,
                            priority=2,
                            depth=crawl_url.depth + 1,
                            metadata={"listing_id": listing.id}
                        ))
            except Exception as e:
                print(f"[!] Error parsing card: {e}")
                continue
                
        return listings
        
    def _parse_card(self, card, metadata: Dict = None) -> Optional[PropertyListing]:
        """Parse a property card"""
        # Find the main link
        link = card.select_one('a.js__product-link-for-product-id') or \
               card.select_one('a[href*="-pr"]') or \
               card.select_one('a[title]')
               
        if not link:
            return None
            
        url = link.get('href', '')
        if not url.startswith('http'):
            url = urljoin(self.BASE_URL, url)
            
        # Extract ID from URL
        listing_id = "unknown"
        id_match = re.search(r'-pr(\d+)', url)
        if id_match:
            listing_id = id_match.group(1)
            
        # Title - get from specific element or link
        title_elem = card.select_one('.js__card-title') or \
                     card.select_one('[class*="title"]') or \
                     link
        title = title_elem.get('title') or title_elem.get_text(strip=True)
        
        # Truncate title if too long (captured extra text)
        if len(title) > 200:
            title = title[:200] + "..."
            
        # Price
        price_elem = card.select_one('.re__card-config-price') or \
                     card.select_one('[class*="price"]')
        price = price_elem.get_text(strip=True) if price_elem else "Thỏa thuận"
        price_value, price_unit = self._parse_price(price)
        
        # Area
        area_elem = card.select_one('.re__card-config-area') or \
                    card.select_one('[class*="area"]')
        area_text = area_elem.get_text(strip=True) if area_elem else ""
        area = self._parse_area(area_text)
        
        # Location
        location_elem = card.select_one('.re__card-location') or \
                        card.select_one('[class*="location"]')
        location_text = location_elem.get_text(strip=True) if location_elem else ""
        
        # Parse location parts
        location = self._parse_location(location_text)
        
        # Thumbnail
        img = card.select_one('img')
        thumbnail = None
        if img:
            thumbnail = img.get('data-src') or img.get('src')
            
        # Badges
        is_vip = bool(card.select_one('[class*="vip"]') or card.select_one('[class*="featured"]'))
        is_verified = bool(card.select_one('[class*="verified"]'))
        
        # Posted date
        date_elem = card.select_one('[class*="date"]') or card.select_one('time')
        posted_date = date_elem.get_text(strip=True) if date_elem else None
        
        # Listing type
        listing_type = "Bán" if "/ban-" in url else "Cho thuê"
        property_type = metadata.get("property_type") if metadata else None
        
        return PropertyListing(
            id=listing_id,
            title=title,
            url=url,
            price=price,
            price_value=price_value,
            price_unit=price_unit,
            listing_type=listing_type,
            property_type=self.PROPERTY_TYPES.get(property_type),
            location=location,
            specs=PropertySpecs(area=area),
            thumbnail=thumbnail,
            posted_date=posted_date,
            is_vip=is_vip,
            is_verified=is_verified
        )
        
    async def _process_detail_page(self, crawl_url: CrawlURL) -> Optional[PropertyListing]:
        """Process a detail page for full information"""
        html = await self._fetch(crawl_url.url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            # Title
            title_elem = soup.select_one('h1.re__pr-title') or soup.select_one('h1')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown"
            
            # ID from URL
            listing_id = crawl_url.metadata.get("listing_id", "unknown")
            if listing_id == "unknown":
                id_match = re.search(r'-pr(\d+)', crawl_url.url)
                if id_match:
                    listing_id = id_match.group(1)
            
            # Price
            price_elem = soup.select_one('.re__pr-short-info-item--price') or \
                         soup.select_one('[class*="price"]')
            price = price_elem.get_text(strip=True) if price_elem else "Thỏa thuận"
            price_value, price_unit = self._parse_price(price)
            
            # Specs
            specs = PropertySpecs()
            spec_items = soup.select('.re__pr-specs-content-item')
            
            for item in spec_items:
                label = item.select_one('.re__pr-specs-content-item-title')
                value = item.select_one('.re__pr-specs-content-item-value')
                
                if not label or not value:
                    continue
                    
                label_text = label.get_text(strip=True).lower()
                value_text = value.get_text(strip=True)
                
                if 'diện tích' in label_text:
                    specs.area = self._parse_area(value_text)
                elif 'phòng ngủ' in label_text:
                    match = re.search(r'(\d+)', value_text)
                    if match:
                        specs.bedrooms = int(match.group(1))
                elif 'phòng tắm' in label_text or 'toilet' in label_text:
                    match = re.search(r'(\d+)', value_text)
                    if match:
                        specs.bathrooms = int(match.group(1))
                elif 'hướng nhà' in label_text:
                    specs.direction = value_text
                elif 'pháp lý' in label_text:
                    specs.legal_status = value_text
                elif 'nội thất' in label_text:
                    specs.interior = value_text
                elif 'số tầng' in label_text:
                    match = re.search(r'(\d+)', value_text)
                    if match:
                        specs.floors = int(match.group(1))
                        
            # Location
            address_elem = soup.select_one('.re__pr-short-description')
            location = Location()
            if address_elem:
                location.address = address_elem.get_text(strip=True)
                location = self._parse_location(location.address)
                
            # Description
            desc_elem = soup.select_one('.re__detail-content')
            description = desc_elem.get_text(strip=True) if desc_elem else None
            
            # Contact
            contact = ContactInfo()
            contact_name_elem = soup.select_one('.re__contact-name')
            if contact_name_elem:
                contact.name = contact_name_elem.get_text(strip=True)
                
            phone_elem = soup.select_one('a[href^="tel:"]')
            if phone_elem:
                contact.phone = phone_elem.get('href', '').replace('tel:', '')
                
            # Images count
            images = soup.select('.re__media-thumb-item')
            image_count = len(images)
            
            # Thumbnail
            main_img = soup.select_one('.re__media-thumb-item img')
            thumbnail = None
            if main_img:
                thumbnail = main_img.get('data-src') or main_img.get('src')
                
            return PropertyListing(
                id=listing_id,
                title=title,
                url=crawl_url.url,
                price=price,
                price_value=price_value,
                price_unit=price_unit,
                location=location,
                specs=specs,
                description=description[:500] if description else None,  # Truncate
                contact=contact,
                thumbnail=thumbnail,
                image_count=image_count
            )
            
        except Exception as e:
            print(f"[!] Error parsing detail page: {e}")
            return None
            
    def _parse_price(self, price_text: str) -> tuple:
        """Parse price string"""
        price_text = price_text.lower().strip()
        
        patterns = [
            (r'([\d.,]+)\s*tỷ', 1_000_000_000, 'tỷ'),
            (r'([\d.,]+)\s*triệu/?tháng', 1_000_000, 'triệu/tháng'),
            (r'([\d.,]+)\s*triệu', 1_000_000, 'triệu'),
        ]
        
        for pattern, multiplier, unit in patterns:
            match = re.search(pattern, price_text)
            if match:
                value_str = match.group(1).replace(',', '.').replace('.', '', match.group(1).count('.') - 1)
                try:
                    return float(value_str) * multiplier, unit
                except ValueError:
                    pass
                    
        return None, None
        
    def _parse_area(self, area_text: str) -> Optional[float]:
        """Parse area string"""
        match = re.search(r'([\d.,]+)\s*m²?', area_text)
        if match:
            try:
                return float(match.group(1).replace(',', '.'))
            except ValueError:
                pass
        return None
        
    def _parse_location(self, location_text: str) -> Location:
        """Parse location string into structured Location"""
        location = Location(address=location_text)
        
        # Common patterns for Vietnamese addresses
        # "Quận Cầu Giấy, Hà Nội" or "Phường X, Quận Y, TP.HCM"
        parts = [p.strip() for p in location_text.replace('·', ',').split(',')]
        
        for part in parts:
            part_lower = part.lower()
            if any(x in part_lower for x in ['hà nội', 'tp.hcm', 'hồ chí minh', 'đà nẵng']):
                location.province = part.strip()
            elif 'quận' in part_lower or 'huyện' in part_lower or 'thành phố' in part_lower:
                location.district = part.strip()
            elif 'phường' in part_lower or 'xã' in part_lower:
                location.ward = part.strip()
            elif 'đường' in part_lower or 'phố' in part_lower:
                location.street = part.strip()
                
        return location
        
    async def _worker(self, worker_id: int):
        """Worker coroutine for processing URLs"""
        while True:
            crawl_url = self.frontier.get()
            if crawl_url is None:
                await asyncio.sleep(0.5)
                # Check if we should exit
                if self.frontier.is_empty():
                    break
                continue
                
            try:
                async with self._semaphore:
                    if crawl_url.url_type == URLType.LISTING_PAGE:
                        listings = await self._process_listing_page(crawl_url)
                        for listing in listings:
                            self.pipeline.process(listing)
                            self.stats.listings_found += 1
                        print(f"[Worker-{worker_id}] Page: {crawl_url.url[:60]}... -> {len(listings)} listings")
                        
                    elif crawl_url.url_type == URLType.DETAIL_PAGE:
                        listing = await self._process_detail_page(crawl_url)
                        if listing:
                            self.pipeline.process(listing)
                            self.stats.details_crawled += 1
                            print(f"[Worker-{worker_id}] Detail: {listing.id} - {listing.title[:40]}...")
                            
                    self.stats.pages_crawled += 1
                    
            except Exception as e:
                print(f"[Worker-{worker_id}] Error: {e}")
                self.stats.errors += 1
                
                # Retry logic
                if crawl_url.retries < self.max_retries:
                    crawl_url.retries += 1
                    self.frontier.add(crawl_url)
                    
            finally:
                self.frontier.complete(crawl_url.url)
                
    async def run(self):
        """Run the spider"""
        print("=" * 60)
        print("BatDongSan.com.vn Spider")
        print("=" * 60)
        print(f"[*] URLs in frontier: {len(self.frontier)}")
        print(f"[*] Max concurrent: {self.max_concurrent}")
        print(f"[*] Crawl details: {self.crawl_details}")
        print("=" * 60)
        
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        self.pipeline.start()
        
        try:
            # Create workers
            workers = [
                asyncio.create_task(self._worker(i))
                for i in range(self.max_concurrent)
            ]
            
            # Progress monitor
            async def monitor():
                while not self.frontier.is_empty() or any(not w.done() for w in workers):
                    print(f"\n[Stats] Pages: {self.stats.pages_crawled} | "
                          f"Listings: {self.stats.listings_found} | "
                          f"Details: {self.stats.details_crawled} | "
                          f"Errors: {self.stats.errors} | "
                          f"Queue: {len(self.frontier)} | "
                          f"Speed: {self.stats.pages_per_minute():.1f} pages/min")
                    await asyncio.sleep(10)
                    
            monitor_task = asyncio.create_task(monitor())
            
            # Wait for all workers
            await asyncio.gather(*workers)
            monitor_task.cancel()
            
        finally:
            self.pipeline.close()
            await self._close_session()
            
        # Final stats
        print("\n" + "=" * 60)
        print("CRAWL COMPLETE")
        print("=" * 60)
        print(f"Total pages crawled: {self.stats.pages_crawled}")
        print(f"Total listings found: {self.stats.listings_found}")
        print(f"Detail pages crawled: {self.stats.details_crawled}")
        print(f"Errors: {self.stats.errors}")
        print(f"Total time: {self.stats.elapsed():.1f}s")
        print(f"Average speed: {self.stats.pages_per_minute():.1f} pages/min")
        print(f"Data downloaded: {self.stats.bytes_downloaded / 1024 / 1024:.2f} MB")
        
        # Save full JSON
        output_path = self.pipeline.save_full_json()
        print(f"Output saved to: {output_path}")
        
        return self.pipeline.listings


# CLI Entry point
async def main():
    spider = BatDongSanSpider(
        max_concurrent=3,           # Concurrent requests
        delay_range=(2.0, 4.0),     # Delay between requests
        crawl_details=False,        # Set True to also crawl detail pages
        output_dir="output"
    )
    
    # Add seed URLs
    spider.add_seed_urls(
        listing_types=["ban"],      # "ban" = for sale, "cho-thue" = for rent
        property_types=["can-ho-chung-cu", "nha-rieng"],  # Property types
        max_pages=3                 # Pages per category
    )
    
    # Run the spider
    listings = await spider.run()
    print(f"\nTotal listings collected: {len(listings)}")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
