"""
Infrastructure Layer - BatDongSan Parser

Implements IParser interface for batdongsan.com.vn HTML parsing.
"""
import re
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from batdongsan.domain.entities import (
    PropertyListing, Location, PropertySpecs, ContactInfo, Price,
    ListingType, PropertyType
)
from batdongsan.domain.interfaces import IParser
from batdongsan.infrastructure.config import settings


class BatDongSanParser(IParser):
    """
    HTML parser for batdongsan.com.vn
    
    Handles extraction of property listings from both
    listing pages and detail pages.
    """
    
    BASE_URL = settings.base_url
    
    def parse_listing_page(
        self,
        html: str,
        metadata: Dict[str, Any] = None
    ) -> List[PropertyListing]:
        """
        Parse a listing page and extract property cards.
        
        Args:
            html: Raw HTML content
            metadata: Additional context (listing_type, property_type)
            
        Returns:
            List of PropertyListing entities
        """
        soup = BeautifulSoup(html, 'lxml')
        listings = []
        metadata = metadata or {}
        
        # Find property cards
        cards = soup.select('.js__card')
        
        if not cards:
            # Fallback selectors
            cards = soup.select('[class*="ProductItem"]') or \
                    soup.select('.product-item') or \
                    soup.select('article[class*="card"]')
        
        for card in cards:
            try:
                listing = self._parse_card(card, metadata)
                if listing:
                    listings.append(listing)
            except Exception as e:
                continue
                
        return listings
    
    def parse_detail_page(self, html: str, url: str) -> Optional[PropertyListing]:
        """
        Parse a detail page for full property information.
        
        Args:
            html: Raw HTML content
            url: Page URL
            
        Returns:
            PropertyListing with full details
        """
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            # Title
            title_elem = soup.select_one('h1.re__pr-title') or soup.select_one('h1')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown"
            
            # ID from URL
            listing_id = self._extract_id(url)
            
            # Price
            price_elem = soup.select_one('.re__pr-short-info-item--price') or \
                         soup.select_one('[class*="price"]')
            price_raw = price_elem.get_text(strip=True) if price_elem else "Thỏa thuận"
            price = self._parse_price(price_raw)
            
            # Specs
            specs = self._parse_detail_specs(soup)
            
            # Location
            address_elem = soup.select_one('.re__pr-short-description')
            location = Location()
            if address_elem:
                location = self._parse_location(address_elem.get_text(strip=True))
                
            # Description
            desc_elem = soup.select_one('.re__detail-content')
            description = desc_elem.get_text(strip=True)[:500] if desc_elem else None
            
            # Contact
            contact = self._parse_contact(soup)
            
            # Images
            images = soup.select('.re__media-thumb-item img')
            thumbnail = None
            if images:
                thumbnail = images[0].get('data-src') or images[0].get('src')
            
            return PropertyListing(
                id=listing_id,
                title=title,
                url=url,
                price=price,
                location=location,
                specs=specs,
                contact=contact,
                description=description,
                thumbnail=thumbnail,
                image_count=len(images),
            )
            
        except Exception as e:
            print(f"[!] Parser Error: {e}")
            return None
    
    def extract_detail_urls(self, html: str) -> List[str]:
        """
        Extract detail page URLs from a listing page.
        
        Args:
            html: Raw HTML content
            
        Returns:
            List of detail page URLs
        """
        soup = BeautifulSoup(html, 'lxml')
        urls = []
        
        # Find all links to detail pages
        links = soup.select('a[href*="-pr"]')
        seen = set()
        
        for link in links:
            href = link.get('href', '')
            if href and href not in seen and re.search(r'-pr\d+', href):
                seen.add(href)
                if not href.startswith('http'):
                    href = urljoin(self.BASE_URL, href)
                urls.append(href)
                
        return urls
    
    def _parse_card(
        self,
        card,
        metadata: Dict[str, Any]
    ) -> Optional[PropertyListing]:
        """Parse a property card element"""
        # Find main link
        link = card.select_one('a.js__product-link-for-product-id') or \
               card.select_one('a[href*="-pr"]') or \
               card.select_one('a[title]')
               
        if not link:
            return None
            
        url = link.get('href', '')
        if not url.startswith('http'):
            url = urljoin(self.BASE_URL, url)
            
        # ID
        listing_id = self._extract_id(url)
        
        # Title
        title_elem = card.select_one('.js__card-title') or \
                     card.select_one('[class*="title"]') or link
        title = title_elem.get('title') or title_elem.get_text(strip=True)
        title = title[:200] if len(title) > 200 else title
        
        # Price
        price_elem = card.select_one('.re__card-config-price') or \
                     card.select_one('[class*="price"]')
        price_raw = price_elem.get_text(strip=True) if price_elem else "Thỏa thuận"
        price = self._parse_price(price_raw)
        
        # Area
        area_elem = card.select_one('.re__card-config-area') or \
                    card.select_one('[class*="area"]')
        area = self._parse_area(area_elem.get_text(strip=True)) if area_elem else None
        
        # Location
        location_elem = card.select_one('.re__card-location') or \
                        card.select_one('[class*="location"]')
        location_text = location_elem.get_text(strip=True) if location_elem else ""
        location = self._parse_location(location_text)
        
        # Thumbnail
        img = card.select_one('img')
        thumbnail = img.get('data-src') or img.get('src') if img else None
        
        # Badges
        is_vip = bool(card.select_one('[class*="vip"]'))
        is_verified = bool(card.select_one('[class*="verified"]'))
        
        # Listing type from URL
        listing_type = ListingType.SALE if "/ban-" in url else ListingType.RENT
        
        # Property type from metadata
        property_type = None
        if metadata.get("property_type"):
            try:
                property_type = PropertyType(metadata["property_type"])
            except ValueError:
                pass
        
        return PropertyListing(
            id=listing_id,
            title=title,
            url=url,
            price=price,
            listing_type=listing_type,
            property_type=property_type,
            location=location,
            specs=PropertySpecs(area=area),
            thumbnail=thumbnail,
            is_vip=is_vip,
            is_verified=is_verified,
        )
    
    def _extract_id(self, url: str) -> str:
        """Extract listing ID from URL"""
        match = re.search(r'-pr(\d+)', url)
        return match.group(1) if match else "unknown"
    
    def _parse_price(self, price_text: str) -> Price:
        """Parse price string to Price value object"""
        price_lower = price_text.lower().strip()
        
        patterns = [
            (r'([\d.,]+)\s*tỷ', 1_000_000_000, 'tỷ'),
            (r'([\d.,]+)\s*triệu/?tháng', 1_000_000, 'triệu/tháng'),
            (r'([\d.,]+)\s*triệu', 1_000_000, 'triệu'),
        ]
        
        for pattern, multiplier, unit in patterns:
            match = re.search(pattern, price_lower)
            if match:
                value_str = match.group(1).replace(',', '.')
                # Handle multiple dots
                if value_str.count('.') > 1:
                    value_str = value_str.replace('.', '', value_str.count('.') - 1)
                try:
                    value = float(value_str) * multiplier
                    return Price(raw=price_text, value=value, unit=unit)
                except ValueError:
                    pass
                    
        return Price(raw=price_text)
    
    def _parse_area(self, area_text: str) -> Optional[float]:
        """Parse area string to float"""
        match = re.search(r'([\d.,]+)\s*m²?', area_text)
        if match:
            try:
                return float(match.group(1).replace(',', '.'))
            except ValueError:
                pass
        return None
    
    def _parse_location(self, location_text: str) -> Location:
        """Parse location string to Location entity"""
        location = Location(address=location_text)
        parts = [p.strip() for p in location_text.replace('·', ',').split(',')]
        
        for part in parts:
            part_lower = part.lower()
            if any(x in part_lower for x in ['hà nội', 'tp.hcm', 'hồ chí minh', 'đà nẵng']):
                location.province = part.strip()
            elif 'quận' in part_lower or 'huyện' in part_lower:
                location.district = part.strip()
            elif 'phường' in part_lower or 'xã' in part_lower:
                location.ward = part.strip()
                
        return location
    
    def _parse_detail_specs(self, soup: BeautifulSoup) -> PropertySpecs:
        """Parse specifications from detail page"""
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
            elif 'hướng' in label_text:
                specs.direction = value_text
            elif 'pháp lý' in label_text:
                specs.legal_status = value_text
                
        return specs
    
    def _parse_contact(self, soup: BeautifulSoup) -> ContactInfo:
        """Parse contact info from detail page"""
        contact = ContactInfo()
        
        name_elem = soup.select_one('.re__contact-name')
        if name_elem:
            contact.name = name_elem.get_text(strip=True)
            
        phone_elem = soup.select_one('a[href^="tel:"]')
        if phone_elem:
            contact.phone = phone_elem.get('href', '').replace('tel:', '')
            
        return contact
