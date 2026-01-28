import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import re
from models import CarListing, SellerInfo, CarSpecs
import time
import random
from fake_useragent import UserAgent

class BonbanhCrawler:
    BASE_URL = "https://bonbanh.com"
    
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        
    def _get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetches a URL and returns a BeautifulSoup object"""
        try:
            print(f"Fetching: {url}")
            time.sleep(random.uniform(1, 2)) 
            response = self.session.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def crawl(self, start_page: int = 1, end_page: int = 2) -> List[CarListing]:
        """Loop through pages and scrape listings"""
        all_cars = []
        
        for page in range(start_page, end_page + 1):
            url = f"{self.BASE_URL}/oto/page,{page}?q="
            soup = self.fetch_page(url)
            
            if not soup: continue
            
            # Find all car items by looking for detail links
            # Matches pattern like /xe-vinfast-vf8-*-12345.html
            car_links = soup.find_all('a', href=re.compile(r'/xe-.*-\d+(?:\.html)?$'))
            
            # Deduplicate by parent container to avoid duplicate items
            seen_parents = set()
            items = []
            for link in car_links:
                # Find the container (usually a few levels up)
                parent = link.find_parent('li') or link.find_parent('div', class_=re.compile(r'item|car'))
                if parent and parent not in seen_parents:
                    seen_parents.add(parent)
                    items.append(parent)
            
            if not items:
                print(f"No items found on page {page}")
                continue
                
            print(f"Page {page}: Found {len(items)} cars")
            
            for item in items:
                car = self.parse_car_item(item)
                if car:
                    all_cars.append(car)
                    
        return all_cars

    def parse_car_item(self, item) -> Optional[CarListing]:
        """Parses a car item directly from the listing page"""
        try:
            # Try to find the title link
            title_tag = item.select_one('.cb_title a') or item.select_one('h3 a') or item.find('a', href=re.compile(r'/xe-.*-\d+'))
            
            if not title_tag: return None
            
            url = title_tag['href']
            if not url.startswith('http'):
                url = self.BASE_URL + '/' + url.lstrip('/')
                
            # Normalize URL
            url = url.replace('.com//', '.com/')
                
            title = title_tag.get_text(strip=True)
            
            # ID from URL
            listing_id = "unknown"
            id_match = re.search(r'-(\d+)(?:\.html)?$', url)
            if id_match: listing_id = id_match.group(1)
            
            price_tag = item.select_one('.cb_price') or item.select_one('.price')
            price = price_tag.get_text(strip=True) if price_tag else "Contact"
            
            # Basic stats
            info_text = item.get_text(" | ", strip=True)
            
            year = 0
            year_match = re.search(r'\b(20\d{2}|19\d{2})\b', title + " " + info_text)
            if year_match: year = int(year_match.group(1))
            
            origin = "Unknown"
            if "Nhập khẩu" in info_text: origin = "Nhập khẩu"
            elif "Lắp ráp" in info_text: origin = "Lắp ráp"
            
            status = "Xe cũ" 
            if "Xe mới" in info_text: status = "Xe mới"
            
            return CarListing(
                id=listing_id,
                title=title,
                url=url,
                price=price,
                price_value=None,
                year=year,
                origin=origin,
                status=status,
                seller=SellerInfo(name="See Detail", phone="See Detail"),
                specs=CarSpecs()
            )

        except Exception as e:
            # print(f"Error parsing item: {e}") # Silence errors for demo
            return None
